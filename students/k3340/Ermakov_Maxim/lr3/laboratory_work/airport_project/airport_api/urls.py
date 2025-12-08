from django.urls import path
from .views import (
    AirportListCreateView, AirportDetailView,
    CompanyListCreateView, CompanyDetailView,
    PlaneTypeListCreateView, PlaneTypeDetailView,
    PlaneListCreateView, PlaneDetailView,
    RouteListCreateView, RouteDetailView,
    FlightListCreateView, FlightDetailView,
    FlightInstanceListCreateView, FlightInstanceDetailView,
    TransitStopListCreateView, TransitStopDetailView,
    PassengerListCreateView, PassengerDetailView,
    SeatListCreateView, SeatDetailView,
    TicketListCreateView, TicketDetailView,
    CrewMemberListCreateView, CrewMemberDetailView,
    CrewListCreateView, CrewDetailView, RouteWithFlightsView, FlightInstanceWithCrewView, RouteTopPlaneTypeView,
    UnderfilledRoutesView, FlightInstanceFreeSeatsView, PlanesInMaintenanceView, CompanyEmployeesCountView,
    CompanyPlanesReportView,
)

app_name = "airport_api"

urlpatterns = [
    # AIRPORT
    path("airports/", AirportListCreateView.as_view()),
    path("airports/<str:pk>/", AirportDetailView.as_view()),

    # COMPANY
    path("companies/", CompanyListCreateView.as_view()),
    path("companies/<int:pk>/", CompanyDetailView.as_view()),

    # PLANE TYPE
    path("plane-types/", PlaneTypeListCreateView.as_view()),
    path("plane-types/<int:pk>/", PlaneTypeDetailView.as_view()),

    # PLANE
    path("planes/", PlaneListCreateView.as_view()),
    path("planes/<int:pk>/", PlaneDetailView.as_view()),

    # ROUTE
    path("routes/", RouteListCreateView.as_view()),
    path("routes/<int:pk>/", RouteDetailView.as_view()),

    # FLIGHT
    path("flights/", FlightListCreateView.as_view()),
    path("flights/<int:pk>/", FlightDetailView.as_view()),

    # FLIGHT INSTANCE
    path("flight-instances/", FlightInstanceListCreateView.as_view()),
    path("flight-instances/<int:pk>/", FlightInstanceDetailView.as_view()),

    # TRANSIT STOP
    path("transit-stops/", TransitStopListCreateView.as_view()),
    path("transit-stops/<int:pk>/", TransitStopDetailView.as_view()),

    # PASSENGER
    path("passengers/", PassengerListCreateView.as_view()),
    path("passengers/<int:pk>/", PassengerDetailView.as_view()),

    # SEAT
    path("seats/", SeatListCreateView.as_view()),
    path("seats/<int:pk>/", SeatDetailView.as_view()),

    # TICKET
    path("tickets/", TicketListCreateView.as_view()),
    path("tickets/<int:pk>/", TicketDetailView.as_view()),

    # CREW MEMBER
    path("crew-members/", CrewMemberListCreateView.as_view()),
    path("crew-members/<int:pk>/", CrewMemberDetailView.as_view()),

    # CREW
    path("crew/", CrewListCreateView.as_view()),
    path("crew/<int:pk>/", CrewDetailView.as_view()),

    path("routes/<int:pk>/with-flights/", RouteWithFlightsView.as_view()),

    path("flight-instances/<int:pk>/with-crew/", FlightInstanceWithCrewView.as_view()),

    path("routes/<int:pk>/top-plane-type/", RouteTopPlaneTypeView.as_view()),

    path("analytics/underfilled-routes/", UnderfilledRoutesView.as_view()),

    path("flight-instances/<int:pk>/free-seats/", FlightInstanceFreeSeatsView.as_view()),

    path("analytics/planes-in-maintenance/", PlanesInMaintenanceView.as_view()),

    path("companies/<int:pk>/employees-count/", CompanyEmployeesCountView.as_view()),

    path("companies/<int:pk>/planes-report/", CompanyPlanesReportView.as_view()),

]
