from rest_framework import permissions
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound

OWNER_METHODS = ('GET','POST', 'DELETE')
UNAUTH_METHODS = ('POST',)

class IsRecipientOrWriteOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        recipient_username = view.kwargs.get('recipient_username')
        try:
            recipient = get_user_model().objects.get(username=recipient_username)
        except get_user_model().DoesNotExist:
            raise NotFound('User does not exist.')
        if request.user == recipient and request.method in OWNER_METHODS:
            return True
        return request.method in UNAUTH_METHODS
