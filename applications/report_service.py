from django.db.models import Avg

from .models import (
    Application,
    AIInterviewSession,
    AIAnswerEvaluation,
)


class CandidateReportService:

    @staticmethod
    def generate_report(application):

        session = AIInterviewSession.objects.filter(
            candidate=application.candidate,
            job=application.job
        ).first()

        ats_score = application.ats_score

        ai_score = 0
        strengths = []
        risks = []

        if session:

            evaluations = AIAnswerEvaluation.objects.filter(
                session=session
            )

            average = evaluations.aggregate(
                Avg("final_score")
            )["final_score__avg"]

            ai_score = round(average or 0, 2)

            for evaluation in evaluations:

                if evaluation.final_score >= 8:
                    strengths.append(
                        evaluation.question.category
                    )

                if evaluation.final_score < 5:
                    risks.append(
                        evaluation.question.category
                    )

        return {

            "candidate": application.candidate.user.username,

            "job": application.job.title,

            "ats_score": ats_score,

            "ai_call_score": ai_score,

            "strengths": list(set(strengths)),

            "risks": list(set(risks))

        }