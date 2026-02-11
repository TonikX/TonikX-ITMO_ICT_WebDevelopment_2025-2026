from rest_framework import viewsets, permissions
from .models import Assignment, Submission, PeerReview
from .serializers import AssignmentSerializer, SubmissionSerializer, PeerReviewSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS: 
            return [IsAuthenticated()]
        return [IsAdminUser()] 

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)



class PeerReviewViewSet(viewsets.ModelViewSet):
    queryset = PeerReview.objects.all()
    serializer_class = PeerReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)