from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    provides read access to everyone, whether logged in or not
    provides write access only to the owner of the object
    """

    def has_object_permission(self, request, view, obj) -> bool:
        # read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # write permissions are only allowed to the owner of the meme
        return obj.owner == request.user
