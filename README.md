# Seedream API — Python client

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![Hosted on Synexa](https://img.shields.io/badge/hosted%20on-Synexa-6366f1.svg)](https://synexa.ai/explore/bytedance/seedream-5-pro-edit?utm_source=github&utm_medium=ugc&utm_campaign=seedream-dev&utm_content=readme-badge&utm_term=tier-a)

Seedream is ByteDance Seed's proprietary image model family, and Seedream 5.0 Pro is its editing tier: it changes exactly the element you describe ("swap the red chair for a green one") and leaves the rest of the picture untouched, working from up to ten reference images. This package is a Python client for the Seedream API hosted on Synexa, so `pip install` and one `run()` call turn an image URL and an instruction into an edited image.

The client gives you a blocking `run()` that returns the output URL, a submit-and-poll mode, webhook delivery on completion, and typed errors. Its only dependency is `httpx`. It suits product teams, design tools and content pipelines that want a state-of-the-art editor as a function call, without an enterprise cloud contract or any GPU of their own.

> **Try it now:** [https://synexa.ai/explore/bytedance/seedream-5-pro-edit](https://synexa.ai/explore/bytedance/seedream-5-pro-edit?utm_source=github&utm_medium=ugc&utm_campaign=seedream-dev&utm_content=readme-top&utm_term=tier-a) — the hosted model behind this client. New accounts get a free trial credit.

## Contents

- [Why this client](#why-this-client)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Hosted models](#hosted-models)
- [Parameters](#parameters)
- [Advanced usage](#advanced-usage)
- [About Seedream](#about-seedream)
- [Use cases](#use-cases)
- [FAQ](#faq)
- [License](#license)

## Why this client

- **There are no weights to self-host.** Seedream is a closed model; ByteDance does not release checkpoints, so the only way to run it is through an API. The hosted endpoint gives you that from a single `pip install`.
- **No enterprise onboarding.** ByteDance's own cloud access to Seedream runs through platform accounts, quotas and regional consoles. Here the setup is an API key and an environment variable.
- **No GPU, no cold start, no scaling work.** The model runs on warm datacenter instances; you send a request and receive a URL, and concurrency is handled for you.
- **$0.0675 per edit, billed per run.** No subscription tier to size and nothing to pay between jobs: a thousand edits cost $67.50, and a prototype that makes ten costs less than a dollar.

## Installation

```bash
pip install git+https://github.com/seedream-dev/seedream-api.git
```

Then set your API key (create one at [synexa.ai](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=seedream-dev&utm_content=readme-apikey&utm_term=tier-a)):

```bash
export SYNEXA_API_KEY="sk-..."
```

## Quickstart

```python
import seedream_api

output = seedream_api.run({
    "prompt": "Replace the sky with a dramatic sunset, keep everything else exactly as it is",
    "image_urls": [
        "https://example.com/input.png"
    ]
})
print(output)   # URL(s) of the generated result
```

Or with an explicit client:

```python
from seedream_api import Client

client = Client(api_key="sk-...")
output = client.run({"prompt": "Replace the sky with a dramatic sunset, keep everything else exactly as it is", "image_urls": ["https://example.com/input.png"]})
```

## Hosted models

| Model | Category | What it does | Price / run |
|---|---|---|---|
| [`bytedance/seedream-5-pro-edit`](https://synexa.ai/explore/bytedance/seedream-5-pro-edit?utm_source=github&utm_medium=ugc&utm_campaign=seedream-dev&utm_content=readme-models&utm_term=tier-a) | image-to-image | Seedream 5.0 Pro is a region-precise image editor that changes one element of a picture while leaving the rest untouched. | $0.0675 |

The default model is **`bytedance/seedream-5-pro-edit`**; pass `model="owner/name"` to `run()` to use another one from the table.

## Parameters

### `bytedance/seedream-5-pro-edit`

| Field | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `prompt` | string | yes | `Replace the sky with a dramatic sunset, …` | — | The text prompt used to edit the image. |
| `image_size` | string | no | `auto_2K` | square_hd, square, portrait_4_3, portrait_16_9, landscape… | The size of the generated image. Total pixels must be between 1024x1024 and 2048x2048, with aspect ratio between 1/16 and 16. |
| `num_images` | integer | no | `1` | 1, 6 | Number of separate model generations to run with the prompt. |
| `output_format` | string | no | `jpeg` | jpeg, png | The file format of the generated image. |
| `image_urls` | files | yes | — | — | Input / reference images (.jpg/.png/.webp), up to 10. The first one is the image being edited |

## Advanced usage

**Submit without blocking, then poll:**

```python
prediction = client.run(input, wait=False)      # returns immediately
prediction = client.wait(prediction, timeout=300)
print(prediction["output"])
```

**Webhook on completion:**

```python
client.run(input, wait=False, webhook="https://your-app.example/hooks/synexa")
```

**Errors:**

```python
from seedream_api import ModelError, PredictionTimeout

try:
    output = client.run(input)
except ModelError as e:
    print("failed:", e, e.prediction and e.prediction.get("id"))
except PredictionTimeout:
    print("still running — poll later")
```

Status values you will see on a prediction: `starting` → `processing` → `succeeded` | `failed`.

## About Seedream

Seedream is the family of image generation and editing models developed by ByteDance's [Seed](https://seed.bytedance.com/en/seedream) research team. Seedream 3.0, released in 2025, was notable for native high-resolution output and reliable bilingual (Chinese and English) text rendering; Seedream 4.0 unified generation and editing in one model and introduced multi-reference input, so several source images can jointly condition a result. The models are proprietary: ByteDance serves them through its own cloud platforms and consumer apps rather than releasing weights.

Seedream 5.0 Pro, the tier served here, is positioned as a region-precise editor. Given a base image and a text instruction, it localises the edit to the described element (an object, a garment, a piece of text, a background region) and preserves identity, lighting and composition elsewhere, which is the failure mode of most prompt-based editors. Up to ten `image_urls` can be supplied; the first is the image being edited and the rest act as references for style, subject or product appearance.

The hosted endpoint requires `prompt` and `image_urls`; `image_size` allows total pixels between 1024×1024 and 2048×2048 at any aspect ratio from 1:16 to 16:1, and `num_images` runs several independent generations so you can pick the best. Each run returns one or more image URLs. As with any instruction-based editor, results are best when the prompt names the target concretely ("the blue mug on the left") and states what must not change.

The endpoint used by this client is `bytedance/seedream-5-pro-edit`, which is ByteDance's Seedream 5.0 Pro model served on Synexa. Because Seedream weights are not public, there is no self-hosting option; the official project page is at https://seed.bytedance.com/en/seedream.

**Official project:** https://seed.bytedance.com/en/seedream

## Use cases

- **Product colourway variants** — call `run({"prompt": "change the sofa fabric to navy blue", "image_urls": [hero]})` once per colour to build a full variant set from one studio photo.
- **Background replacement for listings** — instruct "replace the background with a plain white studio backdrop" and keep the product, its shadow and its reflections intact.
- **Localised marketing creatives** — edit the on-image headline ("change the text on the banner to 'Summer Sale'") across a set of campaign images without a designer re-exporting each one.
- **Virtual try-on and styling** — pass the model photo first in `image_urls` and a garment reference second, with a prompt that puts the garment on the subject.
- **Retouching at scale** — remove distracting objects, fix a logo or swap a prop across thousands of user-generated images submitted with `wait=False` and a `webhook`.
- **Design iteration** — set `num_images` to 4 and let a reviewer choose between candidate edits in an internal tool.

## FAQ

**Is there a Seedream API?**

ByteDance offers Seedream through its own cloud platforms, which require platform accounts. This package is an independent Python client for the `bytedance/seedream-5-pro-edit` endpoint hosted on Synexa, which serves Seedream 5.0 Pro behind an HTTPS API with per-run billing.

**How much does the Seedream API cost?**

The hosted endpoint is billed at $0.0675 per run. Billing is per prediction with no subscription or idle charge, and new Synexa accounts receive a free trial credit.

**Can I run Seedream without a GPU?**

Yes, and there is no other way: Seedream weights are not released, so it always runs on the provider's hardware. With this client your code needs only Python 3.8+, `httpx` and network access.

**Does this client work with ComfyUI or open-source editing models?**

No. It is an HTTP client for the hosted Seedream endpoint and does not load local checkpoints or ComfyUI workflows. If you need an open editing model you can run yourself, look at FLUX.1 Kontext or similar projects; this client can also call hosted alternatives on Synexa by passing a different `model`.

**What input formats does it accept?**

`prompt` (string) and `image_urls` (a list of publicly reachable `.jpg`, `.png` or `.webp` URLs, up to 10, first one being the image to edit) are required. Optional fields are `image_size` (total pixels between 1024×1024 and 2048×2048, aspect ratio between 1/16 and 16), `num_images` (integer) and `output_format`. Output is one or more image URLs.

**Is this the official Seedream SDK?**

No. This is an independent, MIT-licensed client and is not affiliated with ByteDance. The official project page is https://seed.bytedance.com/en/seedream.

## Related

- [Seedream at ByteDance Seed](https://seed.bytedance.com/en/seedream) — official model page and technical reports.
- [Synexa Python client](https://github.com/synexa-ai/synexa-python) — the general-purpose client for every model on the platform.
- [black-forest-labs/flux-kontext-pro](https://synexa.ai/explore/black-forest-labs/flux-kontext-pro) — instruction-based editing from Black Forest Labs, a common comparison point.
- [black-forest-labs/flux-2-klein-9b](https://synexa.ai/explore/black-forest-labs/flux-2-klein-9b) — open-weights image-to-image with up to five references.
- [bytedance/seedvr2-upscale](https://synexa.ai/explore/bytedance/seedvr2-upscale) — upscale the edited result for print or large displays.

## License

MIT. This is an independent, community-maintained client and is not affiliated with or endorsed by the authors of Seedream. Model weights and trademarks belong to their respective owners.



_Last reviewed: 2026-09-22_
