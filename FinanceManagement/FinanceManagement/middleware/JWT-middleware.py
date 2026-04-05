from FinanceManagementApp.models import User
from ..utils import generate_RefreshJwt ,generate_AccessToken
from django.http import JsonResponse
from jwt.exceptions import (ExpiredSignatureError)
import jwt
from django.conf import settings
from bson import ObjectId


class JWTMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        print("JWT Middleware Loaded")



    def __call__(self, request):
        try:
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                access_Token = auth_header.split(" ")[1]
            else:
                return JsonResponse({'error':'auth headers and Bearer is not properly defined '},status=401)
            
            refresh_Token = request.COOKIES.get("refreshToken",None)
            if(not (refresh_Token and access_Token)):
                return JsonResponse({'error':'refresh token and access token is not properly defined '},status=401)
            
            payload = jwt.decode(
                access_Token,
                settings.SECRET_KEYS,
                algorithms=["HS256"]
            )

            user_id = ObjectId(payload.get("user_id"))
                    
            # Custom user model se user fetch

            user=User.objects.filter(id=user_id).first()
            if(not user):
                return JsonResponse({'error':'user does not exist'},status=401)
            request.id= user
            request.access_token=access_Token
            response = self.get_response(request)
            

        except:
            try:
                refresh_Token = request.COOKIES.get("refreshToken",None)
                payload = jwt.decode(
                refresh_Token,
                settings.SECRET_KEYS,
                algorithms=["HS256"]
            )
                
                user_id = ObjectId(payload.get("user_id"))
                user=User.objects.filter(id=user_id).first()
                if(not user):
                    return JsonResponse({'error':'user does not exist'},status=401)
                if(user.refresh_Token!=refresh_Token):
                    return JsonResponse({"error":"Something went wrong"},status=401)
                request.id= user
                request.refresh_Token=refresh_Token

            except Exception as ExpiredSignatureError:
                return JsonResponse({'error':'token is expired'},status=401)

        response = self.get_response(request)
        return response

            