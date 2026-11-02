---
name: trilium-etapi
description: Search and manage notes, attachments, attributes, tree placement, history, revisions, calendar notes, and other documented Trilium ETAPI features.
version: 0.1.0
---

# Trilium ETAPI

Use the `trilium_etapi` tool to call Trilium's documented ETAPI operations. This skill calls Trilium's REST API directly. Its base URL and ETAPI token are configured in the Hermes plugin settings.

## How to use it

1. If the user asks about existing notes, search first with `searchNotes`; use a narrow `ancestorNoteId` when they mention a section or folder.
2. Get the note metadata with `getNoteById` and its body with `getNoteContent` when needed. A note ID is not the same as a branch ID.
3. Before creating or changing content, identify the exact target note and requested change. Do not guess where a note belongs.
4. Before deleting notes, branches, attributes, or attachments, explain what will be removed and ask the user to confirm.
5. After a write, read the affected object again when practical and report the resulting note or entity ID.

## Operations

`trilium_etapi` accepts an official ETAPI `operation_id`, `path_parameters`, optional `query`, and one request body form:

- `json_body` for `application/json` requests;
- `text_body` for `text/plain` note or attachment content;
- `binary_base64` for `application/octet-stream` content.

The complete operation list and URL templates are in `etapi_ops.json`; the current upstream OpenAPI reference is served by Trilium at `/etapi/etapi.openapi.yaml`. The plugin covers note creation, search, metadata/content edits, tree branches, attachments and their binary content, attributes, revisions, history, restore, ZIP import/export, inbox and calendar notes, app info, metrics, and backup operations.

Do not use internal `/api/*` routes. They are not the public ETAPI. Never send the ETAPI token in tool arguments or include it in the response.
