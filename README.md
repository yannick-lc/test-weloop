# Test weloop.ai

![Python version](https://img.shields.io/badge/python-v3.10-blue)
![Platform version](https://img.shields.io/badge/platform-ubuntu-purple)

**Author**: Yannick Le Cacheux

This is a demo of a simple tool that enables a user to ask questions to a model, which then looks for an answer in a given set of documents. It may also ask follow-up questions if necessary.
The tools enables to later obtain a summary of conversations.

Example of a conversation between the user and the model<sup>[[1](#note1)]</sup>:

<pre style="background-color: black; color: white; font-family: monospace; white-space: pre-wrap;"><code><span style="color: #777777;">> Bonjour, en quoi puis-je vous aider ?</span>
> Comment changer la couleur de l'interface utilisateur ?
<span style="color: #777777;">> Vous pouvez changer la couleur de l'interface utilisateur en accédant à votre espace de travail Weloop, puis en vous rendant dans le module "Customize". Ensuite, vous pourrez configurer l'interface utilisateur selon les besoins d'identité visuelle du projet ou de l'entreprise. Est-ce que cela répond à votre question ?</span>
> oui
<span style="color: #777777;">> Parfait ! N'hésitez pas à revenir vers moi si vous avez d'autres questions.</span>
> ok
<span style="color: #777777;">> Au revoir, bonne fin de journée !</span>
</code></pre>

See section [Examples](#examples) for more samples of conversations and summaries.

<sub>[1]: <a id="note1"></a>Unfortunately, Github's Markdown version does not support custom colors or line wraps in code sections. For better readability, it is thus advised to look at this (and the other) example(s) in a different Markdown viewer.</sub>

## Install

Clone the repo and `cd` into the corresponding folder:
```bash
git clone git@github.com:yannick-lc/test-weloop.git
cd test-weloop
```

Create a Python environment (e.g. using conda) and install requirements:
```bash
conda create -n weloop python=3.10
conda activate weloop
pip install -r requirements.txt
pip install -e .
```

If you don't alreay have one, obtain an [API key](https://openai.com/blog/openai-api) for OpenAI.

## Run

Set your [OpenAI API key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key) as an environment variable to be able to query the model:
```bash
export OPENAI_API_KEY="your-api-key"
```

To start a conversation and ask questions to the model:
```bash
weloopai chat
```

To have a summary of the latest conversation:
```bash
weloopai summary
```

To refresh the model's knowledge with additional file (by default, `.txt` files located in `data/knowledge/documents`):
```bash
weloopai store
```

See section [Examples](#examples) for samples of conversations and summaries.

## Overview

### General approach: Retrieval-Augmented Generation

The approach is based on a standard Retrieval-Augmented Generation (RAG) pipeline:

Documents that contain knowledge to be used by the model are embedded as vectors, so that semantic similarity can be performed.
Then, when the user asks a questions, the question is embedded to retrieve the top-K document extracts most relevant to the query.

Text extracts are then integrated into the prompt, and a Large Language Model (LLM) is asked whether or not then contain the answer to the question, and to provide an answer in the former case.

A follow-up conversation with the LLM may then take place if necessary.

> [!note]
> The advantages of this approach are that it is:
> - Flexible: embedding functions, LLMs, prompts etc can all be changed easily to improve performance, reduce cost etc.
> - Scalable: it can be seemlessly scaled to thousands of documents.
> - Standard: it is well-known among AI practicioners and relies on well-maintained libraries, so that maintenance of the software is easy.

### Specificities of this use case

Since there are two tasks in this use case (answering a question, and summarizing a text), 2 system prompts are used: one for answering question, and one for producing summaries.

### Implementation details and hyper-parameters

Implementation was done mostly using Langchain, as it allows to easily implement RAG pipeline.

GPT3.5 was used as the default LLM, because it is easy to integrate (only requires API calls) its performance is OK and its cost reasonable.
(it would be of course easy to upgrade to GPT4 for better performance, but it would be more costly).
The LLM used for summary and chat is the same for now, but it could easily be changed.

Similarly, OpenAI embeddings were used (corresponding to `text-embedding-ada-002`).

Temperature of the LLM was set to 0 to produce reproducible answers, more likely to be correct.

Documents are short so no splitting is necessary for embedding.

2 documents were (and are) retrieved per search to limit the number of tokens used during tests, which seemed to be enough.

## Limits of the approach and possible improvements

This section describes improvements that could be made to the AI.

As of now, the AI retrieves documents only after the first question. A better approach would be:
- After a question is asked, determine whether a document search is useful to answer using a LLM and prompts hidden to the user
- If documents are indeed useful, perform a semantic similarity search to retrieve documents, and prompt the AI to find useful information in the corresponding text.
- Finally, answer to the user.
- Repeat for each question.

However, this approach takes longer to implement, and may be more costly as more tokens are being used for each query.

A similar techique may also be applied to determine whether the conversation should be ended, or more follow-up questions should be asked.

It may also be useful to return the "raw" documents that were used to answer a question to the user.


Limits: for now, dependent on external API (OpenAI).
Tendancy to introduce breaking changes (deprecate models, change API etc).
Also, limits of used embeddings and LLM obviously

Quite obviously, many other aspects may be improved, such as:
- Use different LLMs, embeddings etc to improve performance (e.g. GPT4, although it is much more costly)
- If necessary (e.g. for cost, confidentiality or maintainability reasons), an open-source LLM operating on-premise (e.g. Llama v2) may be used instead
- Use more advanced techniques for document retrieval: document reranking, hypothetical document embedding (https://arxiv.org/abs/2212.10496) etc
- Prompts used for now were crafted fairly quickly and only lightly tested, so it is certain that better prompts could be engineered.
- In particular, it would very probably be useful to use an approach based on few shot learning.
- ...

Finally, to improve performance, more tests should be conducted.
Additional tests would also be required to ensure the model is safe and reasonably resilient to malicious prompt injections.


## Industrialization

The following tasks (not related to the AI itself) should be done to industrialize the model:
- Serve the model with an API (e.g. using LangServe, Flask...)
- Add unit tests
- Make the configuration more flexible, by using environment variables to define where knowledge is stored etc
- Set up a database to store and retrieve conversations instead of simple files
- Package using Docker
- Configure logging, add monitoring to the model in production etc
- ...



## Examples

### Exemple 1
> Comment changer la couleur de l'interface utilisateur ?

Pour cette question, la réponse se trouve dans les documents.

**Conversation**
```bash
$ weloopai chat
```
<!-- We need to use a custom style to display code as it is otherwise impossible to color code in markdown -->
<pre style="background-color: black; color: white; font-family: monospace; white-space: pre-wrap;"><code><span style="color: #777777;">> Bonjour, en quoi puis-je vous aider ?</span>
> Comment changer la couleur de l'interface utilisateur ?
<span style="color: #777777;">> Vous pouvez changer la couleur de l'interface utilisateur en accédant à votre espace de travail Weloop, puis en vous rendant dans le module "Customize". Ensuite, vous pourrez configurer l'interface utilisateur selon les besoins d'identité visuelle du projet ou de l'entreprise. Est-ce que cela répond à votre question ?</span>
> oui
<span style="color: #777777;">> Parfait ! N'hésitez pas à revenir vers moi si vous avez d'autres questions.</span>
> dac
<span style="color: #777777;">> Au revoir, bonne fin de journée !</span>
</code></pre>

**Résumé**
```bash
$ weloopai summary
```
<pre style="background-color: black; color: white; font-family: monospace; white-space: pre-wrap;"><code><span style="color: #777777;">> Résumé : L'utilisateur cherchait à savoir comment changer la couleur de l'interface utilisateur sur Weloop. Je lui ai expliqué qu'il pouvait le faire en accédant à son espace de travail Weloop, puis en se rendant dans le module "Customize" pour configurer l'interface selon les besoins d'identité visuelle du projet ou de l'entreprise. L'utilisateur a confirmé avoir compris et n'a pas posé d'autres questions.</span>
</code></pre>



### Exemple 2
> Comment synchroniser Weloop avec Jira ?

La réponse est implicitement dans les documents (Jira n'est pas mentionné mais des informations sont présentes pour "outil de ticketing").
L'utilisateur ne comprend pas les instructions.

**Conversation**
<pre style="background-color: black; color: white; font-family: monospace; white-space: pre-wrap;"><code><span style="color: #777777;">> Bonjour, en quoi puis-je vous aider ?</span>
> Comment synchroniser Weloop avec Jira ?
<span style="color: #777777;">> La synchronisation de Weloop avec Jira se fait en accédant à vos paramètres de profil, puis en sélectionnant Jira dans la section "Ticketing" et en ajoutant le TOKEN de votre compte Jira. Est-ce que cela répond à votre question ?</span>
> non, je ne trouve pas les paramètres de profil       
<span style="color: #777777;">> Je suis désolé, je n'ai pas d'informations sur l'emplacement spécifique des paramètres de profil dans Weloop. Pourriez-vous me dire quelle version de Weloop vous utilisez et si vous accédez à la plateforme via un navigateur web ou une application mobile ?</span>
> la version 375
<span style="color: #777777;">> Merci pour cette information. Pourriez-vous me décrire les étapes que vous suivez actuellement pour accéder aux paramètres de profil dans Weloop ?</span>
> bah je peux pas justement
<span style="color: #777777;">> Je transmettrai ces informations au support technique. Ils pourront vous aider à trouver l'emplacement des paramètres de profil dans la version 375 de Weloop. Au revoir, bonne fin de journée !</span>
</code></pre>

**Résumé**
<pre style="background-color: black; color: white; font-family: monospace; white-space: pre-wrap;"><code><span style="color: #777777;">> L'utilisateur rencontre des difficultés pour trouver l'emplacement des paramètres de profil dans la version 375 de Weloop. Il a mentionné qu'il ne parvient pas à accéder à ces paramètres.</span>
</code></pre>


### Exemple 3
> Comment enregistrer les feedbacks au format word ?

La réponse n'est pas dans les documents.

**Conversation**
<pre style="background-color: black; color: white; font-family: monospace; white-space: pre-wrap;"><code><span style="color: #777777;">> Bonjour, en quoi puis-je vous aider ?</span>
> Comment enregistrer les feedbacks au format ded word ?
<span style="color: #777777;">> Je n'ai pas d'informations sur l'enregistrement de feedbacks au format Word. Pourriez-vous me donner plus de détails sur le processus que vous souhaitez effectuer ?</span>
> J'ai des feedbacks dans l'outil, j'aimerais tous les exporter au format word
<span style="color: #777777;">> Je n'ai pas d'informations sur l'exportation de feedbacks au format Word. Avez-vous la possibilité d'exporter les feedbacks dans un autre format depuis l'outil ? Avez-vous envisagé d'utiliser un autre type de fichier pour stocker ces feedbacks ?</span>
> non, juste copier-coller mais c'est pas pratique
<span style="color: #777777;">> Je transmettrai ces informations au support technique. Ils pourront étudier la possibilité d'ajouter une fonctionnalité d'exportation au format Word dans l'outil. Au revoir, bonne fin de journée !</span>
</code></pre>

**Résumé**
<pre style="background-color: black; color: white; font-family: monospace; white-space: pre-wrap;"><code><span style="color: #777777;">> L'utilisateur souhaite exporter des feedbacks depuis l'outil vers un format Word, car le copier-coller n'est pas pratique. Il n'a pas trouvé de fonctionnalité d'exportation dans l'outil et n'a pas envisagé d'utiliser un autre type de fichier pour stocker les feedbacks.</span>
</code></pre>



### Exemple 4
> Peut-on créer des tags si on n'est pas administrateur ?

La réponse n'est pas explicite, mais les documents sous-entendent que non.

**Conversation**
<pre style="background-color: black; color: white; font-family: monospace; white-space: pre-wrap;"><code><span style="color: #777777;">> Bonjour, en quoi puis-je vous aider ?</span>
> Peut-on créer des tags si on n'est pas administrateur ?
<span style="color: #777777;">> En tant qu'administrateur, vous pouvez créer des tags en accédant au module Settings --> Général --> TAGS lors de la configuration de votre espace de travail. Cela répond-il à votre question ?</span>
> non, je ne suis pas administrateur. Est-ce que je peux quand même créer des tags ?
<span style="color: #777777;">> Je n'ai pas d'information sur ce sujet. Pouvez-vous me dire dans quel contexte vous souhaitez créer des tags et quel est votre rôle dans cette situation ?</span>
> j'ai un rôle de floppeur, j'aimerais créer des tags pour bifurquer les quaternions
<span style="color: #777777;">> Merci pour ces précisions. Je vais transmettre ces informations au support technique. Ils pourront vous aider à trouver une solution adaptée à votre besoin.</span>
> ok merci
<span style="color: #777777;">> Au revoir, bonne fin de journée !</span>
</code></pre>

**Résumé**
<pre style="background-color: black; color: white; font-family: monospace; white-space: pre-wrap;"><code><span style="color: #777777;">> L'utilisateur a demandé s'il était possible de créer des tags sans être administrateur. Il a précisé qu'il occupait un rôle de "floppeur" et souhaitait créer des tags pour bifurquer les quaternions. Il a confirmé qu'il n'était pas administrateur et a exprimé son besoin de créer des tags dans ce contexte.</span>
</code></pre>



### Exemple 5
> Que mangent les tigres ?

La réponse ne se trouve pas dans les documents.

**Conversation :**
<pre style="background-color: black; color: white; font-family: monospace;white-space: pre-wrap;"><code><span style="color: #777777;">> Bonjour, en quoi puis-je vous aider ?</span>
> Que mangent les tigres ?
<span style="color: #777777;">> Je n'ai pas d'information sur les tigres. Quel type de renseignement cherchez-vous exactement ? Que mangent les tigres dans leur habitat naturel ou en captivité ?</span>
> captivité, c'est pour mon tigre nommé Gérard
<span style="color: #777777;">> Je n'ai pas d'information sur les besoins alimentaires spécifiques des tigres en captivité. Pouvez-vous me dire ce que vous donnez actuellement à Gérard et si vous avez des préoccupations particulières concernant son alimentation ?</span>
> je lui donne des haricots verts, mais je suis pas sûr qu'il aime ça
<span style="color: #777777;">> Je transmettrai ces informations au support technique pour obtenir des conseils sur l'alimentation appropriée pour Gérard. Merci de m'avoir fourni ces détails. Au revoir, bonne fin de journée !</span>
</code></pre>

**Résumé**
<pre style="background-color: black; color: white; font-family: monospace;white-space: pre-wrap;"><code><span style="color: #777777;">> L'utilisateur a mentionné donner des haricots verts à son tigre en captivité, nommé Gérard, mais n'est pas sûr que cela lui convienne. Il cherche des conseils sur l'alimentation appropriée pour son animal.</span>
</code></pre>


## Bibliography

TODO