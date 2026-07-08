from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import CustomUser,Employer,Candidate
from .serializers import (RegisterSerializer,EmployerProfileSerializer,CandidateProfileSerializer,ResumeUploadSerializer,CandidateListSerializer,UserListSerializer)
from .permissions import IsAdmin, IsEmployer, IsCandidate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


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
#RESUME UPLOAD SERIALIZER
class ResumeUploadAPIView(APIView):
    permission_classes = [IsAuthenticated,IsCandidate]

    def put(self,request):
        profile = request.user.candidate_profile
        serializer = ResumeUploadSerializer(
            profile,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "Resume uploaded successfully.",
                "data": serializer.data
            })

        return Response(serializer.errors)
#PAGINATION CANDIDATELIST
class CandidateListAPIView(generics.ListAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateListSerializer
    permission_classes = [IsAuthenticated]
#filtering by role
class UserListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class =  UserListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ["role","created_at","is_verified"]
    search_fields = ["username","email"]