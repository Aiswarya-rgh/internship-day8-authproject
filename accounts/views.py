from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import CustomUser,Employer,Candidate
from .serializers import (RegisterSerializer,EmployerProfileSerializer,CandidateProfileSerializer)
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
#day11 Employer,candidate profile management

class EmployerProfileAPIView(APIView):

    permission_classes = [IsAuthenticated, IsEmployer]

    def get(self, request):
        profile = request.user.employer_profile
        serializer = EmployerProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = request.user.employer_profile
        serializer = EmployerProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def delete(self, request):
        profile = request.user.employer_profile
        profile.delete()

        return Response({
            "message": "Employer profile deleted successfully."
        })

class CandidateProfileAPIView(APIView):

    permission_classes = [IsAuthenticated, IsCandidate]

    def get(self, request):
        profile = request.user.candidate_profile
        serializer = CandidateProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = request.user.candidate_profile
        serializer = CandidateProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def delete(self, request):
        profile = request.user.candidate_profile
        profile.delete()

        return Response({
            "message": "Candidate profile deleted successfully."
        })    
