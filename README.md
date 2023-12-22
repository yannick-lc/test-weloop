# Test weloop.ai

![Python version](https://img.shields.io/badge/python-v3.10-blue)
![Platform version](https://img.shields.io/badge/platform-ubuntu-purple)

**Author**: Yannick Le Cacheux

This is a simple demo of a tool...

<pre style="background-color: black; color: white; font-family: monospace;"><code>
> Bonjour, en quoi puis-je vous aider ?
<span style="color: #3388FF;">> Comment changer la couleur de l'interface utilisateur ?</span>
> Je cherche la réponse à votre question... Vous pouvez changer la couleur de l'interface utilisateur en accédant à votre espace de travail Weloop, puis en vous rendant dans le module "Customize". Ensuite, vous pourrez configurer l'interface utilisateur selon les besoins d'identité visuelle du projet ou de l'entreprise. Est-ce que cela répond à votre question ?
<span style="color: #3388FF;">> oui</span>
> Parfait ! N'hésitez pas à revenir vers moi si vous avez d'autres questions.
<span style="color: #3388FF;">> dac</span>
> Au revoir, joyeuses fêtes de fin d'année !
</code></pre>

See section [Examples](#examples) for more samples of conversations and summaries.

## Install

After cloning the repo, create a Python environment (e.g. using conda) and install requirements:
```bash
conda create -n weloop python=3.10
conda activate weloop
pip install -r requirements.txt
pip install -e .
```

## Run

Set your [OpenAI API key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key) as an environment variable to be able to query the model:
```bash
export OPENAI_API_KEY="your-api-key"
```

To start a conversation and ask questions to the model:
```bash
weloop chat
```

To have a summary of the latest conversation:
```bash
weloop summary
```

To refresh the model's knowledge with additional file (by default, `.txt` files located in `data/knowledge/documents`):
```bash
weloop store
```

See section [Examples](#examples) for samples of conversations and summaries.

## Overview

## Improvements

Unit tests

Serve with API (e.g. using LangServe)
Docker
Config: use env variables to select where knowledge is stored etc
Use a database to store and retrieve conversations, use a more human readable format

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

LLM for summary and chat are the same for now, but could be changed

Documents are short so no splitting is necessary for embedding

Limits: for now, dependent on external API (OpenAI).
Tendancy to introduce breaking changes (deprecate models, change API etc).
Also, limits of used embeddings and LLM obviously

For now and to limit consumption of resources, we only try to look for answers after the first question.
Ideally, we would want to first check if question asked requires to look for documents, retrieve documents if relevant,
and then answer question.
Make it more resilient to malicious prompt injections, monitor usage / set up limits etc.

Check if conv is finished.

System prompt is different
LLM is same but might be changed

## Misc

packages: langchain + hub, chromadb, openai, tiktoken, langchainhub, ipykernel (for notebooks), unstructured



## Examples

### Exemple 1
> Comment changer la couleur de l'interface utilisateur ?

Pour cette question, la réponse se trouve dans les documents.

**Conversation**
```bash
$ weloopai chat
```
<!-- We need to use a custom style to display code as it is otherwise impossible to color code in markdown -->
<pre style="background-color: black; color: white; font-family: monospace;"><code><span style="color: #777777;">> Bonjour, en quoi puis-je vous aider ?</span>
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
<pre style="background-color: black; color: white; font-family: monospace;"><code><span style="color: #777777;">> Résumé : L'utilisateur cherchait à savoir comment changer la couleur de l'interface utilisateur sur Weloop. Je lui ai expliqué qu'il pouvait le faire en accédant à son espace de travail Weloop, puis en se rendant dans le module "Customize" pour configurer l'interface selon les besoins d'identité visuelle du projet ou de l'entreprise. L'utilisateur a confirmé avoir compris et n'a pas posé d'autres questions.</span>
</code></pre>



### Exemple 2
> Comment synchroniser Weloop avec Jira ?

La réponse est implicitement dans les documents (Jira n'est pas mentionné mais des informations sont présentes pour "outil de ticketing").
L'utilisateur ne comprend pas les instructions.

**Conversation**
<pre style="background-color: black; color: white; font-family: monospace;"><code><span style="color: #777777;">> Bonjour, en quoi puis-je vous aider ?</span>
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
<pre style="background-color: black; color: white; font-family: monospace;"><code><span style="color: #777777;">> L'utilisateur rencontre des difficultés pour trouver l'emplacement des paramètres de profil dans la version 375 de Weloop. Il a mentionné qu'il ne parvient pas à accéder à ces paramètres.</span>
</code></pre>


### Exemple 3
> Comment enregistrer les feedbacks au format word ?

La réponse n'est pas dans les documents.

**Conversation**
<pre style="background-color: black; color: white; font-family: monospace;"><code><span style="color: #777777;">> Bonjour, en quoi puis-je vous aider ?</span>
> Comment enregistrer les feedbacks au format ded word ?
<span style="color: #777777;">> Je n'ai pas d'informations sur l'enregistrement de feedbacks au format Word. Pourriez-vous me donner plus de détails sur le processus que vous souhaitez effectuer ?</span>
> J'ai des feedbacks dans l'outil, j'aimerais tous les exporter au format word
<span style="color: #777777;">> Je n'ai pas d'informations sur l'exportation de feedbacks au format Word. Avez-vous la possibilité d'exporter les feedbacks dans un autre format depuis l'outil ? Avez-vous envisagé d'utiliser un autre type de fichier pour stocker ces feedbacks ?</span>
> non, juste copier-coller mais c'est pas pratique
<span style="color: #777777;">> Je transmettrai ces informations au support technique. Ils pourront étudier la possibilité d'ajouter une fonctionnalité d'exportation au format Word dans l'outil. Au revoir, bonne fin de journée !</span>
</code></pre>

**Résumé**
<pre style="background-color: black; color: white; font-family: monospace;"><code><span style="color: #777777;">> L'utilisateur souhaite exporter des feedbacks depuis l'outil vers un format Word, car le copier-coller n'est pas pratique. Il n'a pas trouvé de fonctionnalité d'exportation dans l'outil et n'a pas envisagé d'utiliser un autre type de fichier pour stocker les feedbacks.</span>
</code></pre>



### Exemple 4
> Peut-on créer des tags si on n'est pas administrateur ?

La réponse n'est pas explicite, mais les documents sous-entendent que non.

**Conversation**
<pre style="background-color: black; color: white; font-family: monospace;"><code><span style="color: #777777;">> Bonjour, en quoi puis-je vous aider ?</span>
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
<pre style="background-color: black; color: white; font-family: monospace;"><code><span style="color: #777777;">> L'utilisateur a demandé s'il était possible de créer des tags sans être administrateur. Il a précisé qu'il occupait un rôle de "floppeur" et souhaitait créer des tags pour bifurquer les quaternions. Il a confirmé qu'il n'était pas administrateur et a exprimé son besoin de créer des tags dans ce contexte.</span>
</code></pre>



### Exemple 5
> Que mangent les tigres ?

La réponse ne se trouve pas dans les documents.

**Conversation :**
```
> Bonjour, en quoi puis-je vous aider ?
> Que mangent les tigres ?
> Je cherche la réponse à votre question... Je n'ai pas d'information sur les tigres. Quel type de renseignement cherchez-vous exactement ? Que mangent les tigres dans leur habitat naturel ou en captivité ?
> captivité, c'est pour mon tigre nommé Gérard
> Je n'ai pas d'information sur les besoins alimentaires spécifiques des tigres en captivité. Pouvez-vous me dire ce que vous donnez actuellement à Gérard et si vous avez des préoccupations particulières concernant son alimentation ?
> je lui donne des haricots verts, mais je suis pas sûr qu'il aime ça
> Je transmettrai ces informations au support technique pour obtenir des conseils sur l'alimentation appropriée pour Gérard. Merci de m'avoir fourni ces détails. Au revoir, bonne fin de journée !
```

**Résumé**
<pre style="background-color: black; color: white; font-family: monospace;"><code><span style="color: #777777;">> L'utilisateur a mentionné donner des haricots verts à son tigre en captivité, nommé Gérard, mais n'est pas sûr que cela lui convienne. Il cherche des conseils sur l'alimentation appropriée pour son animal.</span>
</code></pre>


## Bibliography

TODO