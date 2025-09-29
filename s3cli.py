#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import io
import mimetypes
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

from minio import Minio
from minio.error import S3Error


def require_env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        print(f"[FATAL] Missing env var: {name}", file=sys.stderr)
        sys.exit(1)
    return v


def make_client(insecure: bool = False) -> Minio:
    endpoint = require_env("S3_ENDPOINT").replace("https://", "").replace("http://", "")
    access_key = require_env("S3_ACCESS_KEY")
    secret_key = require_env("S3_SECRET_KEY")
    secure = not insecure  # If --insecure is provided => False

    return Minio(
        endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=secure
    )


def guess_content_type(path: Path) -> str:
    ctype, _ = mimetypes.guess_type(path.name)
    return ctype or "application/octet-stream"


def do_upload(args):
    client = make_client(args.insecure)
    bucket = require_env("S3_BUCKET")
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"[FATAL] File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    key = args.key or f"{args.prefix}{file_path.name}"
    content_type = guess_content_type(file_path)
    data = file_path.read_bytes()

    print(f"[STEP] Uploading {file_path} -> s3://{bucket}/{key}")
    client.put_object(
        bucket,
        key,
        io.BytesIO(data),
        length=len(data),
        content_type=content_type
    )
    print("[OK] Uploaded.")


def do_presign(args):
    client = make_client(args.insecure)
    bucket = require_env("S3_BUCKET")
    url = client.presigned_get_object(bucket, args.key, expires=timedelta(seconds=args.expires))
    print(url)


def do_head(args):
    client = make_client(args.insecure)
    bucket = require_env("S3_BUCKET")
    try:
        st = client.stat_object(bucket, args.key)
        print(f"Key: {args.key}\nSize: {st.size}\nContentType: {st.content_type}\nETag: {st.etag}")
    except S3Error as e:
        print(f"[ERR] {e}", file=sys.stderr)
        sys.exit(1)


def do_list(args):
    client = make_client(args.insecure)
    bucket = require_env("S3_BUCKET")
    prefix = args.prefix or ""
    objs = client.list_objects(bucket, prefix=prefix, recursive=True)
    found = False
    for o in objs:
        print(f"{o.object_name}\t{o.size}B")
        found = True
    if not found:
        print("(empty)")


def do_delete(args):
    client = make_client(args.insecure)
    bucket = require_env("S3_BUCKET")
    client.remove_object(bucket, args.key)
    print("[OK] Deleted:", args.key)


def do_overwrite(args):
    client = make_client(args.insecure)
    bucket = require_env("S3_BUCKET")
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"[FATAL] File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    content_type = guess_content_type(file_path)
    data = file_path.read_bytes()
    print(f"[STEP] Overwriting {file_path} -> s3://{bucket}/{args.key}")
    client.put_object(
        bucket,
        args.key,
        io.BytesIO(data),
        length=len(data),
        content_type=content_type
    )
    print("[OK] Overwritten.")


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(prog="minio-cli", description="CLI for managing MinIO/S3-Compatible storage")
    parser.add_argument("--insecure", action="store_true", help="Disable SSL (testing only)")

    sub = parser.add_subparsers(dest="cmd", required=True)

    p_up = sub.add_parser("upload", help="Upload file")
    p_up.add_argument("file")
    p_up.add_argument("--key")
    p_up.add_argument("--prefix", default="")
    p_up.set_defaults(func=do_upload)

    p_ps = sub.add_parser("presign", help="Create temporary GET link")
    p_ps.add_argument("key")
    p_ps.add_argument("--expires", type=int, default=300, help="Expiration time in seconds")
    p_ps.set_defaults(func=do_presign)

    p_hd = sub.add_parser("head", help="Show metadata")
    p_hd.add_argument("key")
    p_hd.set_defaults(func=do_head)

    p_ls = sub.add_parser("list", help="List files")
    p_ls.add_argument("--prefix", default="")
    p_ls.set_defaults(func=do_list)

    p_del = sub.add_parser("delete", help="Delete file")
    p_del.add_argument("key")
    p_del.set_defaults(func=do_delete)

    p_ov = sub.add_parser("overwrite", help="Overwrite existing file")
    p_ov.add_argument("key")
    p_ov.add_argument("file")
    p_ov.set_defaults(func=do_overwrite)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
