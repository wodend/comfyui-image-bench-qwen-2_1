#!/usr/bin/env python3
"""Import a completed T2I pair, correlate a recent ComfyUI timing, and rebuild."""
import argparse
from datetime import datetime
import hashlib
import heapq
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import zlib

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
TIMING = re.compile(r"^\[(?P<time>[^]]+)\] \[INFO\] Prompt executed in (?:(?P<seconds>\d+(?:\.\d+)?) seconds|(?P<hms>\d{1,2}:\d{2}:\d{2}))$")


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def png_info(path):
    """Read dimensions and ComfyUI text chunks without touching image pixels."""
    metadata = {}
    with path.open("rb") as stream:
        if stream.read(8) != PNG_SIGNATURE:
            raise ValueError(f"Not a PNG: {path}")
        width = height = None
        while True:
            raw_length = stream.read(4)
            if not raw_length:
                break
            if len(raw_length) != 4:
                raise ValueError(f"Truncated PNG: {path}")
            length = struct.unpack(">I", raw_length)[0]
            kind = stream.read(4)
            if length > 32 * 1024 * 1024:
                raise ValueError(f"Oversized PNG chunk: {path}")
            data = stream.read(length)
            crc = stream.read(4)
            if len(kind) != 4 or len(data) != length or len(crc) != 4:
                raise ValueError(f"Truncated PNG chunk: {path}")
            if zlib.crc32(kind + data) != struct.unpack(">I", crc)[0]:
                raise ValueError(f"PNG chunk CRC mismatch: {path}")
            if kind == b"IHDR":
                width, height = struct.unpack(">II", data[:8])
            elif kind == b"tEXt" and b"\0" in data:
                key, value = data.split(b"\0", 1)
                metadata[key.decode("latin-1")] = value.decode("utf-8")
            elif kind == b"zTXt" and b"\0" in data:
                key, remainder = data.split(b"\0", 1)
                if remainder[:1] == b"\0":
                    metadata[key.decode("latin-1")] = zlib.decompress(remainder[1:]).decode("utf-8")
            elif kind == b"iTXt" and b"\0" in data:
                key, remainder = data.split(b"\0", 1)
                compressed, method = remainder[:2]
                rest = remainder[2:]
                _, rest = rest.split(b"\0", 1)  # language
                _, value = rest.split(b"\0", 1)  # translated keyword
                if compressed:
                    if method != 0:
                        raise ValueError(f"Unsupported PNG text compression: {path}")
                    value = zlib.decompress(value)
                metadata[key.decode("latin-1")] = value.decode("utf-8")
            if kind == b"IEND":
                break
    if not width or not height:
        raise ValueError(f"Missing PNG dimensions: {path}")
    return width, height, metadata


def recent_log(log_path, lines=1000):
    if not log_path.is_file():
        return [], []
    result = subprocess.run(["tail", "-n", str(lines), str(log_path)],
                            check=True, text=True, capture_output=True)
    entries = result.stdout.splitlines()
    timings = []
    for index, line in enumerate(entries):
        match = TIMING.match(line)
        if match:
            if match["seconds"] is not None:
                seconds = float(match["seconds"])
            else:
                hours, minutes, seconds_part = map(int, match["hms"].split(":"))
                seconds = hours * 3600 + minutes * 60 + seconds_part
            timings.append((index, datetime.strptime(match["time"], "%Y-%m-%d %H:%M:%S,%f"),
                            seconds, match["time"]))
    return entries, timings


def match_source(qwen_path, source_arg, output_dir):
    target_hash = sha256(qwen_path)
    if source_arg:
        candidates = [source_arg]
    elif output_dir.is_dir():
        candidates = heapq.nlargest(100, output_dir.rglob("*.png"), key=lambda p: p.stat().st_mtime)
    else:
        candidates = []
    for candidate in candidates:
        if candidate.is_file() and candidate.stat().st_size == qwen_path.stat().st_size and sha256(candidate) == target_hash:
            return candidate
    return None


def match_timing(source, entries, timings):
    if source is None:
        return None
    saved = datetime.fromtimestamp(source.stat().st_mtime)
    matches = sorted(((abs((completed - saved).total_seconds()), index, seconds, stamp)
                      for index, completed, seconds, stamp in timings))
    if not matches or matches[0][0] > 5 or (len(matches) > 1 and matches[1][0] <= 5):
        return None
    _, index, seconds, stamp = matches[0]
    started = next((i for i in range(index - 1, -1, -1) if "Starting server" in entries[i]), -1)
    earlier = any(started < i < index for i, _, _, _ in timings)
    kind = "Subsequent run" if earlier else "First observed in log tail"
    return {"seconds": seconds, "logged_at": stamp, "kind": kind, "line": entries[index]}


