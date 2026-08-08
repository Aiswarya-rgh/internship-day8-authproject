from django.db.models import Count, Avg
from django.core.cache import cache

from applications.models import Application


class AnalyticsService:

    @staticmethod
    def get_funnel_metrics():

        cache_key = "analytics_funnel"

        data = cache.get(cache_key)

        if data:
            return data

        data = {
            "Applied": Application.objects.filter(
                status=Application.APPLIED
            ).count(),

            "Shortlisted": Application.objects.filter(
                status=Application.SHORTLISTED
            ).count(),

            "Interview Scheduled": Application.objects.filter(
                status=Application.INTERVIEW
            ).count(),

            "Selected": Application.objects.filter(
                status=Application.SELECTED
            ).count(),
        }

        cache.set(cache_key, data, timeout=300)

        return data

    @staticmethod
    def get_job_performance():

        return (
            Application.objects
            .select_related("job")
            .values("job__title")
            .annotate(

                total_applications=Count("id"),

                avg_ats_score=Avg("ats_score"),

                shortlisted=Count(
                    "id",
                    filter=None
                ),
            )
        )

    @staticmethod
    def get_conversion_ratio():

        applied = Application.objects.filter(
            status=Application.APPLIED
        ).count()

        shortlisted = Application.objects.filter(
            status=Application.SHORTLISTED
        ).count()

        interviewed = Application.objects.filter(
            status=Application.INTERVIEW
        ).count()

        selected = Application.objects.filter(
            status=Application.SELECTED
        ).count()

        return {

            "Applied_to_Shortlisted":
                round((shortlisted / applied) * 100, 2)
                if applied else 0,

            "Shortlisted_to_Interview":
                round((interviewed / shortlisted) * 100, 2)
                if shortlisted else 0,

            "Interview_to_Selected":
                round((selected / interviewed) * 100, 2)
                if interviewed else 0,
        }

    @staticmethod
    def get_time_based_stats():

        return (
            Application.objects
            .values("applied_at__date")
            .annotate(total=Count("id"))
            .order_by("applied_at__date")
        )

    @staticmethod
    def get_role_based_metrics():

        return (
            Application.objects
            .select_related("job")
            .values("job__title")
            .annotate(

                applications=Count("id"),

                avg_ats_score=Avg("ats_score")
            )
        )