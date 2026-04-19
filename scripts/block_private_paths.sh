#!/usr/bin/env bash
# Reject any staged path that belongs in the private deploy fork only.
# Used by both the local pre-commit hook and CI (see .github/workflows/ci.yml).
set -euo pipefail

DENY='^(dashboard/|shell\.md$|sitemap\.xml$|robots\.txt$|logo\.png$|logo_under_1mb_768\.png$|python_modules/|\.assetsignore$|scripts/generate_articles\.py$)'

if [ "$#" -eq 0 ]; then
  candidates=$(git ls-files)
else
  candidates=$(printf '%s\n' "$@")
fi

hits=$(printf '%s\n' "$candidates" | grep -E "$DENY" || true)

if [ -n "$hits" ]; then
  echo "Refusing private/site paths (verifiabl.dev deploy-only):" >&2
  echo "$hits" >&2
  echo >&2
  echo "These belong in the private deploy fork, not the public OSS repo." >&2
  echo "Unstage with: git restore --staged <file>" >&2
  exit 1
fi
