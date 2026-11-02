"""Local command-line client for Trilium's documented ETAPI operations."""

import argparse
import base64
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


def main():
    ops = {o["id"]: o for o in json.loads(Path(__file__).with_name("etapi_ops.json").read_text(encoding="utf-8"))}
    parser = argparse.ArgumentParser(description="Call Trilium's official REST ETAPI")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="List supported operation IDs and paths")
    call = sub.add_parser("call", help="Call one official ETAPI operation")
    call.add_argument("operation_id", choices=ops)
    call.add_argument("--path", default="{}", help="JSON object of path parameters")
    call.add_argument("--query", default="{}", help="JSON object of query parameters")
    bodies = call.add_mutually_exclusive_group()
    bodies.add_argument("--json", help="JSON request body")
    bodies.add_argument("--text-file", type=Path, help="UTF-8 text body from file")
    bodies.add_argument("--binary-file", type=Path, help="Binary body from file")
    call.add_argument("--output", type=Path, help="Write response bytes to file")
    args = parser.parse_args()
    if args.command == "list":
        for op in ops.values():
            print(f'{op["id"]:30} {op["method"]:6} {op["path"]}')
        return 0

    url = os.environ.get("TRILIUM_BASE_URL", "").strip().rstrip("/")
    token = os.environ.get("TRILIUM_ETAPI_TOKEN", "").strip()
    parsed = urlsplit(url)
    if not url or not token:
        raise ValueError("Set TRILIUM_BASE_URL and TRILIUM_ETAPI_TOKEN in the local environment")
    if parsed.scheme not in ("https", "http") or not parsed.netloc or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("TRILIUM_BASE_URL must be a plain Trilium instance URL")
    if parsed.scheme == "http" and parsed.hostname not in ("localhost", "127.0.0.1", "::1"):
        raise ValueError("Use HTTPS for a remote Trilium instance")
    if url.endswith("/etapi"):
        url = url[:-6]
    op = ops[args.operation_id]
    path_values, query_values = json.loads(args.path), json.loads(args.query)
    if not isinstance(path_values, dict) or not isinstance(query_values, dict):
        raise ValueError("--path and --query must be JSON objects")
    path = op["path"]
    for name in op["path_params"]:
        if name not in path_values:
            raise ValueError(f"Missing path parameter: {name}")
        value = str(path_values[name])
        if value in ("", ".", "..") or "/" in value or "\\" in value:
            raise ValueError(f"Invalid path parameter: {name}")
        path = path.replace("{" + name + "}", quote(value, safe=""))
    query = urlencode([(k, str(item).lower() if isinstance(item, bool) else str(item)) for k, v in query_values.items() if v is not None for item in (v if isinstance(v, list) else [v])])
    endpoint = url + "/etapi" + path + (("?" + query) if query else "")
    body, content_type = None, None
    if args.json is not None:
        body, content_type = json.dumps(json.loads(args.json), ensure_ascii=False).encode(), "application/json"
    elif args.text_file:
        body, content_type = args.text_file.read_bytes(), "text/plain; charset=utf-8"
    elif args.binary_file:
        body = args.binary_file.read_bytes()
        content_type = "application/zip" if args.operation_id == "importZip" else "application/octet-stream"
    headers = {"Authorization": token, "Accept": "*/*"}
    if content_type:
        headers["Content-Type"] = content_type
    request = Request(endpoint, data=body, headers=headers, method=op["method"])
    try:
        with build_opener(NoRedirect).open(request, timeout=45) as response:
            raw, status, mime = response.read(), response.status, response.headers.get("Content-Type", "")
    except HTTPError as exc:
        raw, status, mime = exc.read(), exc.code, exc.headers.get("Content-Type", "")
    except URLError as exc:
        raise ValueError(f"Cannot reach Trilium: {exc.reason}") from exc
    if args.output and status < 300:
        args.output.write_bytes(raw)
        print(json.dumps({"status": status, "output": str(args.output), "bytes": len(raw)}))
    else:
        try:
            result = json.loads(raw.decode("utf-8")) if "json" in mime else raw.decode("utf-8")
        except UnicodeDecodeError:
            result = {"base64": base64.b64encode(raw).decode("ascii"), "bytes": len(raw)}
        print(json.dumps({"status": status, "result": result}, ensure_ascii=False))
    return 0 if status < 300 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(2)
