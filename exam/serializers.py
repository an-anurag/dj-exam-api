from rest_framework import serializers

from .models import Question, Result


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'question', 'que_type']


class QuestionWithOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'question', 'que_type', 'selected_option']


class ResultSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()

    class Meta:
        model = Result
        fields = ['id', 'user', 'score', 'date_created', 'date_modified']
