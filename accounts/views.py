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
from jobs.models import Job
from applications.models import Application

from .utils import (
    extract_resume_text,
    clean_resume_text,
    tokenize_text,
    extract_skills,
    extract_email,
    extract_phone,
    extract_experience,
    extract_role,
    extract_education,
    calculate_resume_score,
    calculate_match_score,
    get_role_threshold,
    get_application_status,


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

        # Extract Resume
        extracted_text = extract_resume_text(file_path)
        cleaned_text = clean_resume_text(extracted_text)

        print("\n========== EXTRACTED TEXT ==========")
        print(cleaned_text)
        print("====================================\n")

        # Tokenization
        tokens = tokenize_text(cleaned_text)
        print("TOKENS:", tokens)

        # Skill Extraction
        skills = extract_skills(tokens)
        print("SKILLS:", skills)

        # Other Resume Details
        email = extract_email(cleaned_text)
        phone = extract_phone(cleaned_text)
        experience = extract_experience(cleaned_text)
        role = extract_role(cleaned_text)
        education = extract_education(cleaned_text)

        resume_score = calculate_resume_score(
            skills,
            experience,
            education
        )

        job_id = request.query_params.get("job")
        match_result = None

        if job_id:

            try:

                job = Job.objects.get(id=job_id)

                job_skills = job.skills.split(",")

                match_result = calculate_match_score(
                    skills,
                    job_skills
                )
                application_status = get_application_status(
                     job,
                    match_result["match_percentage"]
                )

                print("\n========== DEBUG ==========")
                print("Logged Candidate ID:", request.user.candidate_profile.id)
                print("Requested Job ID:", job.id)

                print("All Applications:")
                print(
                    list(
                        Application.objects.values(
                            "id",
                            "candidate_id",
                            "job_id",
                            "ats_score"
                        )
                    )
                )

                try:

                    application = Application.objects.get(
                        candidate=request.user.candidate_profile,
                        job=job
                    )

                    print("Before Save:", application.ats_score)

                    application.ats_score = match_result["match_percentage"]
                    application.status = application_status
                    application.save()

                    if application_status == "Shortlisted":
                       notification = "Congratulations! You have been shortlisted."

                    elif application_status == "Rejected":
                        notification = "Your application was rejected based on ATS score."

                    else:
                      notification = "Your application is under review."

                    application.refresh_from_db()

                    print("After Save:", application.ats_score)

                except Application.DoesNotExist:

                    print("Application Not Found")

                print("===========================\n")

            except Job.DoesNotExist:

                match_result = {
                    "error": "Job not found."
                }

        return Response(
            {
                "success": True,
                "message": "Resume parsed successfully.",
                "notification": notification,

                "resume": {
                    "email": email,
                    "phone": phone,
                    "role": role,
                    "education": education,
                    "experience": experience,
                    "resume_score": resume_score,
                    "job_match": match_result,
                    "application_status": application_status,

                    "skills": {
                        "count": len(skills),
                        "matched_skills": skills
                    }
                }
            }
        )