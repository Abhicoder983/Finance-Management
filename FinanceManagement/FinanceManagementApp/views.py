from django.shortcuts import render
from .models import User,recordsModel
from FinanceManagement.utils import generate_RefreshJwt,generate_AccessToken
from rest_framework.response import Response
# Create your views here.

def dashboard(request):
    try:
        user=User.objects.get(request.id,None)





        if(request.get('access_token',None)):
            access_Token= generate_AccessToken(user._id)
            json_data={user,access_Token}
            return Response(json_data,status=200)
        else:
            access_Token=generate_AccessToken(user._id)
            refresh_Token=generate_RefreshJwt(user._id,user.role)
            user.refresh_Token=refresh_Token
            user.save()
            json_data={access_Token,user}
            response = Response(json_data,status=200)
            response.set_cookie(key="refresh_token",        # cookie name
        value=refresh_Token,        # value
        httponly=True,              # JS se access nahi
        secure=True,               # localhost → False, prod → True
        samesite="Lax",             # CSRF protection
        max_age=6 * 24 * 60 * 60    # seconds (6 days))
    )
            return response
        
    except:
        response= Response({'error':'user does not exist'}, status=401)
        response.set_cookie(key="refresh_token",        # cookie name
        value=None,        # value
        httponly=True,              # JS se access nahi
        secure=True,               # localhost → False, prod → True
        samesite="Lax",             # CSRF protection
        max_age=6 * 24 * 60 * 60    # seconds (6 days))
    )
        return response
    

def logout(request):
    try:
        user=User.objects.get(request.id,None)
        user.refresh_Token=None
        
        user.save()

        json_data={'access_Token':None}

        response = Response(json_data,status=200)

        response.set_cookie(key="refresh_token",        # cookie name
        value=None,        # value
        httponly=True,              # JS se access nahi
        secure=True,               # localhost → False, prod → True
        samesite="Lax",             # CSRF protection
        max_age=6 * 24 * 60 * 60    # seconds (6 days))
    )
        return response
    except:
        response= Response({'error':'user does not exist'}, status=401)
        response.set_cookie(key="refresh_token",        # cookie name
        value=None,        # value
        httponly=True,              # JS se access nahi
        secure=True,               # localhost → False, prod → True
        samesite="Lax",             # CSRF protection
        max_age=6 * 24 * 60 * 60    # seconds (6 days))
    )
        return response

