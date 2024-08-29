from flask import Flask, redirect, url_for, session, request, render_template_string
from authlib.integrations.flask_client import OAuth
import os, threading, uuid, webbrowser, time
from werkzeug.serving import run_simple

from core.token import Token
from dotenv import load_dotenv


client_id = INSERT_YOUR_CLIENT_SECRET_ID
client_secret = INSERT_YOUR_CLIENT_SECRET_HERE

TokenManager = Token()

running = True
LastAuth = None

class Auth:
    def __init__(self):
        global running
        global LastAuth

        if LastAuth:
            LastAuth.shutdown_server()
            LastAuth = None 

        LastAuth = self

        running = True
        self.info = None
        self.stop_event = threading.Event()
        self._setup_flask_app()
        self._setup_oauth()
        self.init_app()

        server_thread = threading.Thread(target=self._run_server)
        server_thread.start()

        while running:
            time.sleep(1)

    def _setup_flask_app(self):
        self.app = Flask(__name__)
        self.app.secret_key = os.urandom(24)
        self.app.debug = False

    def _setup_oauth(self):
        self.oauth = OAuth(self.app)
        self.register = self.oauth.register(
            name='google',
            client_id=client_id,
            client_secret=client_secret,
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            access_token_url='https://accounts.google.com/o/oauth2/token',
            client_kwargs={'scope': 'openid email profile'},
            jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
        )

    def shutdown_server(self):
        global running

        if self.info:
            from window.init import database

            account = database.account_exists_with_info(self.info)
            
            if account:
                TokenManager.store_token(account['_id'])
            else:
                new_token = str(uuid.uuid4())
                TokenManager.store_token(new_token)

                database.create_user(TokenManager.get_token(), self.info)
                print(self.info)

        running = False
        self.stop_event.set()
        print("Shutdown initiated")
        
    def init_app(self):
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/login', 'login', self.login)
        self.app.add_url_rule('/login/authorized', 'authorized', self.authorized)
        self.app.add_url_rule('/login/success', 'login_success', self.login_success)
        self.app.add_url_rule('/security-check', 'security_check', self.security_check)
        self.app.add_url_rule('/shutdown', 'shutdown', self.shutdown_server)

        webbrowser.open_new("http://localhost:5500")

    def _run_server(self):
        try:
            run_simple('localhost', 5500, self.app, use_reloader=False)
        except Exception as e:
            print(f"Server stopped with exception: {e}")


    def index(self):
        return redirect(url_for('login'))

    def login(self):
        nonce = str(uuid.uuid4())
        session['nonce'] = nonce
        redirect_uri = url_for('authorized', _external=True)
        return self.register.authorize_redirect(redirect_uri, nonce=nonce)
    
    def authorized(self):
        try:
            token = self.register.authorize_access_token()
            if token is None:
                return 'Access Denied', 403

            nonce = session.pop('nonce', None)
            if not nonce:
                return 'Nonce not found in session', 400

            self.info = self.register.parse_id_token(token, nonce=nonce)
            if not self.info or 'sub' not in self.info:
                return 'Invalid token data', 400

            session['user_info'] = self.info
            self.shutdown_server()
            return redirect(url_for('login_success'))

        except Exception as e:
            return str(e), 500

    def login_success(self):
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Login Success</title>
            <script>
                setTimeout(function() {
                    window.location.href = "{{ url_for('security_check') }}";
                }, 2000);
            </script>
        </head>
        <body>
            <p>Login successfully, please wait...</p>
        </body>
        </html>
        ''')

    def security_check(self):
        return redirect("https://www.google.com")
