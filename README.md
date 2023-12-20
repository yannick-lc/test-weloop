# test-weloop
Technical test for Weloop.ai

## Install

```bash
conda create -n weloop python=3.10
conda activate weloop
pip install -r requirements.txt
pip install -e .
```

OpenAI API key

## Run

To start a conversation and ask questions to the model:
```bash
weloop chat
```

To have a summary of the last conversation:
```bash
weloop summary
```

## Improvements / TODO

Docker
Unit tests
Config: use env variables to select where knowledge is stored etc
Use a database to store and retrieve conversations
