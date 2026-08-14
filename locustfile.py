from locust import HttpUser, task, between
import os


class JobPortalUser(HttpUser):

    wait_time = between(1, 3)

    def on_start(self):
        """
        Login once when each virtual user starts.
        """

        username = os.getenv("LOCUST_USERNAME")
        password = os.getenv("LOCUST_PASSWORD")

        self.token = None

        if not username or not password:
            print("LOCUST_USERNAME or LOCUST_PASSWORD is not set.")
            return

        response = self.client.post(
            "/api/login/",
            json={
                "username": username,
                "password": password,
            },
            name="Login",
        )

        if response.status_code == 200:
            data = response.json()
            self.token = data.get("access")

            if self.token:
                print("Locust login successful.")
            else:
                print("Login succeeded but no access token was returned.")

        else:
            print(
                f"Locust login failed: "
                f"{response.status_code} - {response.text}"
            )

    def auth_headers(self):
        """
        Headers used for protected APIs.
        """

        if self.token:
            return {
                "Authorization": f"Bearer {self.token}"
            }

        return {}

    # ==========================================
    # PUBLIC JOB API
    # ==========================================

    @task(5)
    def public_jobs(self):

        self.client.get(
            "/api/jobs/public/",
            name="Public Jobs"
        )

    # ==========================================
    # ACCOUNT / PROFILE APIs
    # ==========================================

    @task(3)
    def profile(self):

        self.client.get(
            "/api/profile/",
            headers=self.auth_headers(),
            name="Profile"
        )

    @task(2)
    def candidate_profile(self):

        self.client.get(
            "/api/candidate-profile/",
            headers=self.auth_headers(),
            name="Candidate Profile"
        )

    @task(2)
    def employer_profile(self):

        self.client.get(
            "/api/employer-profile/",
            headers=self.auth_headers(),
            name="Employer Profile"
        )

    # ==========================================
    # APPLICATION APIs
    # ==========================================

    @task(3)
    def application_history(self):

        self.client.get(
            "/api/applications/history/",
            headers=self.auth_headers(),
            name="Application History"
        )

    @task(3)
    def applied_jobs(self):

        self.client.get(
            "/api/applications/applied-jobs/",
            headers=self.auth_headers(),
            name="Applied Jobs"
        )

    @task(2)
    def saved_jobs(self):

        self.client.get(
            "/api/applications/saved-jobs/",
            headers=self.auth_headers(),
            name="Saved Jobs"
        )

    @task(2)
    def matching_jobs(self):

        self.client.get(
            "/api/applications/matching-jobs/",
            headers=self.auth_headers(),
            name="Matching Jobs"
        )

    @task(2)
    def skill_suggestions(self):

        self.client.get(
            "/api/applications/skill-suggestions/",
            headers=self.auth_headers(),
            name="Skill Suggestions"
        )

    @task(2)
    def timeline(self):

        self.client.get(
            "/api/applications/timeline/",
            headers=self.auth_headers(),
            name="Application Timeline"
        )

    @task(2)
    def notifications(self):

        self.client.get(
            "/api/applications/notifications/",
            headers=self.auth_headers(),
            name="Notifications"
        )

    @task(2)
    def interview_status(self):

        self.client.get(
            "/api/applications/interview-status/",
            headers=self.auth_headers(),
            name="Interview Status"
        )

    # ==========================================
    # ANALYTICS APIs
    # ==========================================

    @task(1)
    def analytics_funnel(self):

        self.client.get(
            "/api/analytics/funnel/",
            headers=self.auth_headers(),
            name="Analytics Funnel"
        )

    @task(1)
    def analytics_job_performance(self):

        self.client.get(
            "/api/analytics/job-performance/",
            headers=self.auth_headers(),
            name="Analytics Job Performance"
        )

    @task(1)
    def analytics_conversion(self):

        self.client.get(
            "/api/analytics/conversion/",
            headers=self.auth_headers(),
            name="Analytics Conversion"
        )

    @task(1)
    def analytics_time_stats(self):

        self.client.get(
            "/api/analytics/time-stats/",
            headers=self.auth_headers(),
            name="Analytics Time Stats"
        )

    @task(1)
    def analytics_role_metrics(self):

        self.client.get(
            "/api/analytics/role-metrics/",
            headers=self.auth_headers(),
            name="Analytics Role Metrics"
        )