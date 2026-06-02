"""
Quote-span extractor for Dante's Divine Comedy (analysis step).

Deterministic logic (no LLM): after apostrophe disambiguation
(`convert_apostrophe` in tokenizer.py), the quote delimiters become
unambiguous, so matched pairs can be extracted as a nesting tree:

  «  »  U+00AB / U+00BB : outer speech
  ‘  ’  U+2018 / U+2019 : inner quote
  “  ”  U+201C / U+201D : innermost quote

Output: quotes/<canticle>.xml — generated, NOT committed (see .gitignore).
Nesting is expressed by element nesting. Each <q> carries a stable `id`
(e.g. "10:77A") and, when several quotes share a start line, a short `head`
of leading tokens as a human hint. No speaker here; speakers are maintained
in a sibling committed file (quotes/<canticle>.tsv) produced by a distinct step.

The `id` is line-anchored: "<canto>:<start-line>" plus a suffix letter
(A, B, ... in open order) only when more than one quote starts on that line.
Ids stay stable across regeneration as long as the source and quote structure
do not change.

Output paths are relative to this script's directory.
"""
import sys
import string
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tokenizer import convert_apostrophe, tokenize, has_alpha

OPENERS = {"«": "»", "‘": "’", "“": "”"}  # «»  ‘’  “”
CLOSERS = {v: k for k, v in OPENERS.items()}


def build_tree(lines: List[str]) -> list:
    """
    Parse disambiguated lines into a tree of quote nodes.

    Returns the list of top-level nodes. Each node is a dict with keys
    opener, sline, scol (open position), eline, ecol (close position),
    and children (nested nodes, in source order).

    Raises:
        ValueError: on a mismatched or unclosed delimiter.
    """
    root: list = []
    stack: list = []
    for ln, line in enumerate(lines, 1):
        for col, ch in enumerate(line):
            if ch in OPENERS:
                node = {"opener": ch, "sline": ln, "scol": col, "children": []}
                (stack[-1]["children"] if stack else root).append(node)
                stack.append(node)
            elif ch in CLOSERS:
                if not stack or stack[-1]["opener"] != CLOSERS[ch]:
                    raise ValueError(f"mismatched {ch!r} at line {ln}")
                node = stack.pop()
                node["eline"], node["ecol"] = ln, col
    if stack:
        raise ValueError(f"unclosed delimiters: {stack}")
    return root


def flatten(nodes: list, acc: list) -> list:
    """Collect every node in the tree (depth-first) into acc."""
    for node in nodes:
        acc.append(node)
        flatten(node["children"], acc)
    return acc


def leading_tokens(lines: List[str], node: dict) -> List[str]:
    """Alphabetic tokens following the node's opening delimiter on its start line."""
    rest = lines[node["sline"] - 1][node["scol"] + 1:]
    return [t for t in tokenize(rest) if has_alpha(t)]


def _suffix(i: int) -> str:
    """Open-order suffix: A, B, ... Z, then numeric beyond 26 (defensive)."""
    return string.ascii_uppercase[i] if i < 26 else str(i + 1)


def assign_ids(canto: int, lines: List[str], root: list) -> None:
    """
    Give every quote a line-anchored id, and a `head` hint when its start line
    carries more than one quote. Quotes sharing a start line are ordered by
    open position (so a parent precedes a child that opens on the same line).
    """
    groups: dict = {}
    for node in flatten(root, []):
        groups.setdefault(node["sline"], []).append(node)
    for sline, group in groups.items():
        group.sort(key=lambda n: n["scol"])
        if len(group) == 1:
            group[0]["id"] = f"{canto}:{sline}"
            continue
        toks = [leading_tokens(lines, n) for n in group]
        # Grow the prefix until every member's head is distinct.
        k = 1
        while k <= max(len(t) for t in toks):
            heads = [" ".join(t[:k]) for t in toks]
            if len(set(heads)) == len(heads):
                break
            k += 1
        for i, (node, t) in enumerate(zip(group, toks)):
            node["id"] = f"{canto}:{sline}{_suffix(i)}"
            node["head"] = " ".join(t[:k]) or "?"


def parse_canto(canto: int, path: Path) -> list:
    """Read a canto source file and return its quote tree (ids/heads assigned)."""
    lines = [
        convert_apostrophe(l)
        for line in path.read_text(encoding="utf-8").splitlines()
        if (l := line.strip())
    ]
    root = build_tree(lines)
    assign_ids(canto, lines, root)
    return root


def _esc(s: str) -> str:
    """Escape a string for an XML attribute value (double-quoted)."""
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def render(node: dict, depth: int) -> List[str]:
    """Render a node (and its children) as indented XML lines."""
    ind = "  " * depth
    line = (f'{node["sline"]}' if node["sline"] == node["eline"]
            else f'{node["sline"]}-{node["eline"]}')
    marker = node["opener"] + OPENERS[node["opener"]]
    attrs = f'id="{node["id"]}" line="{line}" marker="{_esc(marker)}"'
    if "head" in node:
        attrs += f' head="{_esc(node["head"])}"'
    if node["children"]:
        out = [f"{ind}<q {attrs}>"]
        for child in node["children"]:
            out += render(child, depth + 1)
        out.append(f"{ind}</q>")
        return out
    return [f"{ind}<q {attrs}/>"]


def emit_canticle(canticle: str, cantos: List[tuple]) -> str:
    """Render a whole canticle (list of (n, root)) as one XML document."""
    out = [f'<canticle name="{canticle}">']
    for n, root in cantos:
        out.append(f'  <canto n="{n}">')
        for node in root:
            out += render(node, 2)
        out.append("  </canto>")
    out.append("</canticle>")
    return "\n".join(out) + "\n"


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("canticles", nargs="+", help="canticle names, e.g. inferno")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    it_dir = script_dir.parent / "it"
    xml_dir = script_dir / "quotes"
    xml_dir.mkdir(exist_ok=True)
    for canticle in args.canticles:
        sources = sorted((it_dir / canticle).glob("[0-9][0-9].txt"))
        cantos = [(int(p.stem), parse_canto(int(p.stem), p)) for p in sources]
        out_path = xml_dir / f"{canticle}.xml"
        out_path.write_text(emit_canticle(canticle, cantos), encoding="utf-8")
        print(f"Wrote: quotes/{canticle}.xml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
