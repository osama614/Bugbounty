from rest_framework.permissions import BasePermission

class IsVerified(BasePermission):
    message = "You should verify your email and phone to get access to the dashboard"

    def has_permission(self, request, view):
        if request.user.verified_email and request.user.verified_phone:
            return True
        
        else:
            return False