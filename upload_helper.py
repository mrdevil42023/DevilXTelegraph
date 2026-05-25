import requests
import mimetypes
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

CATBOX_API = "https://catbox.moe/user/api.php"


def _upload_catbox(file_path, file_name, mime_type):
    with open(file_path, "rb") as f:
        resp = requests.post(
            CATBOX_API,
            data={"reqtype": "fileupload", "userhash": ""},
            files={"fileToUpload": (file_name, f, mime_type)},
            timeout=60
        )
    resp.raise_for_status()
    url = resp.text.strip()
    if not url.startswith("http"):
        raise Exception(f"Catbox returned: {url}")
    return url


def _upload_0x0(file_path, file_name, mime_type):
    with open(file_path, "rb") as f:
        resp = requests.post(
            "https://0x0.st",
            files={"file": (file_name, f, mime_type)},
            timeout=60
        )
    resp.raise_for_status()
    url = resp.text.strip()
    if not url.startswith("http"):
        raise Exception(f"0x0.st returned: {url}")
    return url


def _upload_uguu(file_path, file_name, mime_type):
    with open(file_path, "rb") as f:
        resp = requests.post(
            "https://uguu.se/upload",
            files={"files[]": (file_name, f, mime_type)},
            timeout=60
        )
    resp.raise_for_status()
    data = resp.json()
    files = data.get("files", [])
    if not files or not files[0].get("url", "").startswith("http"):
        raise Exception(f"Uguu returned: {data}")
    return files[0]["url"]


def _upload_gofile(file_path, file_name, mime_type):
    server_resp = requests.get("https://api.gofile.io/getServer", timeout=15)
    server_resp.raise_for_status()
    server = server_resp.json().get("data", {}).get("server")
    if not server:
        raise Exception("GoFile: could not get server")
    with open(file_path, "rb") as f:
        resp = requests.post(
            f"https://{server}.gofile.io/uploadFile",
            files={"file": (file_name, f, mime_type)},
            timeout=120
        )
    resp.raise_for_status()
    data = resp.json()
    url = data.get("data", {}).get("downloadPage", "")
    if not url.startswith("http"):
        raise Exception(f"GoFile returned: {data}")
    return url


def _upload_transfersh(file_path, file_name, mime_type):
    with open(file_path, "rb") as f:
        resp = requests.put(
            f"https://transfer.sh/{file_name}",
            data=f,
            headers={"Max-Days": "14"},
            timeout=60
        )
    resp.raise_for_status()
    url = resp.text.strip()
    if not url.startswith("http"):
        raise Exception(f"transfer.sh returned: {url}")
    return url


HOSTS = [
    ("Catbox",     _upload_catbox),
    ("0x0.st",     _upload_0x0),
    ("Uguu.se",    _upload_uguu),
    ("GoFile",     _upload_gofile),
    ("Transfer.sh", _upload_transfersh),
]


def upload_file(file_path):
    """
    Uploads the file to all hosts in parallel.
    Returns a list of (host_name, url) tuples for every host that succeeded.
    Raises an exception only if ALL hosts fail.
    """
    mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    file_name = os.path.basename(file_path)

    results = []
    errors = []

    def try_upload(label, fn):
        try:
            url = fn(file_path, file_name, mime_type)
            print(f"[Upload] ✓ {label}: {url}")
            return (label, url)
        except Exception as e:
            print(f"[Upload] ✗ {label}: {e}")
            return (label, None, str(e))

    with ThreadPoolExecutor(max_workers=len(HOSTS)) as ex:
        futures = {ex.submit(try_upload, label, fn): label for label, fn in HOSTS}
        for future in as_completed(futures):
            res = future.result()
            if res[1]:
                results.append((res[0], res[1]))
            else:
                errors.append(f"{res[0]}: {res[2]}")

    if not results:
        raise Exception("All upload hosts failed:\n" + "\n".join(errors))

    return results
