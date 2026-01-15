from rest_framework import serializers
from .models import Assignment, Variant, GradingCriterion, Submission, PeerReview


class CriterionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradingCriterion
        fields = '__all__'


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True, read_only=True)
    criteria = CriterionSerializer(many=True, read_only=True)

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'teacher', 'variants', 'criteria']
        read_only_fields = ['teacher']

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ['student'] 


class PeerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeerReview
        fields = '__all__'
        read_only_fields = ['reviewer'] 