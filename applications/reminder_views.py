from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import ReminderLog
from .serializers import ReminderLogSerializer


class ReminderLogAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        logs = ReminderLog.objects.all().order_by("-sent_at")

        serializer = ReminderLogSerializer(
            logs,
            many=True
        )

        return Response(
            {
                "success": True,
                "count": logs.count(),
                "results": serializer.data
            }
        )