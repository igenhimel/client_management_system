from django.shortcuts import render
import jwt
from django.http import JsonResponse
from django.conf import settings
from functools import wraps

SECRET_KEY = 'your-secret-key'  # Use the Django project's secret key


def token_required(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        token = request.COOKIES.get('jwt')
        error = ""
        if not token:
            error = "You are not authorized to access this content"
            return render(request, 'managementApps/error/401.html', {'error': error})
        try:

            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            request.user_id = user_id

        except jwt.ExpiredSignatureError:
            error = "You are not authorized to access this content"
            return render(request, 'managementApps/error/401.html', {'error': error})

        except (jwt.DecodeError, jwt.InvalidTokenError):
            error = "You are not authorized to access this content"
            return render(request, 'managementApps/error/401.html', {'error': error})

        return view_func(request, *args, **kwargs)

    return wrapped
