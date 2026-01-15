from django.contrib import admin
from .models import Assignment, Variant, GradingCriterion, Submission, PeerReview

admin.site.register(Assignment)
admin.site.register(Variant)
admin.site.register(GradingCriterion)
admin.site.register(Submission)
admin.site.register(PeerReview)