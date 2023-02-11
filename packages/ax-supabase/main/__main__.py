import hashlib
import hmac
import json
import os

from supabase import Client, create_client


def save(dataset):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)
    data = supabase.table("generated").insert(dataset).execute()
    print(data)


def check_signature(sig, data, secret):
    try:
        signature_header = sig.replace("sha1=", "")
        signature_content = hmac.new(
            key=secret.encode("utf-8"), msg=data, digestmod=hashlib.sha1
        ).hexdigest()
    except AttributeError:
        pass
    except KeyError:
        pass
    except Exception:
        raise
    else:
        return bool(signature_header == signature_content)
    return False


def main(args):
    if args.get("__ow_method", "").lower() == "get":
        return {"body": os.environ.get("AX_WEBHOOK_SECRET")}

    # reserialize json parameters
    data = {
        "id": args.get("id"),
        "uid": args.get("uid"),
        "name": args.get("name"),
        "text": args.get("text"),
        "text_modified": args.get("text_modified"),
        "collection_id": args.get("collection_id"),
        "collection_name": args.get("collection_name"),
        "language": args.get("language"),
        "html": args.get("html"),
        "html_axite": args.get("html_axite"),
    }

    signature = args.get("__ow_headers", {}).get("x-myax-signature", "")
    secret = os.environ.get("AX_WEBHOOK_SECRET", "")
    _data = json.dumps(data).encode()

    if check_signature(signature, _data, secret):
        dataset = json.loads(_data)
        dataset["document_id"] = dataset.pop("id")
        save(dataset)
    else:
        print("wrong signature")

    return {"body": "OK"}
