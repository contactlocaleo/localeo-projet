# F04 - Limites des corps HTTP

La pile compatible FastAPI 0.136.0 / Starlette 1.3.1 conserve SQLAdmin 0.29.0.
Starlette 1.3.1 corrige [CVE-2026-54283](https://github.com/Kludex/starlette/security/advisories/GHSA-82w8-qh3p-5jfq).

Avant tout parsing, le corps de `/admin/login` est limite a 16 Kio et les autres
corps HTTP a 8 Mio (limite globale, fichiers et enveloppe multipart compris).
Les limites metier d'upload, plus petites, restent applicables. Un depassement
renvoie 413, un Content-Length ambigu/invalide 400. Les octets sont comptes
meme sans Content-Length ou lorsque celui-ci sous-estime le corps.
Le proxy doit egalement borner la duree de reception et les connexions lentes.
