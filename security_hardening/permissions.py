from rest_framework.permissions import BasePermission


class IsEmployerRole(BasePermission):
    message = "Employer access required."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "Employer"
        )


class IsCandidateRole(BasePermission):
    message = "Candidate access required."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "Candidate"
        )


class IsAdminRole(BasePermission):
    message = "Admin access required."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "Admin"
        )