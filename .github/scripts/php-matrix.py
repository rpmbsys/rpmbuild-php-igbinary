#!/usr/bin/env python3
"""Emit GitHub Actions build matrices for this repo, optionally filtered to a
single PHP minor. Writes ``test=<json>`` and ``docker=<json>`` to
``$GITHUB_OUTPUT`` (falls back to stdout when run locally).

Usage: php-matrix.py <all|8.5|85|8.4|84|8.3|83|8.2|82>

  test   - include-entries for the RPM build job (PHP minor x Rocky 9/10)
  docker - base-publish compose files (base-publisher repos consume this;
           leaf repos have no docker job and simply ignore it)
"""
import json
import os
import sys

SUPPORTED = ["82", "83", "84", "85"]
ROCKY = ["10", "9"]


def matrices(selector):
    """Return (test, docker) matrices for the given PHP selector.

    Accepts dotted or undotted form (8.5 / 85) or "all"; raises ValueError on
    anything else.
    """
    sel = selector.replace(".", "")
    if sel == "all":
        versions = SUPPORTED
    elif sel in SUPPORTED:
        versions = [sel]
    else:
        raise ValueError(f"invalid PHP selector {selector!r} (want all|8.2|8.3|8.4|8.5)")

    test = [
        {
            "compose-file": f"docker-compose.php{v}.yml",
            "repo": f"php{v}custom",
            "build": f"rocky{r}build",
            "uploader": f"rocky{r}bintray",
            "repo_path": f"rocky/{r}",
        }
        for v in versions
        for r in ROCKY
    ]
    docker = [f"build/php{v}/docker-compose.yml" for v in versions]
    return test, docker


def main(argv):
    try:
        test, docker = matrices(argv[1] if len(argv) > 1 else "all")
    except ValueError as exc:
        print(f"php-matrix: {exc}", file=sys.stderr)
        return 1

    lines = [
        "test=" + json.dumps(test, separators=(",", ":")),
        "docker=" + json.dumps(docker, separators=(",", ":")),
    ]
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
    else:
        print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
