# Astrological Introspection

This Django app calculates **tropical zodiac, whole-sign houses** and offers a
source-grounded chat guide using approved traditional Jyotisha texts only. It
intentionally does not mix in sidereal recalculations, nakshatras, or dashas.
Traditional Jyotisha texts do not establish that ancient authors prescribed
tropical astrology; the app applies Jyotisha concepts to tropical placements
as a clearly labeled modern adaptation.

On the chart page, select a planet or (when birthplace and birth time are
known) an angle to expand an AI-written plain-language summary. The approved
traditional source is listed once at the bottom of the chart page. In the
question box, Enter sends the message and Shift+Enter inserts a new line.

Birth time without a selected birthplace is used as a UTC approximation for
planetary positions only. Houses and angles require both a birthplace and a
birth time; without a birthplace, a sign-change notice flags planets whose
sign may be uncertain.

Planet summaries distinguish traditional Jyotisha sign conditions (own sign,
exaltation, or debilitation) from house placement. In traditional astrology,
the angular houses (1st, 4th, 7th, and 10th) indicate a separate kind of
prominence; a house does not itself change a planet's sign-based condition.

New charts are held in the current browser session and are not stored as
permanent chart records. Optionally select **Save my chart details in this
browser** to keep the birth details on that device and restore the chart later.
Generated placement summaries are cached in the same browser when this option
is enabled. This browser cache is not synced or encrypted; anyone using that
browser profile can restore it. Use **Clear saved chart from this browser** on
the chart page (or clear the site data in the browser) to remove it. Existing
private links created by an earlier version remain available.

## Free AI setup

The default configuration uses [Ollama](https://ollama.com/) locally. Ollama
and the `llama3.2:3b` model are free to run on your own computer; no model API
key or per-message billing is required:

```text
ollama pull llama3.2:3b
copy .env.example .env
python manage.py migrate
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
