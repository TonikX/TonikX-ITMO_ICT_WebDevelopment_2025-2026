from django.urls import path
from .views import *

urlpatterns = [
    path('alpinists/', AlpinistListCreateView.as_view()),
    path('mountains/', MountainListCreateView.as_view()),
    path('clubs/', ClubListCreateView.as_view()),
    path('routes/', RouteListCreateView.as_view()),

    path('climbs/', ClimbListView.as_view()), 
    path('climbs/create/', ClimbCreateView.as_view()),
    path('climbs/recent/',  RecentClimbsView.as_view()), 

    path('query/alpinists-by-date/', AlpinistsInDateRangeView.as_view()),
    path('query/mountain-stats/', MountainStatsView.as_view()),
    path('query/unclimbed/', UnclimbedMountainsView.as_view()),
    path('query/alpinist-mountain-stats/', AlpinistMountainClimbsView.as_view()),
    path('query/climbs-by-period/', ClimbListByPeriodView.as_view()),
    path('query/final-report/', MountainReportView.as_view()),
]