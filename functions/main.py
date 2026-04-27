# Firebase Cloud Function entry point
from firebase_functions import https_fn
from firebase_admin import initialize_app
from app import app as flask_app

# Initialize Firebase Admin
initialize_app()

@https_fn.on_request()
def app(req: https_fn.Request) -> https_fn.Response:
    # This wraps the Flask app for Firebase
    with flask_app.request_context(req.environ):
        return flask_app.full_dispatch_request()
