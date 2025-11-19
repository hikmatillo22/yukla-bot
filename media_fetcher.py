import requests, tempfile, os, time
MAX_RETRIES = 4
RETRY_DELAY = 3
def download_to_file(url, max_bytes=None, timeout=180):
    last_err = None
    path = None
    for attempt in range(1, MAX_RETRIES+1):
        try:
            r = requests.get(url, stream=True, timeout=timeout)
            r.raise_for_status()
            suffix = os.path.splitext(url.split('?')[0])[1] or ''
            fd, path = tempfile.mkstemp(suffix=suffix)
            os.close(fd)
            total = 0
            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if not chunk: break
                    f.write(chunk)
                    total += len(chunk)
                    if max_bytes and total > max_bytes:
                        f.close(); os.remove(path)
                        raise ValueError('File too large')
            return path
        except Exception as e:
            last_err = e
            try:
                if path and os.path.exists(path): os.remove(path)
            except: pass
            if attempt == MAX_RETRIES: raise last_err
            time.sleep(RETRY_DELAY)
def remove_file(path):
    try: os.remove(path)
    except: pass
