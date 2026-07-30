from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .ai_models import AIInterviewSession


class SaveTranscriptAPIView(APIView):

    def post(self, request):

        session_id = request.data.get("session_id")

        transcript = request.data.get("transcript")

        try:

            session = AIInterviewSession.objects.get(
                session_id=session_id
            )

        except AIInterviewSession.DoesNotExist:

            return Response(
                {
                    "message": "Session not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        session.transcript = transcript
        session.save()

        return Response(
            {
                "message": "Transcript saved successfully.",
                "transcript": session.transcript
            }
        )