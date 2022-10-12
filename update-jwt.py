# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

import os
import jwt
import time
from datetime import datetime

import mpy.util.simple_asana_handler as asana

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

def update_jwt():
    access_token = make_jwt()
    asana_handler = asana.Simple_asana_handler(token=os.getenv('ASANA_PAT'))
    asana_handler.put_jwt(access_token)

if __name__ == '__main__':
    refresh_sec = int(os.getenv('JWT_REFRESH_SEC'))
    do_loop = int(os.getenv('DO_LOOP'))

    while True:
        update_jwt()
        date = datetime.now()
        print(date)

        if not do_loop:
            break

        time.sleep(refresh_sec)