from rest_framework import serializers


# Serializers are very similar to django forms
class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing out APIView"""
    name = serializers.CharField(max_length=10)
