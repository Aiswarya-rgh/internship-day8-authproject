from .services import AuditLogService


class AuditLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        try:
            response = self.get_response(request)

            # Log unauthorized / forbidden requests
            if response.status_code in [401, 403]:
                user = (
                    request.user
                    if getattr(request.user, "is_authenticated", False)
                    else None
                )

                AuditLogService.security(
                    action="Unauthorized access attempt",
                    user=user,
                    ip_address=self.get_client_ip(request),
                    endpoint=request.path,
                    description=f"HTTP {response.status_code}",
                )

            return response

        except Exception as exc:

            user = (
                request.user
                if getattr(request.user, "is_authenticated", False)
                else None
            )

            AuditLogService.error(
                action="Unhandled application exception",
                exception=exc,
                user=user,
                endpoint=request.path,
            )

            raise

    @staticmethod
    def get_client_ip(request):

        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")

        if forwarded:
            return forwarded.split(",")[0].strip()

        return request.META.get("REMOTE_ADDR")