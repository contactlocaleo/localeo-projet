#!/usr/bin/env python3
"""Check local Markdown links in Git-visible Localeo guidance, without network access.

Normal mode uses tracked and non-ignored untracked files. Staged mode reads all
guidance from each selected repository's index and checks destinations inside
that repository against the index too; neighbouring repositories use disk.
--changed selects changed guidance plus guidance linking to deleted paths.
Anchors, external URLs, absolute web/API paths and example code are not checked.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import html
import json
import os
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit


APPLICATIONS = ("localeo-backend", "localeo-animation", "localeo-commercant", "localeo-marketplace")
EXCLUDED_PARTS = frozenset({
    ".git", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", ".runtime", "dist", "build", "output", "tmp",
    "test-results", "playwright-report", ".lighthouseci", "coverage", "vendor",
})


@dataclass(frozen=True)
class Link:
    line: int
    destination: str | None
    reference: str | None = None


def _blank(text: str) -> str:
    return "".join("\n" if char == "\n" else " " for char in text)


def _without_code(text: str) -> str:
    lines = []
    fence = None
    for line in text.splitlines(keepends=True):
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
        if fence:
            lines.append(_blank(line))
            if match and match[1][0] == fence[0] and len(match[1]) >= len(fence) and not match[2].strip():
                fence = None
        elif match:
            fence = match[1]
            lines.append(_blank(line))
        else:
            lines.append(line)
    text = re.sub(r"<!--.*?-->", lambda match: _blank(match[0]), "".join(lines), flags=re.S)
    # A matching run of backticks closes an inline code span, even over a newline.
    return re.sub(r"(?<!`)(`+)(?!`)(.*?)(?<!`)\1(?!`)", lambda match: _blank(match[0]), text, flags=re.S)


def _label(text: str) -> str:
    return " ".join(html.unescape(text).split()).casefold()


def _destination(text: str, start: int) -> tuple[str, int] | None:
    if start >= len(text):
        return None
    if text[start] == "<":
        match = re.match(r"<((?:\\.|[^<>\n])*)>", text[start:])
        return (match[1], start + match.end()) if match else None
    depth = 0
    position = start
    while position < len(text):
        char = text[position]
        if char == "\\" and position + 1 < len(text):
            position += 2
            continue
        if char.isspace() or (char == ")" and depth == 0):
            break
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        position += 1
    if depth:
        return None
    return text[start:position], position


def markdown_links(markdown: str) -> list[Link]:
    """Extract inline and full/collapsed/shortcut reference links (and images)."""
    text = _without_code(markdown)
    definitions = {}
    spans = []
    for match in re.finditer(r"^ {0,3}\[([^\]\n]+)\]:[ \t]*(?:\n[ \t]*)?", text, flags=re.M):
        parsed = _destination(text, match.end())
        if parsed and parsed[0]:
            definitions.setdefault(_label(match[1]), parsed[0])
            end = text.find("\n", parsed[1])
            spans.append((match.start(), len(text) if end == -1 else end))
    for start, end in reversed(spans):
        text = text[:start] + _blank(text[start:end]) + text[end:]
    links = []
    position = 0
    while position < len(text):
        if text[position] == "\\":
            position += 2
            continue
        if text[position] != "[":
            position += 1
            continue
        start = position
        position += 1
        depth = 1
        while position < len(text) and depth:
            if text[position] == "\\":
                position += 2
                continue
            if text[position] == "[":
                depth += 1
            elif text[position] == "]":
                depth -= 1
            position += 1
        if depth:
            # An unmatched prose bracket must not hide later valid links.
            position = start + 1
            continue
        label = text[start + 1:position - 1]
        line = text.count("\n", 0, start) + 1
        if position < len(text) and text[position] == "(":
            cursor = position + 1
            while cursor < len(text) and text[cursor].isspace():
                cursor += 1
            parsed = _destination(text, cursor)
            if parsed:
                destination, end = parsed
                # An optional quoted/parenthesized title follows the destination.
                tail = re.match(r"\s*(?:\"(?:\\.|[^\"])*\"|'(?:\\.|[^'])*'|\((?:\\.|[^)])*\))?\s*\)", text[end:])
                if tail:
                    links.append(Link(line, destination))
                    position = end + tail.end()
        elif position < len(text) and text[position] == "[":
            end = text.find("]", position + 1)
            if end != -1:
                reference = _label(text[position + 1:end] or label)
                links.append(Link(line, definitions.get(reference), reference))
                position = end + 1
        elif _label(label) in definitions:
            links.append(Link(line, definitions[_label(label)], _label(label)))
    return links


def local_target(source: Path, destination: str) -> Path | None:
    destination = html.unescape(re.sub(r"\\([\\`*{}\[\]()#+\-.!_<> ])", r"\1", destination.strip()))
    if not destination or destination.startswith(("#", "/", "\\")) or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", destination):
        return None
    try:
        relative = unquote(urlsplit(destination).path)
    except ValueError:
        return None
    if not relative:
        return None
    return Path(os.path.abspath(source.parent / relative))


def _git(repo: Path, *arguments: str) -> bytes:
    result = subprocess.run(["git", "-C", str(repo), *arguments], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"})
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace").strip())
    return result.stdout


def _paths(repo: Path, *arguments: str) -> set[str]:
    return {item.decode("utf-8", errors="surrogateescape") for item in _git(repo, *arguments).split(b"\0") if item}


def _is_guidance(relative: str) -> bool:
    path = Path(relative)
    if EXCLUDED_PARTS.intersection(path.parts) or path.parts[:2] == ("demonstrations", "prive"):
        return False
    return path.name in {"AGENTS.md", "AGENT.md", "README.md"} or (
        path.name == "SKILL.md" and path.parts[0] == ".agents")


def _relative(path: Path, repo: Path) -> str | None:
    try:
        return path.relative_to(repo).as_posix()
    except ValueError:
        return None


def check_guidance(root: Path, repos: list[Path] | None = None, *, documents: list[Path] | None = None,
                   staged: bool = False, changed: bool = False) -> dict:
    root = Path(os.path.abspath(root))
    explicit_repos = repos is not None
    selected = repos if explicit_repos else [root, *(root.parent / name for name in APPLICATIONS)]
    result = {"mode": "staged" if staged else "working-tree", "changed_only": changed,
              "repositories": [], "checked_guides": 0, "checked_links": 0, "errors": [], "warnings": []}
    states = []
    for candidate in dict.fromkeys(Path(os.path.abspath(repo)) for repo in selected):
        if not candidate.is_dir():
            item = {"repository": str(candidate), "reason": "repository_missing"}
            result["errors" if explicit_repos else "warnings"].append(item)
            continue
        try:
            actual = Path(_git(candidate, "rev-parse", "--show-toplevel").decode().strip())
            if actual.resolve() != candidate.resolve():
                raise RuntimeError("Expected an independent repository root")
            indexed = _paths(candidate, "ls-files", "--cached", "-z")
            untracked = set() if staged else _paths(candidate, "ls-files", "--others", "--exclude-standard", "-z")
            visible = indexed | untracked
            updates, deleted = set(), set()
            if changed:
                arguments = ["diff", "--no-renames"]
                if staged:
                    arguments.append("--cached")
                else:
                    try:
                        _git(candidate, "rev-parse", "--verify", "HEAD")
                        arguments.append("HEAD")
                    except RuntimeError:
                        updates |= indexed
                updates |= _paths(candidate, *arguments, "--name-only", "-z", "--") | untracked
                deleted = _paths(candidate, *arguments, "--diff-filter=D", "--name-only", "-z", "--")
            states.append({"repo": candidate, "indexed": indexed, "visible": visible,
                           "guides": {name for name in visible if _is_guidance(name)},
                           "updates": updates, "deleted": deleted})
            result["repositories"].append(str(candidate))
        except (RuntimeError, OSError) as error:
            result["errors"].append({"repository": str(candidate), "reason": "git_error", "detail": str(error)})
    for document in documents or []:
        document = Path(os.path.abspath(document if document.is_absolute() else root / document))
        owner = next((state for state in states if _relative(document, state["repo"]) is not None), None)
        relative = _relative(document, owner["repo"]) if owner else None
        if owner and relative in owner["visible"]:
            owner["guides"].add(relative)
        else:
            result["errors"].append({"source": str(document), "reason": "document_not_git_visible"})
    deleted_paths = {state["repo"] / name for state in states for name in state["deleted"]}
    for state in states:
        repo = state["repo"]
        for name in sorted(state["guides"]):
            source = repo / name
            if not staged and not source.exists():
                continue  # A deleted guide has no working-tree content to validate.
            try:
                content = (_git(repo, "show", ":" + name).decode("utf-8-sig") if staged
                           else source.read_text(encoding="utf-8-sig"))
                links = markdown_links(content)
            except (OSError, RuntimeError, UnicodeError) as error:
                result["errors"].append({"source": str(source), "reason": "read_error", "detail": str(error)})
                continue
            targets = [(link, local_target(source, link.destination) if link.destination is not None else None) for link in links]
            impacted = any(target is not None and any(deleted == target or target in deleted.parents for deleted in deleted_paths)
                           for _, target in targets)
            if changed and name not in state["updates"] and not impacted:
                continue
            result["checked_guides"] += 1
            for link, target in targets:
                if link.destination is None:
                    result["errors"].append({"source": str(source), "line": link.line,
                                             "reference": link.reference, "reason": "undefined_reference"})
                    continue
                if target is None:
                    continue
                result["checked_links"] += 1
                relative = _relative(target, repo)
                if staged and relative is not None:
                    prefix = "" if relative == "." else relative.rstrip("/") + "/"
                    exists = relative in state["indexed"] or any(name.startswith(prefix) for name in state["indexed"])
                else:
                    exists = target.exists()
                if not exists:
                    result["errors"].append({"source": str(source), "line": link.line, "destination": link.destination,
                                             "target": str(target), "reason": "missing_target"})
    if not states and not result["errors"]:
        result["errors"].append({"reason": "no_repositories"})
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="Project repository root")
    parser.add_argument("--repo", type=Path, action="append", help="Repository root to check (repeatable; defaults to the five repositories)")
    parser.add_argument("--document", type=Path, action="append", help="Additional Git-visible Markdown document, relative to --root (repeatable)")
    parser.add_argument("--report", help="Write a JSON report to this path, or '-' for stdout")
    parser.add_argument("--staged", action="store_true", help="Read guidance and same-repository destinations from the Git index")
    parser.add_argument("--changed", action="store_true", help="Check changed guides and guides referring to deleted paths")
    args = parser.parse_args(argv)
    result = check_guidance(args.root, args.repo, documents=args.document, staged=args.staged, changed=args.changed)
    report = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.report == "-":
        print(report, end="")
    else:
        if args.report:
            Path(args.report).write_text(report, encoding="utf-8")
        print(f"Guidance: {result['checked_guides']} guides, {result['checked_links']} local links, "
              f"{len(result['errors'])} errors, {len(result['warnings'])} warnings")
        for issue in result["errors"]:
            print(f"{issue.get('source', issue.get('repository', ''))}:{issue.get('line', '')}: "
                  f"{issue['reason']} {issue.get('destination', issue.get('reference', issue.get('detail', '')))}")
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
