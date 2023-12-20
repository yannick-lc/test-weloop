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

## TODO

Unit tests
Update data knowledge
Examples

## Improvements

Serve with API (e.g. using LangServe)
Docker
Config: use env variables to select where knowledge is stored etc
Use a database to store and retrieve conversations

AI: reranking etc
Hypothetical document embedding https://arxiv.org/abs/2212.10496

Return source documents

Better prompt engineering ofc (and few-shot learning)

## General doc and discussion

Built with RAG and Langchain (link)
RAG because scalable
Langchain because easy to deploy

Details of RAG pipeline:
OpenAIEmbedding (Ada?) for embeddings
GPT3.5 by default as LLM, because easy to integrate and perf OK
(easy to upgrade to GPT4 for better perf (but more costly))
Temperature of 0 because...

LLM prompt for retrieval: French translation of "standard" prompt for retrieval

Documents are short so no splitting is necessary for embedding

Limits: for now, dependent on external API (OpenAI).
Tendancy to introduce breaking changes (deprecate models, change API etc).
Also, limits of used embeddings and LLM obviously

For now and to limit consumption of resources, we only try to look for answers after the first question.
Ideally, we would want to first check if question asked requires to look for documents, retrieve documents if relevant,
and then answer question.
Make it more resilient to malicious prompt injections, monitor usage / set up limits etc.

Check if conv is finished.

## Misc

packages: langchain + hub, chromadb, openai, tiktoken, langchainhub, ipykernel (for notebooks), unstructured

## Exemples de questions :

