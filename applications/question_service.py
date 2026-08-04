from .models import JobQuestionMapping


class QuestionFlowService:

    @staticmethod
    def get_questions(job):
        mappings = JobQuestionMapping.objects.filter(
            job=job
        ).order_by("order")

        return [mapping.question for mapping in mappings]

    @staticmethod
    def get_current_question(session):
        questions = QuestionFlowService.get_questions(session.job)

        if session.current_question_index >= len(questions):
            return None

        return questions[session.current_question_index]

    @staticmethod
    def next_question(session):
        session.current_question_index += 1
        session.save()

        return QuestionFlowService.get_current_question(session)