def write_text(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def run(args):
    record_path = ROOT / "benchmarks/records" / f"{args.test_id}.json"
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.test_id) or not record_path.is_file():
        raise ValueError("Use the ID of an approved structured benchmark record")
    record = json.loads(record_path.read_text())
    if record["id"] != args.test_id or record["group"] != "t2i":
        raise ValueError("This script currently processes only T2I records with matching IDs")
    images = {model: SITE / "assets/images" / args.test_id / model / "output-001.png"
              for model in ("qwen-image-2-1", "chatgpt")}
    missing = [str(path) for path in images.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError("Copy both originals before running:\n" + "\n".join(missing))
    info = {model: png_info(path) for model, path in images.items()}
    qwen_meta = info["qwen-image-2-1"][2]
    if not {"prompt", "workflow"} <= qwen_meta.keys():
        raise ValueError("Qwen PNG has no embedded prompt and workflow; provide the originals")
    graph = json.loads(qwen_meta["prompt"])
    workflow = json.loads(qwen_meta["workflow"])
    encoders = [node for node in graph.values() if node.get("class_type") == "TextEncodeQwenImage21"]
    samplers = [node for node in graph.values() if node.get("class_type") == "KSampler"]
    if len(encoders) != 1 or len(samplers) != 1:
        raise ValueError("Expected one Qwen text encoder and one sampler; inspect workflow manually")
    exact = encoders[0]["inputs"]["prompt"]
    try:
        description = json.loads(exact)["rewritten_prompt"]
    except (ValueError, KeyError, TypeError):
        description = exact
    if description != record["prompt"]["display"]:
        raise ValueError("Qwen's actual prompt differs from the approved display prompt; review before importing")
    sampler = samplers[0]["inputs"]
    source = match_source(images["qwen-image-2-1"], args.qwen_source, args.comfy_output_dir)
    entries, timings = recent_log(args.log)
    timing = match_timing(source, entries, timings)
    if args.check:
        for model, path in images.items():
            print(f"{model}: {path.name}, {info[model][0]} × {info[model][1]}, sha256 {sha256(path)}")
        print(f"Original Qwen output: {source or 'not found'}")
        print(f"Matched recent timing: {timing['line'] if timing else 'none (leave timing unrecorded)'}")
        return
    data_dir = SITE / "data" / args.test_id
    prompt_path = data_dir / "prompt.json"
    workflow_path = data_dir / "workflow.json"
    api_path = data_dir / "workflow-api.json"
    write_text(prompt_path, exact + "\n")
    write_text(workflow_path, json.dumps(workflow, indent=2, ensure_ascii=False) + "\n")
    write_text(api_path, json.dumps(graph, indent=2, ensure_ascii=False) + "\n")
    artifact_paths = [*images.values(), prompt_path, workflow_path, api_path]
    manifest_path = data_dir / "manifest.json"
    manifest = {"path_base": "site/", "files": {
        str(path.relative_to(SITE)): {"sha256": sha256(path), "bytes": path.stat().st_size}
        for path in artifact_paths}}
    write_text(manifest_path, json.dumps(manifest, indent=2) + "\n")
    outputs = []
    for model, path in images.items():
        width, height, _ = info[model]
        qwen = model == "qwen-image-2-1"
        outputs.append({
            "model_id": model,
            "label": "Qwen Image 2.1" if qwen else "ChatGPT image output",
            "path": str(path.relative_to(SITE)),
            "alt": ("Qwen" if qwen else "ChatGPT") + f" original output for {record['title']}",
            "caption": ("Local ComfyUI" if qwen else "Operator-supplied PNG") + f" · {width} × {height}",
            "width": width, "height": height,
            "duration_seconds": timing["seconds"] if qwen and timing else None,
            "timing_kind": timing["kind"] if qwen and timing else None,
            **({"logged_at": timing["logged_at"], "timing_source": str(args.log.relative_to(ROOT))
                if args.log.is_relative_to(ROOT) else str(args.log)} if qwen and timing else {}),
            **({"seed": sampler.get("seed")} if qwen else {})
        })
    record["status"] = "complete"
    record["summary"] = f"Both original outputs for {record['title']} are available for side-by-side review. Reference selection for the later edit remains pending."
    record["prompt"]["submitted"] = {"qwen": str(prompt_path.relative_to(SITE)),
                                      "chatgpt": str(prompt_path.relative_to(SITE))}
    record["prompt"]["note"] = "The exact submitted prompt is archived below. The ChatGPT PNG has no generation metadata."
    record["outputs"] = outputs
    record["pending_models"] = []
    record["settings"] = [
        ["Seed", str(sampler.get("seed", "Not recorded")), "Not recorded"],
        ["Steps / CFG", f"{sampler.get('steps', 'unknown')} / {sampler.get('cfg', 'unknown')}", "Not exposed in supplied record"],
        ["Sampler / scheduler", f"{sampler.get('sampler_name', 'unknown')} / {sampler.get('scheduler', 'unknown')}", "Not exposed in supplied record"],
        ["Output dimensions", f"{info['qwen-image-2-1'][0]} × {info['qwen-image-2-1'][1]}", f"{info['chatgpt'][0]} × {info['chatgpt'][1]}"],
        ["Timing", f"{timing['seconds']:.2f} seconds ({timing['kind'].lower()})" if timing else "Not safely matched to this output", "Not recorded"],
    ]
    timing_note = (f"ComfyUI log: {timing['line']}. Matched to the original Qwen PNG by SHA-256 and its save time."
                   if timing else "A unique ComfyUI timing could not be matched to the original Qwen PNG; none was inferred.")
    record["notes"] = [timing_note, "No ChatGPT timing or generation metadata is available from the supplied PNG."]
    record["artifacts"] = [["ComfyUI workflow", str(workflow_path.relative_to(SITE))],
                           ["API workflow", str(api_path.relative_to(SITE))],
                           ["Exact submitted prompt", str(prompt_path.relative_to(SITE))],
                           ["Image and artifact hashes", str(manifest_path.relative_to(SITE))]]
    write_text(record_path, json.dumps(record, indent=2, ensure_ascii=False) + "\n")
    handoff = ROOT / "benchmarks" / f"{args.test_id}.md"
    if handoff.is_file():
        text = handoff.read_text()
        text = re.sub(r"(?m)^Status: .*", "Status: ready for review — both outputs imported", text, count=1)
        marker = "\n<!-- postgen:start -->"
        text = text.split(marker, 1)[0]
        text += (f"\n<!-- postgen:start -->\n## Post-generation capture\n\n"
                 f"- Qwen original: `{images['qwen-image-2-1'].relative_to(ROOT)}`; SHA-256 `{sha256(images['qwen-image-2-1'])}`.\n"
                 f"- ChatGPT original: `{images['chatgpt'].relative_to(ROOT)}`; SHA-256 `{sha256(images['chatgpt'])}`.\n"
                 f"- Qwen actual seed: `{sampler.get('seed', 'unavailable')}`; steps: `{sampler.get('steps', 'unavailable')}`; CFG: `{sampler.get('cfg', 'unavailable')}`; sampler/scheduler: `{sampler.get('sampler_name', 'unavailable')}/{sampler.get('scheduler', 'unavailable')}`.\n"
                 f"- Timing: {timing_note}\n"
                 f"- Captured artifacts: `site/data/{args.test_id}/`. Visual review and reference selection remain pending.\n"
                 "<!-- postgen:end -->\n")
        write_text(handoff, text)
    print(f"Imported {args.test_id}; timing: {timing['seconds'] if timing else 'unmatched'} seconds")
    subprocess.run([sys.executable, str(ROOT / "scripts/build_site.py")], cwd=ROOT, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--test-id", required=True, help="Approved T2I task ID")
    parser.add_argument("--check", action="store_true", help="Inspect inputs and timing without writing files")
    parser.add_argument("--log", type=Path, default=ROOT / "logs/comfyui-current.log")
    parser.add_argument("--comfy-output-dir", type=Path, default=Path("/mnt/hdd/ComfyUIOutput"))
    parser.add_argument("--qwen-source", type=Path, help="Original ComfyUI output PNG if auto-detection misses it")
    args = parser.parse_args()
    try:
        run(args)
    except (ValueError, FileNotFoundError, KeyError, json.JSONDecodeError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
