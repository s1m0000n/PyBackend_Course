from rest_framework import serializers
from .models import Function


class FunctionSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=1, max_length=128)
    call_spec = serializers.CharField(min_length=1, max_length=512)
    args = serializers.CharField(min_length=1)
    description = serializers.CharField(min_length=1)
    examples = serializers.CharField(min_length=1)

    def create(self, validated_data):
        return Function.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.call_spec = validated_data.get('call_spec', instance.call_spec)
        instance.args = validated_data.get('args', instance.args)
        instance.description = validated_data.get('description', instance.description)
        instance.examples = validated_data.get('examples', instance.examples)
        instance.save()
        return instance
