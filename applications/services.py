from django.db.models import Case, When, Value, IntegerField

from .models import Application


class PremiumCandidateRankingService:

    @staticmethod
    def get_ranked_candidates(job):
        """
        Return candidates ranked by ATS score.

        Higher ATS score = higher ranking.
        """

        applications = (
            Application.objects
            .filter(job=job)
            .select_related("candidate")
            .order_by("-ats_score", "created_at")
        )

        ranked_candidates = []

        for rank, application in enumerate(applications, start=1):
            ranked_candidates.append({
                "rank": rank,
                "application_id": application.id,
                "candidate_id": application.candidate.id,
                "ats_score": application.ats_score,
                "status": application.status,
            })

        return ranked_candidates