import time


class AIBridgeService:

    def generate_interview_question(self, prompt):

        retries = 3

        while retries > 0:

            try:

                print("Calling AI...")

                return {
                    "status":"success",
                    "question":"Tell me about yourself."
                }

            except Exception:

                retries -= 1

                time.sleep(2)

        return {
            "status":"failed",
            "message":"AI Service Unavailable"
        }