# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

import os
import requests
import jwt
import time
from datetime import datetime

def make_jwt():
    iat = time.time()
    exp = iat + int(os.getenv('JWT_EXPIRY_SEC'))
    payload = {'iss': os.getenv('GOOGLE_SERVICE_EMAIL'),
            'sub': os.getenv('GOOGLE_SERVICE_EMAIL'),
            'aud': os.getenv('GOOGLE_AUD'),
            'iat': iat,
            'exp': exp}
    additional_headers = {'kid': os.getenv('GOOGLE_KEY_ID')}

    signed_jwt = jwt.encode(
        payload, 
        os.getenv('GOOGLE_PRIVATE_KEY').replace('\\n', '\n'),
        headers=additional_headers,
        algorithm='RS256'
    )
    return signed_jwt

def _build_header(token, content_type=None, accept=None):
    headers = {}

    if content_type:
        headers['Content-type'] = content_type

    if accept:
        headers['Accept'] = accept

    headers['Authorization'] = f'Bearer {token}'

    return headers

def update_jwt():
    # Make Google JWT
    access_token = make_jwt()
    print(access_token)

    # Update it in Asana
    ENDPOINT_BASE = "https://app.asana.com/api/1.0"
    endpoint = ENDPOINT_BASE + f"/tasks/{os.getenv('ASANA_TASK_GID')}"

    headers = _build_header(
        os.getenv('ASANA_PAT'),
        content_type='application/json',
        accept='application/json'
    )
    params = {
        'notes': access_token
    }
    data = {
        'data': params
    }
    r = requests.put(endpoint, json=data, headers=headers).json()['data']
    print(r)

while True:
    update_jwt()
    date = datetime.now()
    print(f'{date=}')
    refresh_sec = int(os.getenv('JWT_REFRESH_SEC'))
    print(refresh_sec)
    time.sleep(refresh_sec)