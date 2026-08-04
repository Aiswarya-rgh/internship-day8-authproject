class AIScoringEngine:

    @staticmethod
    def calculate_scores(answer):

        answer = answer.lower()

        # ---------- Relevance ----------

        relevance = 90 if len(answer) > 20 else 60

        # ---------- Completeness ----------

        completeness = min(len(answer) * 2, 100)

        # ---------- Keyword Matching ----------

        keywords = [
            "python",
            "django",
            "api",
            "database",
            "jwt"
        ]

        matched = 0

        for keyword in keywords:

            if keyword in answer:

                matched += 1

        keyword_score = (matched / len(keywords)) * 100

        # ---------- Weighted Score ----------

        final_score = (

            relevance * 0.50 +

            completeness * 0.30 +

            keyword_score * 0.20

        )

        return {

            "relevance": round(relevance, 2),

            "completeness": round(completeness, 2),

            "keyword": round(keyword_score, 2),

            "final": round(final_score, 2)

        }