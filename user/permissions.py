from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission class to determine if the requesting user is the owner of the object.

    This permission class checks if the requesting user is the owner of the object being accessed.
    If the request method is safe (GET, HEAD, OPTIONS), access is allowed.
    Otherwise, access is only granted if the requesting user is the owner of the object.

    Attributes:
        message (str): The error message returned when permission is denied.
    """

    message = "You do not have permission to perform this action."

    def has_object_permission(self, request, view, obj):
        """
        Method to determine if the requesting user has permission to access the object.

        Args:
            request: The incoming request.
            view: The view handling the request.
            obj: The object being accessed.

        Returns:
            bool: True if permission is granted, False otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.email == request.user
