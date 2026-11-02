# Trilium for ChatGPT

This connects a custom GPT to your Trilium server. ChatGPT sends requests directly to the server's REST ETAPI. There is no MCP server or intermediary.

## Connect it

1. In `openapi.yaml`, replace `https://YOUR_TRILIUM_HOST` with your public HTTPS address, for example `https://notes.example.com`. Keep `/etapi` at the end of the server URL.
2. In ChatGPT, create or edit a GPT and open **Configure → Actions → Create new action**.
3. Paste the contents of `openapi.yaml` into the schema editor (or import the file if your editor offers that option).
4. Under **Authentication**, choose **API Key**, then **Custom**. Set the header name to `Authorization`.
5. Paste the ETAPI token from **Trilium → Options → ETAPI** into the key field. Enter the token as shown; do not add `Bearer`.
6. Add the text from `instructions.md` to the GPT's instructions, save, and try a read-only request such as finding a note.

The server address belongs in the schema. The token belongs in ChatGPT's authentication settings; don't put it in this repository or in the schema.

## What it can do

The schema follows Trilium's official ETAPI specification. It covers note search and content, note tree branches, attachments, attributes, revisions and history, restore, import/export, inbox and calendar notes, app info, metrics, and backups. Trilium serves the specification used by your instance at `https://<your-host>/etapi/etapi.openapi.yaml`.

Some operations transfer ZIP files or other binary data. The API is described in the schema, but ChatGPT Actions may not handle every binary upload or download in a useful way. For those operations, use Hermes or Trilium's own interface.

This is a **GPT Action**, which lets a custom GPT call an external REST API. It is not a standalone ChatGPT app from the app directory. Availability of GPT creation and Actions depends on your ChatGPT plan and workspace settings.
