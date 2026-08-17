from django.db.models import Count, Avg, Q
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

    @staticmethod
    def get_advanced_recruiter_analytics(employer):
        """
        Premium recruiter analytics.

        Calculates:
        - total applications
        - shortlisted candidates
        - interviews
        - selected candidates
        - average ATS score
        - hiring efficiency
        - selection success rate
        """

        applications = Application.objects.filter(
            job__employer=employer
        )

        total_applications = applications.count()

        shortlisted = applications.filter(
            status=Application.SHORTLISTED
        ).count()

        interviewed = applications.filter(
            status=Application.INTERVIEW
        ).count()

        selected = applications.filter(
            status=Application.SELECTED
        ).count()

        avg_ats_score = applications.aggregate(
            average=Avg("ats_score")
        )["average"]

        hiring_efficiency = (
            round(
                (selected / total_applications) * 100,
                2
            )
            if total_applications
            else 0
        )

        selection_success_rate = (
            round(
                (selected / interviewed) * 100,
                2
            )
            if interviewed
            else 0
        )

        return {
            "total_applications": total_applications,
            "shortlisted_candidates": shortlisted,
            "interviews": interviewed,
            "selected_candidates": selected,
            "average_ats_score": round(
                avg_ats_score,
                2
            ) if avg_ats_score is not None else 0,
            "hiring_efficiency": hiring_efficiency,
            "selection_success_rate": selection_success_rate,
        }
    @staticmethod
    def get_hiring_efficiency_metrics(employer):
        """
        Calculate hiring efficiency metrics for one recruiter/employer.
        """

        applications = Application.objects.filter(
            job__employer=employer
        )

        total = applications.count()

        shortlisted = applications.filter(
            status=Application.SHORTLISTED
        ).count()

        interviewed = applications.filter(
            status=Application.INTERVIEW
        ).count()

        selected = applications.filter(
            status=Application.SELECTED
        ).count()

        rejected = applications.filter(
            status=Application.REJECTED
        ).count()

        avg_ats = applications.aggregate(
            average=Avg("ats_score")
        )["average"]

        return {
            "total_applications": total,
            "shortlisted": shortlisted,
            "interviewed": interviewed,
            "selected": selected,
            "rejected": rejected,
            "average_ats_score": (
                round(float(avg_ats), 2)
                if avg_ats is not None
                else 0
            ),
            "shortlist_rate": (
                round((shortlisted / total) * 100, 2)
                if total else 0
            ),
            "interview_rate": (
                round((interviewed / total) * 100, 2)
                if total else 0
            ),
            "selection_rate": (
                round((selected / total) * 100, 2)
                if total else 0
            ),
            "hiring_efficiency": (
                round((selected / total) * 100, 2)
                if total else 0
            ),
        }


    @staticmethod
    def get_candidate_success_predictions(employer):
        """
        Estimate candidate success using ATS score and
        current application status.

        This is a rule-based prediction using the data
        currently available in Application.
        """

        applications = (
            Application.objects
            .select_related(
                "candidate",
                "candidate__user",
                "job",
            )
            .filter(
                job__employer=employer
            )
            .order_by("-ats_score")
        )

        results = []

        for application in applications:

            ats_score = float(
                application.ats_score or 0
            )

            if application.status == Application.SELECTED:
                probability = 100
                prediction = "Successful"

            elif ats_score >= 80:
                probability = 85
                prediction = "High Success Potential"

            elif ats_score >= 60:
                probability = 65
                prediction = "Moderate Success Potential"

            elif ats_score >= 40:
                probability = 45
                prediction = "Low Success Potential"

            else:
                probability = 25
                prediction = "Very Low Success Potential"

            results.append({
                "application_id": application.id,
                "candidate": (
                    application.candidate.user.email
                ),
                "job": application.job.title,
                "status": application.status,
                "ats_score": ats_score,
                "success_probability": probability,
                "prediction": prediction,
            })

        return results