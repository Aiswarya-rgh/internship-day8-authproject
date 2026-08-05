from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Application,InterviewSchedule
from .serializers import InterviewScheduleSerializer
from .scheduling_service import InterviewSchedulingService


class ScheduleInterviewAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        application_id = request.data.get("application")

        try:

            application = Application.objects.get(
                id=application_id
            )

        except Application.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Application not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        schedule = InterviewSchedulingService.schedule_interview(
            application
        )

        if schedule is None:

            return Response(
                {
                    "success": False,
                    "message": "No available interview slots."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = InterviewScheduleSerializer(schedule)

        return Response(
            {
                "success": True,
                "message": "Interview scheduled successfully.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

class RescheduleInterviewAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        schedule_id = request.data.get("schedule")

        try:

            schedule = InterviewSchedule.objects.get(
                id=schedule_id
            )

        except InterviewSchedule.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Interview schedule not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        updated_schedule = InterviewSchedulingService.reschedule_interview(
            schedule
        )

        if updated_schedule is None:

            return Response(
                {
                    "success": False,
                    "message": "No alternate interview slots available."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = InterviewScheduleSerializer(updated_schedule)

        return Response(
            {
                "success": True,
                "message": "Interview rescheduled successfully.",
                "data": serializer.data
            }
        )

class ConfirmInterviewAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        schedule_id = request.data.get("schedule")

        try:

            schedule = InterviewSchedule.objects.get(
                id=schedule_id
            )

        except InterviewSchedule.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Interview schedule not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        schedule.confirmation_status = True
        schedule.save()

        serializer = InterviewScheduleSerializer(schedule)

        return Response(
            {
                "success": True,
                "message": "Interview confirmed successfully.",
                "data": serializer.data
            }
        )