from rest_framework import serializers

class ForecastRequestSerializer(serializers.Serializer):
    country = serializers.CharField(max_length=100)
    prediction_date = serializers.DateField()