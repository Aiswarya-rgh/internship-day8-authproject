from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import CustomUser
from .serializers import RegisterSerializer
from .permissions import IsAdmin, IsEmployer, IsCandidate

class RegisterAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


class ProfileAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "username": request.user.username,
            "email": request.user.email,
            "role": request.user.role,
        })


class EmployerDashboard(APIView):

    permission_classes = [IsEmployer]

    def get(self, request):
        return Response({
            "message": "Employer can post jobs."
        })


class CandidateDashboard(APIView):

    permission_classes = [IsCandidate]

    def get(self, request):
        return Response({
            "message": "Candidate can apply for jobs."
        })


class AdminDashboard(APIView):

    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({
            "message": "Admin can control the system."
        })