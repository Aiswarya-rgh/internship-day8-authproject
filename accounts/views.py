from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import AdminAuditLog

from .models import CustomUser,Employer,Candidate
from .serializers import (RegisterSerializer,EmployerProfileSerializer,CandidateProfileSerializer,ResumeUploadSerializer,CandidateListSerializer,UserListSerializer,AdminAuditLogSerializer)
from .permissions import IsAdmin, IsEmployer, IsCandidate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .utils import extract_resume_text
from accounts.permissions import IsCandidate
from .utils import (
    extract_resume_text,
    clean_resume_text
)


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

class ApproveEmployerAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, pk):

        try:
            employer = Employer.objects.get(pk=pk)
        except Employer.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Employer not found."
                },
                status=404
            )

        employer.is_company_verified = True
        employer.save()
       

        AdminAuditLog.objects.create(
        admin=request.user,
        action=f"Approved employer {employer.user.email}"
         )
        

        return Response(
            {
                "success": True,
                "message": "Employer approved successfully."
            }
        )
from .models import CustomUser


class BlockUserAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, pk):

        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "User not found."
                },
                status=404
            )

        user.is_active = False
        user.save()

        AdminAuditLog.objects.create(
        admin=request.user,
        action=f"Blocked user {user.email}"
         )
        return Response(
            {
                "success": True,
                "message": "User blocked successfully."
            }
        )
class FlagUserAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, pk):

        try:
            user = CustomUser.objects.get(pk=pk)

        except CustomUser.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "User not found."
                },
                status=404
            )

        user.is_flagged = True
        user.save()

        AdminAuditLog.objects.create(
        admin=request.user,
        action=f"Flagged user {user.email}"
         )

        return Response(
            {
                "success": True,
                "message": "User flagged successfully."
            }
        )
class AdminAuditLogAPIView(generics.ListAPIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    serializer_class = AdminAuditLogSerializer

    queryset = AdminAuditLog.objects.all().order_by("-created_at")
class ResumeTextAPIView(APIView):

    permission_classes = [IsAuthenticated, IsCandidate]

    def get(self, request):

        candidate = request.user.candidate_profile

        if not candidate.resume:
            return Response(
                {
                    "success": False,
                    "message": "Resume not uploaded."
                },
                status=404
            )

        file_path = candidate.resume.path

        extracted_text = extract_resume_text(file_path)

        cleaned_text = clean_resume_text(extracted_text)

        return Response(
       {
        "success": True,
        "message": "Resume text extracted successfully.",
        "resume_text": cleaned_text
        }
)