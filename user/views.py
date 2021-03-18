import json
import bcrypt
import jwt

from django.views import View
from django.http  import JsonResponse

from .models     import User
from my_settings import SECRET_KEY

class LoginView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            user     = User.objects.get(username=data['username'])
            password = data['password']
            user_id  = user.id
            
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                token = jwt.encode({"user_id" : user_id}, SECRET_KEY, algorithm="HS256")
                return JsonResponse({'token' : token, "message":"SUCCESS"}, status=200)
            return JsonResponse({"message" : "INVALID_USER"}, status=403)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"message" : "USER_DOES_NOT_EXIST"}, status=401)
        
    