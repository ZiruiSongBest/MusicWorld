# stable-audio-tools
Training and inference code for audio generation models

# Install

The library can be installed from PyPI with:
```bash
$ pip install stable-audio-tools
```

To run the training scripts or inference code, you'll want to clone this repository, navigate to the root, and run:
```bash
$ pip install .
```

# Requirements
Requires PyTorch 2.0 or later for Flash Attention support

Development for the repo is done in Python 3.8.10

# Interface

A basic Gradio interface is provided to test out trained models. 

For example, to create an interface for the [`stable-audio-open-1.0`](https://huggingface.co/stabilityai/stable-audio-open-1.0) model, once you've accepted the terms for the model on Hugging Face, you can run:
```bash
$ python3 ./run_gradio.py --pretrained-name stabilityai/stable-audio-open-1.0
```

The `run_gradio.py` script accepts the following command line arguments:

- `--pretrained-name`
  - Hugging Face repository name for a Stable Audio Tools model
  - Will prioritize `model.safetensors` over `model.ckpt` in the repo
  - Optional, used in place of `model-config` and `ckpt-path` when using pre-trained model checkpoints on Hugging Face
- `--model-config`
  - Path to the model config file for a local model
- `--ckpt-path`
  - Path to unwrapped model checkpoint file for a local model
- `--pretransform-ckpt-path` 
  - Path to an unwrapped pretransform checkpoint, replaces the pretransform in the model, useful for testing out fine-tuned decoders
  - Optional
- `--share`
  - If true, a publicly shareable link will be created for the Gradio demo
  - Optional
- `--username` and `--password`
  - Used together to set a login for the Gradio demo
  - Optional
- `--model-half`
  - If true, the model weights to half-precision
  - Optional



