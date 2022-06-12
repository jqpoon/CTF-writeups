import random
import string
import flask
import socket
import ipaddress
import os
import requests
from urllib.parse import urlparse

FLAG = "ICTF{f4k3_fl4g_f0r_t3st1ng}"

AUTH_TOKEN = "123"

app = flask.Flask(__name__)

@app.route('/')
def index():
    return '''
        <!DOCTYPE html>
        <html>
            <head>
                <title>Enhanced Enumnerator</title>
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
                <script src="https://cdn.jsdelivr.net/npm/vue"></script>
            </head>
            <body style="height: 100vh;">
                <div id="app" class="container" style="height: 100%">
                    <br/>
                    <h1 class="d-flex justify-content-center">Enhanced Enumerator</h1>
                    <h3 class="d-flex justify-content-center">Super Secure</h3>
                    <br/>
                    <h6 class="d-flex justify-content-center">Since you broke my last enumerator, I made a new one that is super secure.</h3>
                    <h6 class="d-flex justify-content-center"><span>Getting the flag will be much harder this time, due to my advanced filters and <a href=https://www.youtube.com/watch?v=dQw4w9WgXcQ>firewalls.</a></span></h6>
                    <br/>
                    <br/>
                    <div class="input-group input-group-lg mb-3">
                        <input v-model="url" class="form-control">
                        <div class="input-group-append">
                            <button v-on:click="fetch" class="btn btn-primary">SuperFastSearch</button>
                        </div>
                    </div>
                    <iframe :srcdoc="page" width="100%" height="50%"></iframe>
                </div>
                <script>
                    new Vue({
                        el: '#app',
                        data: {url: 'www.google.co.uk', page: ''},
                        methods: {
                          fetch: function () {
                            this.page = '';
                            fetch('/fetch?url=' + this.url)
                                .then((r) => r.text())
                                .then((r) => {
                                    this.page = r;
                                    })
                            }
                        }
                    })
                </script>
            </body>
        </html>
    '''

@app.route('/give_flag')
def admin():       
    if flask.request.remote_addr not in ['127.0.0.1', '::1', '::ffff:127.0.0.1']:
        return '''
            <html>
                <head>
                    <title>Not the admin page</title>
                    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
                </head>
                <body style="background:black">
                    <div class="d-flex justify-content-center">
                        <h1>You failed.</h1>
                        <br/>
                        <h2>Forbidden</h2>
                    </div>
                </body>
            </html>
        '''
    msg = '''
        <html>
            <head>
                <title>Admin page</title>
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
            </head>
            <body style="background:green">
                <br/>
                <h1 class="d-flex justify-content-center">Welcome back, admin!</h1>
                <h3 class="d-flex justify-content-center">Your flag has been stored safely below.</h1>
                <h6 class="d-flex justify-content-center">Flag: %s</h6>
            </body>
        </html>
    ''' % (FLAG)
    return msg

@app.route('/fetch')
def fetch():
    page = flask.request.args.get('page', '')
    if not page.startswith('http://') and not page.startswith('https://'):
        page = 'http://' + page
    
    result = verify_page(page)
    if result is not None:
        return result
    html_page = fetch_page(page, 0)
    return html_page

@app.errorhandler(404)
def page_not_found(e):
    return "This is not the page that you are looking for."

def verify_page(page):
    try:
        check = is_valid(urlparse(page).hostname)
    except Exception as e:
        return '''
            <html>
                <head>
                    <title>Wait, what?</title>
                </head>
                <body>
                    <h2>Not sure what happened.</h2>
                    <h3>But it can't be good. </h3>
                </body>
            </html>
        '''
    if not check:
        return '''
            <html>
                <head>
                    <title>Forbidden</title>
                </head>
                <body>
                    <h2>This is not allowed. Ever</h2>
                </body>
            </html>
        '''
    return None

def fetch_page(page, recursion):
    try:
        req = requests.get(page, allow_redirects=False, timeout=5, headers={'rm-token': AUTH_TOKEN})
    except Exception as e:
       return '''
                <html>
                    <head>
                        <title>Broken again</title>
                    </head>
                    <body>
                        <h1>Stop breaking my enumerator.</h1>
                    </body>
                </html>
            '''
    if 'location' in req.headers:
        if recursion > 1:
            return '''
                <html>
                    <head>
                        <title>Nope</title>
                    </head>
                    <body>
                        <h1>I don't like recursion.</h1>
                        <h2>Stopping here.</h2>
                    </body>
                </html>
            '''
        page = req.headers['location']
        check = verify_page(page)

        if check is not None:
            return check
        return fetch_page(page, recursion + 1)

    return req.text

def is_valid(hostname):
    try:
        return ipaddress.ip_address(socket.gethostbyname(hostname)).is_global
    except Exception as e:
        return False

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
