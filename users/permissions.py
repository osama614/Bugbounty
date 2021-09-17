from rest_framework.permissions import BasePermission

class IsVerifiedEmail(BasePermission):
    message = {
                "message":"You should verify your email get access to the dashboard !",
                "verification_step": "email",

              }

    def has_permission(self, request, view):
        if request.user.verified_email:
            return True

        else:
            return False

class IsVerifiedPhone(BasePermission):
    message = {
                "message":"You should verify your phone to get access to the dashboard !",
                "verification_step": "phone",

              }


    def has_permission(self, request, view):
        if request.user.verified_phone:
            return True

        else:
            return False