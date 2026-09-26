# Astrological Introspection

This Django app calculates **tropical zodiac, whole-sign houses** and offers a
source-grounded chat guide. It intentionally does not mix in sidereal zodiac,
nakshatras, or dashas.

## Free AI setup

The default configuration uses [Ollama](https://ollama.com/) locally. Ollama
and the `llama3.2:3b` model are free to run on your own computer; no model API
key or per-message billing is required:

```text
ollama pull llama3.2:3b
copy .env.example .env
ollama serve
python manage.py runserver
```

The server sends chart facts, the approved source catalog in
`shared/sources.json`, and bounded chat history to the model. It never sends
the user's name or raw birth location to the model.

For a hosted model, set `AI_BASE_URL`, `AI_API_KEY`, and `AI_MODEL` to an
OpenAI-compatible provider. “Free” hosted inference is subject to that
provider's quota and terms; the local Ollama path is the only no-billing
option this project can guarantee.

## Free HTTPS deployment

`render.yaml` describes a Render free web service. Render provides a free
`onrender.com` subdomain and managed HTTPS certificate automatically. Deploy
from the repository using Render Blueprint, then set `GEOAPIFY_API_KEY` and a
hosted `AI_BASE_URL`/`AI_API_KEY` in the dashboard if chat must work while
hosted. A local Ollama server cannot be reached from Render.

A custom registrable domain is not normally free. If you later buy one,
attach it in Render and use its automatic certificate, or put it behind
Cloudflare's free DNS/proxy. Do not upload certificate private keys to this
repository.
