from .permissions import get_active_subscription


class FeatureAccessService:

    @staticmethod
    def get_subscription(user):
        return get_active_subscription(user)

    @staticmethod
    def has_feature(user, feature_name):

        subscription = get_active_subscription(user)

        if not subscription:
            return False

        plan = subscription.plan

        return bool(
            getattr(plan, feature_name, False)
        )

    @staticmethod
    def can_post_job(user):

        subscription = get_active_subscription(user)

        if not subscription:
            return False

        plan = subscription.plan

        # Unlimited plans
        if getattr(plan, "unlimited_job_posts", False):
            return True

        # Limit checking will be added below.
        return True

    @staticmethod
    def can_access_candidates(user):

        subscription = get_active_subscription(user)

        if not subscription:
            return False

        plan = subscription.plan

        if getattr(plan, "unlimited_candidate_access", False):
            return True

        return True