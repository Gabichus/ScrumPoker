from flask import redirect, session, jsonify, request, make_response
from app import app,db
from app.models import User
from flask_jwt_extended import create_access_token

from uuid import uuid4
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from json import loads, dumps
from jwt import decode

from config import backendAddress

discovery_doc = loads(urlopen("https://accounts.google.com/.well-known/openid-configuration").read().decode("ascii"))

client_id = "862399293797-q7m316vv5rlk05ppbhjrdh5hd15fcus9.apps.googleusercontent.com"
client_secret = "FV6zxEsSIoE3fnC9sK-I3CIM"
redirect_url = backendAddress + "/login_from_google_2"


def login_from_google_1():
    session['state'] = "security_token={}".format(str(uuid4()))
    # session['typeApp'] = request.args.get('typeApp') 
    url = ("{}?client_id={}&".format(discovery_doc['authorization_endpoint'], client_id) +
           "response_type=code&scope=openid%20email&redirect_uri={}&".format(redirect_url) +
           "state={}&".format(session['state']) +
           # "openid.realm=example.com&" + "hd=example.com&" +
           "nonce={})".format(str(uuid4())))
    return redirect(url)


def login_from_google_2():
    if not request.args.get("code"):
        return "<h3>Arg 'code' not found, arg 'error'='{}'<h3>".format(request.args.get('error')), 401
    if request.args.get('state') != session['state']:
        return "<h3>Invalid state parameter.<h3>", 401

    data = loads(urlopen(Request(discovery_doc["token_endpoint"], urlencode({
        "code": request.args.get("code"),
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_url,
        "grant_type": "authorization_code"
    }).encode('ascii'), method="POST")).read().decode("ascii"))

    email = decode(data["id_token"], verify=False)["email"]

    user = User.query.filter_by(gmail=email).first()
    if not user:
        # "https://accounts.google.com/Logout"
        return redirect('https://accounts.google.com/Logout')
        # return "<h3>User is not found</h3>", 400

    at = create_access_token(identity=user.id)
    user.token = at
    db.session.commit()
    return '''<script>
                opener.postMessage("{}", '*');
                window.close();
            </script>'''.format(at)