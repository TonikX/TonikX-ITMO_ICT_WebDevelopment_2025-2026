from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Airport, Company, Plane, Flight, Seat, Passenger, Ticket, CrewMember, Crew
from .serializers import *
from django.db.models import Count


# Feature views
@api_view(['GET'])
def mark_top(request):
    """
    Get the most popular plane mark.
    
    Returns the mark of the plane that appears most frequently in the database.
    
    Responses:
        200: Successfully retrieved the top mark
        500: Internal server error
    """
    mark_counts = Plane.objects.values('mark').annotate(count=Count('mark')).order_by('-count')
    
    if mark_counts:
        top_mark = mark_counts[0]['mark']
    else:
        top_mark = "No planes found"
    
    serializer = MarkTopSerializer({'top_mark': top_mark})
    return Response(serializer.data)

@api_view(['GET'])
def mark_all(request):
    """
    Get all plane marks and their counts.
    
    Returns a list of all plane marks along with the count of planes for each mark,
    and the total count of all planes.
    
    Responses:
        200: Successfully retrieved all marks and counts
        500: Internal server error
    """
    mark_counts = Plane.objects.values('mark').annotate(count_boards=Count('mark'))

    marks_data = [
        {'mark': item['mark'], 'count_boards': item['count_boards']}
        for item in mark_counts
    ]
    
    count_boards = sum(item['count_boards'] for item in marks_data)
    
    serializer = MarkAllSerializer(marks_data, many=True)
    return Response({
        'marks': serializer.data,
        'count_boards': count_boards
    })

@api_view(['POST'])
def routes_pick(request):
    """
    Get flights with occupancy below a specified threshold.
    
    Accepts an optional 'filled_less_than' parameter (float between 0 and 1) to filter flights
    by their occupancy ratio. Returns flights with occupancy below the specified threshold.
    
    Request Body:
        filled_less_than (float, optional): Occupancy threshold (0.0 to 1.0)
        
    Responses:
        200: Successfully retrieved flights
        400: Invalid request data
        500: Internal server error
    """
    serializer = RoutesPickSerializer(data=request.data)
    if serializer.is_valid():
        filled_less_than = serializer.validated_data.get('filled_less_than')
        
        flights = Flight.objects.all()
        
        if filled_less_than is not None:
            filtered_flights = []
            for flight in flights:
                total_seats = Seat.objects.filter(flight=flight).count()
                
                booked_seats = Seat.objects.filter(flight=flight, is_booked=True).count()
                
                if total_seats > 0:
                    occupancy_ratio = booked_seats / total_seats
                else:
                    occupancy_ratio = 0
                
                if occupancy_ratio < filled_less_than:
                    filtered_flights.append(flight)
            
            flights = filtered_flights
        
        flight_serializer = FlightSerializer(flights, many=True)
        return Response({'flights': flight_serializer.data})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def flights_available_seats(request, id):
    """
    Get available seats for a specific flight.
    
    Returns a list of available seat numbers for the specified flight ID.
    
    Path Parameters:
        id (int): The ID of the flight
        
    Responses:
        200: Successfully retrieved available seats
        404: Flight not found
        500: Internal server error
    """
    try:
        flight = Flight.objects.get(id=id)

        available_seats = Seat.objects.filter(flight=flight, is_booked=False)
        seat_numbers = [int(seat.seat_number) for seat in available_seats]
        serializer = AvailableSeatsSerializer({'available_seats': seat_numbers})
        return Response(serializer.data)
    except Flight.DoesNotExist:
        return Response({'error': 'Flight not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def planes_in_repair(request):
    """
    Get all planes that are currently in repair.
    
    Returns a list of planes with status 'repair'.
    
    Responses:
        200: Successfully retrieved planes in repair
        500: Internal server error
    """
    planes = Plane.objects.filter(status='repair')
    serializer = PlanesInRepairSerializer(planes, many=True)
    return Response({'planes': serializer.data})

@api_view(['GET'])
def employees_count(request):
    """
    Get the total count of employees (crew members).
    
    Returns the total number of crew members in the database.
    
    Responses:
        200: Successfully retrieved employee count
        500: Internal server error
    """
    count = CrewMember.objects.count()
    serializer = EmployeesCountSerializer({'employees_count': count})
    return Response(serializer.data)
