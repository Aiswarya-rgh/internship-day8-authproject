from rest_framework import serializers


class FunnelSerializer(serializers.Serializer):

    Applied = serializers.IntegerField()

    Shortlisted = serializers.IntegerField()

    Interview_Scheduled = serializers.IntegerField(source="Interview Scheduled")

    Selected = serializers.IntegerField()