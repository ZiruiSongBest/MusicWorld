# MusicWorld
Project for UTS 41129 Software Innovation Studio - Spring 2024

Team 17: CCF-A  

Team member:Hanyang Tan, Zirui Song, Yaohang Li, Yuxuan Ji, Zhishuo Li  

# Music Generation
Our demo could be seen in [wav](./stable-audio-tools/hammer.wav), which is a demo with "The sound of a hammer hitting a wooden surface."


# Installation Guide

First clone our repo and go to the directory. then initialize submodules.

```bash
git submodule update --init --recursive
```

To install the backend Python environment, we suggest using `conda` to manage the environment.

```bash
conda create -n musicworld python=3.10 -y
conda activate musicworld

cd stable-audio-tools
pip install -e .
cd ..
pip install -r requirements.txt
```

# Run the demo

In the directory music-world-apis

```bash
python main.py
```