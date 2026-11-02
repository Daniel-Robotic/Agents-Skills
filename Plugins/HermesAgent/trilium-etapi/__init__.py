"""Hermes Agent plugin for the Trilium ETAPI REST API."""

from __future__ import annotations

import base64
import json
import re
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlsplit
from urllib.request import Request, urlopen

from agent.secret_scope import get_secret


_OPS = {
    item["id"]: item
    for item in json.loads((Path(__file__).parent / "etapi_ops.json").read_text(encoding="utf-8"))
}
_ID_PATTERN = re.compile(r"^[A-Za-z0-9_]{1,128}$")
_DATE_PATTERN = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
_WEEK_PATTERN = re.compile(r"^[0-9]{4}-W[0-9]{2}$")


def _base_url(value: str) -> str:
    value = value.strip().rstrip("/")
    parsed = urlsplit(value)
    if parsed.scheme not in {"https", "http"} or not parsed.netloc:
        raise ValueError("Set base_url to the Trilium instance URL, for example https://notes.example.com")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("base_url must not contain credentials, a query string, or a fragment")
    if parsed.scheme != "https" and parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
        raise ValueError("Use HTTPS for remote Trilium servers")
    if value.endswith("/etapi"):
        value = value[:-6]
    return value


def _encode_query(query: Any) -> str:
    if query is None:
        return ""
    if not isinstance(query, dict):
        raise ValueError("query must be an object of ETAPI query parameters")
    pairs: list[tuple[str, str]] = []
    for key, value in query.items():
        if value is None:
            continue
        values = value if isinstance(value, list) else [value]
        for item in values:
            if isinstance(item, (dict, list)):
                raise ValueError(f"query parameter {key} must contain scalar values")
            pairs.append((str(key), str(item).lower() if isinstance(item, bool) else str(item)))
    encoded = urlencode(pairs)
    return f"?{encoded}" if encoded else ""


def _response_body(raw: bytes, content_type: str) -> dict[str, Any]:
    if not raw:
        return {"content_type": content_type, "body": None}
    if "json" in content_type.lower():
        try:
            return {"content_type": content_type, "body": json.loads(raw.decode("utf-8"))}
        except (UnicodeDecodeError, json.JSONDecodeError):
            pass
    try:
        return {"content_type": content_type, "body": raw.decode("utf-8")}
    except UnicodeDecodeError:
        return {
            "content_type": content_type,
            "body_base64": base64.b64encode(raw).decode("ascii"),
            "byte_length": len(raw),
        }


def _call_etapi(ctx: Any, args: dict[str, Any]) -> str:
    operation_id = args.get("operation_id")
    operation = _OPS.get(operation_id)
    if not operation:
        return json.dumps({"ok": False, "error": "Unknown operation_id. Use one of the operations listed in the tool description."})

    try:
        base = _base_url(str(ctx.get_config("base_url", default="")))
        token = (get_secret("TRILIUM_ETAPI_TOKEN") or "").strip()
        if not token:
            raise ValueError("Set the ETAPI token in the Trilium ETAPI plugin settings.")

        path_parameters = args.get("path_parameters") or {}
        if not isinstance(path_parameters, dict):
            raise ValueError("path_parameters must be an object")
        path = operation["path"]
        for name in operation["path_params"]:
            value = path_parameters.get(name)
            if value is None:
                raise ValueError(f"Missing path parameter: {name}")
            text_value = str(value)
            if name in {"noteId", "branchId", "attributeId", "attachmentId", "revisionId", "parentNoteId", "backupName"} and not _ID_PATTERN.fullmatch(text_value):
                raise ValueError(f"Invalid {name}; ETAPI IDs contain letters, numbers, or underscores")
            if name == "date" and not _DATE_PATTERN.fullmatch(text_value):
                raise ValueError("date must use YYYY-MM-DD")
            if name == "week" and not _WEEK_PATTERN.fullmatch(text_value):
                raise ValueError("week must use YYYY-Www, for example 2026-W44")
            path = path.replace("{" + name + "}", quote(text_value, safe=""))

        url = base + "/etapi" + path + _encode_query(args.get("query"))
        body_fields = [key for key in ("json_body", "text_body", "binary_base64") if args.get(key) is not None]
        if len(body_fields) > 1:
            raise ValueError("Use only one of json_body, text_body, or binary_base64")

        data = None
        headers = {"Authorization": token, "Accept": "*/*"}
        if body_fields:
            field = body_fields[0]
            if field == "json_body":
                data = json.dumps(args[field], ensure_ascii=False).encode("utf-8")
                headers["Content-Type"] = "application/json"
            elif field == "text_body":
                data = str(args[field]).encode("utf-8")
                headers["Content-Type"] = "text/plain; charset=utf-8"
            else:
                data = base64.b64decode(args[field], validate=True)
                headers["Content-Type"] = "application/octet-stream"

        request = Request(url, data=data, headers=headers, method=operation["method"])
        try:
            with urlopen(request, timeout=45) as response:
                raw = response.read()
                result = {"ok": True, "operation_id": operation_id, "status": response.status}
                result.update(_response_body(raw, response.headers.get("Content-Type", "application/octet-stream")))
                return json.dumps(result, ensure_ascii=False)
        except HTTPError as exc:
            raw_error = exc.read()
            try:
                detail = json.loads(raw_error.decode("utf-8")) if raw_error else None
            except (UnicodeDecodeError, json.JSONDecodeError):
                detail = raw_error.decode("utf-8", errors="replace")[:4000]
            return json.dumps({"ok": False, "operation_id": operation_id, "status": exc.code, "error": detail}, ensure_ascii=False)
        except URLError as exc:
            return json.dumps({"ok": False, "operation_id": operation_id, "error": f"Could not reach Trilium: {exc.reason}"}, ensure_ascii=False)
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        return json.dumps({"ok": False, "operation_id": operation_id, "error": str(exc)}, ensure_ascii=False)


_SCHEMA = {
    "name": "trilium_etapi",
    "description": (
        "Call Trilium's official REST ETAPI. Use operation_id from the supported list: "
        + ", ".join(_OPS)
        + ". Path parameters go in path_parameters; query string values go in query. "
        "Send JSON with json_body, text content with text_body, or raw binary as base64 in binary_base64. "
        "This tool can create, edit, move, restore, or delete Trilium data; explain consequential changes and get user confirmation before carrying them out."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "operation_id": {"type": "string", "enum": list(_OPS), "description": "ETAPI operationId from the official specification."},
            "path_parameters": {"type": "object", "additionalProperties": {"type": "string"}, "description": "Values for the operation's path placeholders, such as noteId or date."},
            "query": {"type": "object", "additionalProperties": {"type": ["string", "number", "integer", "boolean", "array", "null"]}, "description": "ETAPI query parameters."},
            "json_body": {"type": "object", "description": "JSON request body for ETAPI operations that accept application/json."},
            "text_body": {"type": "string", "description": "UTF-8 note or attachment content for text/plain endpoints."},
            "binary_base64": {"type": "string", "description": "Base64-encoded bytes for application/octet-stream endpoints."},
        },
        "required": ["operation_id"],
        "additionalProperties": False,
    },
}


def register(ctx: Any) -> None:
    ctx.register_tool(name="trilium_etapi", toolset="trilium", schema=_SCHEMA, handler=lambda args: _call_etapi(ctx, args))
