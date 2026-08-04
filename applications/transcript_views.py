from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .ai_models import AIInterviewSession
from .models import JobQuestionMapping


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

        # Save transcript
        session.transcript = transcript

        # Save latest candidate response
        if isinstance(transcript, dict):
            session.last_response = transcript.get("text", "")
        else:
            session.last_response = str(transcript)

        session.save()

        # Move to next question
        next_question = QuestionFlowService.next_question(session)

        # Check Interview Completion
        completed = InterviewFlow.is_completed(session)

        if completed:

            session.status = "Completed"
            session.save()

            return Response(
                {
                    "message": "Interview Completed Successfully.",
                    "completed": True,
                    "transcript": session.transcript
                }
            )

        return Response(
            {
                "message": "Transcript Saved Successfully.",
                "completed": False,
                "transcript": session.transcript,
                "next_question": next_question.question if next_question else None,
                "question_id": next_question.id if next_question else None
            }
        )


class QuestionFlowService:

    @staticmethod
    def get_questions(job):

        mappings = JobQuestionMapping.objects.filter(
            job=job
        ).order_by("order")

        return [mapping.question for mapping in mappings]

    @staticmethod
    def get_current_question(session):

        questions = QuestionFlowService.get_questions(session.job)

        if session.current_question_index >= len(questions):
            return None

        return questions[session.current_question_index]

    @staticmethod
    def next_question(session):

        session.current_question_index += 1
        session.save()

        return QuestionFlowService.get_current_question(session)


class InterviewFlow:

    @staticmethod
    def is_completed(session):

        return session.current_question_index >= session.max_questions