from .models import AuditLog
import logging

class AuditLogService:

    @staticmethod
    def log(
        event_type,
        action,
        status="SUCCESS",
        user=None,
        description=None,
        failure_reason=None,
        ip_address=None,
        endpoint=None,
    ):
        return AuditLog.objects.create(
            event_type=event_type,
            action=action,
            status=status,
            user=user,
            description=description,
            failure_reason=failure_reason,
            ip_address=ip_address,
            endpoint=endpoint,
        )

    @staticmethod
    def application(
        action,
        user=None,
        description=None,
        status="SUCCESS",
    ):
        return AuditLogService.log(
            event_type="APPLICATION",
            action=action,
            status=status,
            user=user,
            description=description,
        )

    @staticmethod
    def ai_event(
        action,
        user=None,
        description=None,
        status="SUCCESS",
    ):
        return AuditLogService.log(
            event_type="AI",
            action=action,
            status=status,
            user=user,
            description=description,
        )

    @staticmethod
    def error(
        action,
        exception,
        user=None,
        endpoint=None,
    ):
        return AuditLogService.log(
            event_type="ERROR",
            action=action,
            status="FAILED",
            user=user,
            description=str(exception),
            failure_reason=str(exception),
            endpoint=endpoint,
        )

    @staticmethod
    def retry(
        action,
        failure_reason,
        user=None,
    ):
        return AuditLogService.log(
            event_type="RETRY",
            action=action,
            status="FAILED",
            user=user,
            failure_reason=failure_reason,
        )

    @staticmethod
    def security(
        action,
        user=None,
        ip_address=None,
        endpoint=None,
        description=None,
    ):
        return AuditLogService.log(
            event_type="SECURITY",
            action=action,
            status="FAILED",
            user=user,
            ip_address=ip_address,
            endpoint=endpoint,
            description=description,
        )

    @staticmethod
    def user_action(
        action,
        user=None,
        description=None,
    ):
        return AuditLogService.log(
            event_type="USER",
            action=action,
            user=user,
            description=description,
        )

    @staticmethod
    def admin_action(
        action,
        user=None,
        description=None,
    ):
        return AuditLogService.log(
            event_type="ADMIN",
            action=action,
            user=user,
            description=description,
        )
from .models import AuditLog


logger = logging.getLogger("audit_logs")


class AuditLogService:

    @staticmethod
    def log_error(action, description="", failure_reason=""):
        logger.error(
            "%s | %s",
            action,
            failure_reason
        )

        return AuditLog.objects.create(
            event_type="ERROR",
            action=action,
            status="Failed",
            description=description,
            failure_reason=failure_reason,
        )