import base64
import hashlib
import hmac
import time

import requests
import random

endpoint = "tmt.tencentcloudapi.com"
secret_id = "AKIDa9eDT1eYP5amxLnjme3KQrma6Vjp3gZM"
secret_key = "nlcNx68yc5QalkYBd1DmBPRIH9rNI3e3"


def get_string_to_sign(method, endpoint, params):
    s = method + endpoint + "/?"
    query_str = "&".join("%s=%s" % (k, params[k]) for k in sorted(params))
    return s + query_str


def sign_str(key, s, method):
    hmac_str = hmac.new(key.encode("utf8"), s.encode("utf8"), method).digest()
    return base64.b64encode(hmac_str)


def trans_tencent(q="苹果", fromLang='auto', toLang='en'):
    data = {
        'SourceText': q,
        'Source': fromLang,
        'Target': toLang,
        'Action': "TextTranslate",
        'Nonce': random.randint(32768, 65536),
        'ProjectId': 0,
        'Region': 'ap-hongkong',
        'SecretId': secret_id,
        'SignatureMethod': 'HmacSHA1',
        'Timestamp': int(time.time()),
        'Version': '2018-03-21',
    }
    s = get_string_to_sign("GET", endpoint, data)
    data["Signature"] = sign_str(secret_key, s, hashlib.sha1)

    # 此处会实际调用，成功后可能产生计费
    r = requests.get("https://" + endpoint, params=data, timeout=3)
    # print(r.json())
    return r.json()['Response']['TargetText']


if __name__ == '__main__':
    print(trans_tencent())
    print(trans_tencent('apple', 'auto', 'zh'))
