# Génération d'une API key

```python
import secrets, hashlib
raw = secrets.token_urlsafe(32)
key_prefix = raw[:8]
key_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
print(raw)
print(key_prefix)
print(key_hash)
```
