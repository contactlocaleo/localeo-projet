"""Compare scoped consumer operations and their reachable schemas, offline.

Annotations may differ. Operations outside the declared consumer scopes never
participate. Request/response types, required fields, enums and status codes do.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

METHODS = {'get', 'post', 'put', 'patch', 'delete', 'head', 'options'}
ANNOTATIONS = {'description', 'summary', 'title', 'example', 'examples', 'tags', 'externalDocs'}
SCOPES = {
    'commercant': ('../localeo-commercant/api/localeo-openapi.json', (
        '/protected/animation-locale/commercants/me', '/protected/facturation',
        '/protected/gestion-prestations', '/protected/identite-acces/commercants',
        '/protected/gestion-commercants')),
    'animation': ('../localeo-animation/src/imports/openapi.json', (
        '/protected/animation-locale', '/public/identite-acces/animation',
        '/protected/referencement/commercants-animation', '/protected/referencement/imports-commercants',
        '/protected/identite-acces/animation', '/public/credits-achat-b2b')),
}


def normalize(value, key=None):
    if isinstance(value, dict):
        # Property/enum names can themselves be "title" or "description".
        return {name: normalize(child, name) for name, child in value.items()
                if key in {'properties', 'schemas', 'responses', 'headers'} or name not in ANNOTATIONS}
    if isinstance(value, list):
        items = [normalize(child) for child in value]
        return sorted(items, key=lambda item: json.dumps(item, sort_keys=True)) if key in {'required', 'enum'} else items
    return value


def projection(document, operations):
    result, pending, seen = {}, [], set()
    def visit(value):
        if isinstance(value, dict):
            if '$ref' in value:
                pending.append(value['$ref'])
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)
    for path, method in operations:
        operation = document['paths'][path][method]
        # OpenAPI permits shared parameters on the path item.
        item = {'operation': operation, 'parameters': document['paths'][path].get('parameters', [])}
        result[f'{method.upper()} {path}'] = normalize(item)
        visit(item)
    while pending:
        ref = pending.pop()
        if ref in seen:
            continue
        seen.add(ref)
        if not ref.startswith('#/'):
            raise ValueError(f'External reference unsupported: {ref}')
        value = document
        for segment in ref[2:].split('/'):
            value = value[segment.replace('~1', '/').replace('~0', '~')]
        result[ref] = normalize(value)
        visit(value)
    return result


def compare(producer, consumer, prefixes):
    operations = [(path, method) for path, item in consumer['paths'].items()
                  if any(path == prefix or path.startswith(prefix + '/') for prefix in prefixes)
                  for method in item if method in METHODS]
    if not operations:
        raise ValueError('No consumer operations in declared scope')
    missing = [f'{method.upper()} {path}' for path, method in operations
               if method not in producer['paths'].get(path, {})]
    if missing:
        return len(operations), missing
    left, right = projection(producer, operations), projection(consumer, operations)
    return len(operations), sorted(key for key in left.keys() | right.keys() if left.get(key) != right.get(key))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    producer = json.loads((args.root / 'docs/specifications/epic-41-api/openapi.json').read_bytes())
    failed = False
    for name, (filename, prefixes) in SCOPES.items():
        consumer = json.loads((args.root / filename).read_bytes())
        count, differences = compare(producer, consumer, prefixes)
        print(f'{name}: {count} scoped operations, {len(differences)} semantic differences')
        for difference in differences:
            print('  ' + difference)
        failed |= bool(differences)
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
