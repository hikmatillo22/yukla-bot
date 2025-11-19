# admin.py - send broadcast to ids listed in admin_targets.txt
import sys, requests
from config import TOKEN
def read_targets(path='admin_targets.txt'):
    try:
        with open(path,'r') as f:
            return [int(x.strip()) for x in f if x.strip()]
    except Exception:
        return []
def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    r = requests.post(url, json={'chat_id': chat_id, 'text': text})
    return r.status_code, r.text
if __name__=='__main__':
    if len(sys.argv)<2:
        print('Usage: python admin.py "Your message"')
        sys.exit(1)
    msg = sys.argv[1]
    targets = read_targets()
    if not targets:
        print('No targets in admin_targets.txt')
        sys.exit(1)
    for t in targets:
        code, text = send_message(t, msg)
        print('sent to', t, code)
