import time
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class AIBridgeService:

    def generate_interview_question(self, prompt):

        retries = 3

        while retries > 0:

            try:

                print("Calling AI...")

                return {
                    "status": "success",
                    "question": "Tell me about yourself."
                }

            except Exception:

                retries -= 1

                print(f"Retrying AI API... ({retries} retries left)")
                time.sleep(2)

        return {
            "status": "failed",
            "message": "AI Service Unavailable"
        }

    def trigger_voice_call(
        self,
        phone_number,
        candidate_name,
        language="English",
        voice="Female"
    ):
        """
        Placeholder for future Voice Call API integration
        (Twilio / Exotel / Plivo etc.)
        """

        print("===================================")
        print("Triggering AI Voice Interview Call")
        print(f"Candidate : {candidate_name}")
        print(f"Phone     : {phone_number}")
        print(f"Language  : {language}")
        print(f"Voice     : {voice}")
        print("===================================")

        return {
            "status": "success",
            "message": "Voice call triggered successfully.",
            "candidate": candidate_name,
            "phone_number": phone_number,
            "language": language,
            "voice": voice
        }