

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import CustomUser


class AuthenticationTests(APITestCase):

    def setUp(self):

        self.signup_url = "/api/signup/"

        self.user_data = {

            "username": "candidate1",

            "email": "candidate1@gmail.com",

            "phone": "9876543210",

            "role": "Candidate",

            "password": "Candidate@123"

        }

    def test_user_registration(self):

        response = self.client.post(

            self.signup_url,

            self.user_data,

            format="json"

        )

        self.assertEqual(

            response.status_code,

            status.HTTP_201_CREATED

        )

        self.assertTrue(

            CustomUser.objects.filter(

                username="candidate1"

            ).exists()

        )

    def test_user_login(self):

      CustomUser.objects.create_user(

        username="candidate1",

        email="candidate1@gmail.com",

        phone="9876543210",

        role="Candidate",

        password="Candidate@123"

       )

      response = self.client.post(

        "/api/login/",

        {

            "username": "candidate1",

            "password": "Candidate@123"

        },

        format="json"

    )

      self.assertEqual(

        response.status_code,

        status.HTTP_200_OK

    )

      self.assertIn(

        "access",

        response.data

    )

      self.assertIn(

        "refresh",

        response.data

    )
    def test_invalid_login(self):

     CustomUser.objects.create_user(

        username="candidate1",

        email="candidate1@gmail.com",

        phone="9876543210",

        role="Candidate",

        password="Candidate@123"

    )

     response = self.client.post(

        "/api/login/",

        {

            "username": "candidate1",

            "password": "WrongPassword"

        },

        format="json"

    )


     self.assertEqual(

        response.status_code,

        status.HTTP_401_UNAUTHORIZED

    )

    def test_profile_access(self):

     user = CustomUser.objects.create_user(

        username="candidate1",

        email="candidate1@gmail.com",

        phone="9876543210",

        role="Candidate",

        password="Candidate@123"

    )

     login = self.client.post(

        "/api/login/",

        {

            "username": "candidate1",

            "password": "Candidate@123"

        },

        format="json"

    )

     token = login.data["access"]

     self.client.credentials(

        HTTP_AUTHORIZATION=f"Bearer {token}"

    )

     response = self.client.get(

        "/api/profile/"

    )

     self.assertEqual(

        response.status_code,

        status.HTTP_200_OK

    )

     self.assertEqual(

        response.data["username"],

        "candidate1"

    )

     self.assertEqual(

        response.data["role"],

        "Candidate"

    )
    def test_candidate_cannot_access_employer_dashboard(self):

     CustomUser.objects.create_user(

        username="candidate1",

        email="candidate1@gmail.com",

        phone="9876543210",

        role="Candidate",

        password="Candidate@123"

    )

     login = self.client.post(

        "/api/login/",

        {

            "username": "candidate1",

            "password": "Candidate@123"

        },

        format="json"

    )

     token = login.data["access"]

     self.client.credentials(

        HTTP_AUTHORIZATION=f"Bearer {token}"

    )

     response = self.client.get(

        "/api/employer/"

    )

     self.assertEqual(

        response.status_code,

        status.HTTP_403_FORBIDDEN

    )
    def test_employer_can_access_employer_dashboard(self):

     CustomUser.objects.create_user(

        username="employer1",

        email="employer1@gmail.com",

        phone="9876543210",

        role="Employer",

        password="Employer@123"

    )

     login = self.client.post(

        "/api/login/",

        {

            "username": "employer1",

            "password": "Employer@123"

        },

        format="json"

    )

     token = login.data["access"]

     self.client.credentials(

        HTTP_AUTHORIZATION=f"Bearer {token}"

    )

     response = self.client.get(

        "/api/employer/"

    )

     self.assertEqual(

        response.status_code,

        status.HTTP_200_OK

    )