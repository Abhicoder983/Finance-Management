import jwt
from django.conf import settings
from datetime import datetime, timedelta

def generate_RefreshJwt(user,role):
    payload = {
       
        "user_id": user,
        "role":role,
        "exp":datetime.utcnow() + timedelta(days=10),
        "iat":datetime.utcnow()
        
    }

    token = jwt.encode(payload, settings.SECRET_KEYS, algorithm="HS256")
    return token

def generate_AccessToken(user):
    payload={
        "user_id":str(user),
        "exp":datetime.utcnow() + timedelta(days=2),
        "iat":datetime.utcnow()
    }

    token = jwt.encode(payload, settings.SECRET_KEYS, algorithm="HS256")
    return token
