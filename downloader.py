import requests
from urllib.parse import quote_plus
def _walk_json(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                yield from _walk_json(v)
            elif isinstance(v, str):
                if v.startswith('http://') or v.startswith('https://'):
                    yield {'key': k, 'value': v}
    elif isinstance(obj, list):
        for item in obj:
            yield from _walk_json(item)
def guess_type_from_url(url):
    lower = url.lower()
    if any(lower.endswith(ext) for ext in ('.mp4', '.mov', '.mkv', '.webm', '.ts')):
        return 'video'
    if any(lower.endswith(ext) for ext in ('.mp3', '.m4a', '.aac', '.ogg', '.wav')):
        return 'audio'
    return 'document'
def fetch_and_parse(api_base, target_url, timeout=20):
    full = api_base + quote_plus(target_url)
    r = requests.get(full, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    medias = []
    if isinstance(data, dict):
        for key in ('result','data','media','files','download','downloads','response'):
            if key in data and data[key]:
                payload = data[key]
                if isinstance(payload, dict):
                    if 'medias' in payload and isinstance(payload['medias'], list):
                        for entry in payload['medias']:
                            if isinstance(entry, dict):
                                url = entry.get('url') or entry.get('src') or entry.get('link')
                                if isinstance(url, str) and url.startswith('http'):
                                    t = entry.get('type') or guess_type_from_url(url)
                                    medias.append({'url': url, 'type': t, 'title': entry.get('title') or entry.get('name')})
                    for item in _walk_json(payload):
                        medias.append({'url': item['value'], 'type': guess_type_from_url(item['value'])})
                elif isinstance(payload, list):
                    for entry in payload:
                        if isinstance(entry, str) and entry.startswith('http'):
                            medias.append({'url': entry, 'type': guess_type_from_url(entry)})
                        elif isinstance(entry, dict):
                            for item in _walk_json(entry):
                                medias.append({'url': item['value'], 'type': guess_type_from_url(item['value'])})
                elif isinstance(payload, str) and payload.startswith('http'):
                    medias.append({'url': payload, 'type': guess_type_from_url(payload)})
        for item in _walk_json(data):
            if not any(m['url'] == item['value'] for m in medias):
                medias.append({'url': item['value'], 'type': guess_type_from_url(item['value'])})
    medias = [m for m in medias if m['type'] in ('video','audio') and isinstance(m.get('url'), str)]
    seen = set(); unique = []
    for m in medias:
        if m['url'] not in seen:
            seen.add(m['url']); unique.append(m)
    return unique
def choose_media_type(url, declared_type=None):
    if declared_type:
        t = declared_type.lower()
        if 'video' in t: return 'video'
        if 'audio' in t: return 'audio'
        return 'document'
    return guess_type_from_url(url)
