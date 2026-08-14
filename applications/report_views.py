from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from billing.permissions import HasAIAnalytics

from .models import Application
from .report_service import CandidateReportService


class CandidateReportAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        HasAIAnalytics,
    ]

    def get(self, request, application_id):

        try:
            application = Application.objects.get(id=application_id)

        except Application.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Application not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        report = CandidateReportService.generate_report(application)

        return Response(
            {
                "success": True,
                "report": report
            }
        )