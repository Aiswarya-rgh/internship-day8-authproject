from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .ai_models import AIInterviewSession
from .models import (
    AIQuestionTemplate,
    AIAnswerEvaluation,
)

from .question_service import QuestionFlowService
from .scoring_engine import AIScoringEngine
from .serializers import AIAnswerEvaluationSerializer


class StartInterviewAPIView(APIView):
    """
    Returns the first/current interview question
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):

        try:

            session = AIInterviewSession.objects.get(
                session_id=session_id
            )

        except AIInterviewSession.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Interview Session Not Found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        question = QuestionFlowService.get_current_question(session)

        if question is None:

            return Response(
                {
                    "success": True,
                    "completed": True,
                    "message": "Interview Completed."
                }
            )

        return Response(
            {
                "success": True,
                "completed": False,
                "session_id": session.session_id,
                "question_id": question.id,
                "question": question.question
            }
        )


class SubmitAnswerAPIView(APIView):
    """
    Stores answer and evaluates it.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            session = AIInterviewSession.objects.get(
                id=request.data["session"]
            )

        except AIInterviewSession.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Session Not Found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:

            question = AIQuestionTemplate.objects.get(
                id=request.data["question"]
            )

        except AIQuestionTemplate.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Question Not Found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        answer = request.data["raw_answer"]

        scores = AIScoringEngine.calculate_scores(answer)

        evaluation = AIAnswerEvaluation.objects.create(

            session=session,

            question=question,

            raw_answer=answer,

            confidence_score=95,

            ai_annotation="AI evaluated successfully.",

            relevance_score=scores["relevance"],

            completeness_score=scores["completeness"],

            keyword_score=scores["keyword"],

            final_score=scores["final"]

        )

        serializer = AIAnswerEvaluationSerializer(evaluation)

        return Response(
            {
                "success": True,
                "message": "Answer Evaluated Successfully.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class RetrieveScoreAPIView(APIView):
    """
    Returns all evaluated answers for one interview.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):

        evaluations = AIAnswerEvaluation.objects.filter(
            session__id=session_id
        )

        serializer = AIAnswerEvaluationSerializer(
            evaluations,
            many=True
        )

        return Response(
            {
                "success": True,
                "count": evaluations.count(),
                "results": serializer.data
            }
        )


class NextQuestionAPIView(APIView):
    """
    Returns the next interview question.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):

        try:

            session = AIInterviewSession.objects.get(
                session_id=session_id
            )

        except AIInterviewSession.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Session Not Found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        question = QuestionFlowService.next_question(session)

        if question is None:

            return Response(
                {
                    "success": True,
                    "completed": True,
                    "message": "Interview Completed."
                }
            )

        return Response(
            {
                "success": True,
                "completed": False,
                "question_id": question.id,
                "question": question.question
            }
        )