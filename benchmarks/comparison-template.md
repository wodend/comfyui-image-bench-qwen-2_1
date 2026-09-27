## T2I or I2I · Task name

Describe the task and identify the source of each model label. Link a completed run record.

### Prompt

ChatGPT was used to generate the prompts used.

Include the exact shared submitted prompt. For I2I, include input images and hashes.

### Results

Copy this HTML into `site/index.md`, replacing paths, dimensions, labels, and descriptions:

```html
<div class="comparison" aria-label="Task comparison">
<figure>
<a href="assets/images/<test-id>/qwen-image-2-1/output-001.png"><img src="assets/images/<test-id>/qwen-image-2-1/output-001.png" width="1184" height="1776" alt="Describe the Qwen output"></a>
<figcaption><strong>Qwen Image 2.1</strong><span>Configuration and output size</span></figcaption>
</figure>
<figure>
<a href="assets/images/<test-id>/chatgpt/output-001.png"><img src="assets/images/<test-id>/chatgpt/output-001.png" width="1024" height="1536" alt="Describe the ChatGPT output"></a>
<figcaption><strong>Recorded ChatGPT model label</strong><span>Configuration and output size</span></figcaption>
</figure>
</div>
```

### Recorded settings

Record settings for both models, identify missing values, and link the exact workflow, environment lock, prompts, input images, and SHA-256 manifest under `data/<test-id>/`.
