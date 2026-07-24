from locust import HttpUser, task, between


class JobPortalUser(HttpUser):

    wait_time = between(1, 3)

    @task
    def public_jobs(self):

        self.client.get("/api/jobs/public/")