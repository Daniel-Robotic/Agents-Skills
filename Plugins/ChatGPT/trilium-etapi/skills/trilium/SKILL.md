---
name: trilium
description: Search, read, create, edit, and organize Trilium notes using the official ETAPI through the bundled local REST client.
---

# Trilium

This plugin runs locally in Codex Desktop and calls the user's Trilium ETAPI directly over HTTPS. It needs `TRILIUM_BASE_URL` (for example `https://notes.example.com`) and `TRILIUM_ETAPI_TOKEN` in the local environment. Read `../../README.md` for setup. Never print the token or pass it as a command argument.

Run the bundled client using `python <plugin-root>/scripts/etapi.py list` to see the supported operations. Run `python <plugin-root>/scripts/etapi.py call <operationId> --path '{"noteId":"..."}' --query '{"search":"..."}' --json '{...}'` to call an operation. For note content, use `--text-file <path>`; for ZIP and other binary uploads, use `--binary-file <path>`. Use `--output <path>` for binary downloads.

Search before guessing a note ID. Read the target note before editing it. Explain destructive changes and ask for confirmation before deleting. If the server returns an error, report the error and do not claim success.

The operation list covers the official ETAPI specification stored in `scripts/etapi_ops.json`. Consult the Trilium instance's `/etapi/etapi.openapi.yaml` for the exact request fields supported by that version.
