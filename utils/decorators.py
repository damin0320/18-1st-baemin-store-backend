import json
import jwt
from jwt.exceptions import InvalidSignatureError, DecodeError

from django.http import JsonResponse

from user.models           import User
from baemin_store.settings import SECRET_KEY, HASHING_ALGORITHM


# auth check with blocking
def auth_check(func):
    def wrapper(self, request):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return JsonResponse({'message': 'TOKEN_DOSE_NOT_EXIST'})
            decoded_auth_token = jwt.decode(token, SECRET_KEY, algorithms=HASHING_ALGORITHM)
            
            user_id = decoded_auth_token['user_id']
            user    = User.objects.get(id=user_id)

            request.user = user
            return func(self, request)

        except InvalidSignatureError:
            return JsonResponse({'message': 'SIGNATURE_VERIFICATION_FAILED'})
        except DecodeError:
            debugger.exception('DecodeError')
            return JsonResponse({'message': 'DECODE_ERROR'})
        except User.DoesNotExist:
            return JsonResponse({'message': 'USER_DOES_NOT_EXIST'})
    return wrapper


# user check without blocking 
def user_check(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            if not token:
                request.user = None
                return func(self, request, *args, **kwargs)
            decoded_auth_token = jwt.decode(token, SECRET_KEY, algorithms=HASHING_ALGORITHM)
            
            user_id = decoded_auth_token['user_id']
            user    = User.objects.get(id=user_id)

            request.user = user
            return func(self, request, *args, **kwargs)

        except InvalidSignatureError:
            return JsonResponse({'message': 'SIGNATURE_VERIFICATION_FAILED'})
        except DecodeError:
            return JsonResponse({'message': 'DECODE_ERROR'})
        except User.DoesNotExist:
            return JsonResponse({'message': 'USER_DOES_NOT_EXIST'})
    return wrapper
