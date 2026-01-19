from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import JsonResponse

from .models import (
    Task, TaskFile, TaskLink, Team, TeamMember,
    Solution, Evaluation
)
from .serializers import (
    TaskSerializer, TaskDetailSerializer, TaskFileSerializer, TaskLinkSerializer,
    TaskFileCreateSerializer, TaskLinkCreateSerializer,
    TeamSerializer, TeamDetailSerializer, TeamMemberSerializer,
    SolutionListSerializer, SolutionDetailSerializer,
    EvaluationSerializer
)
from .permissions import (
    IsCaptain, IsCurator, IsJury, IsMainAdmin,
    IsTeamCaptain, IsTaskCurator, CanViewSolution,
    CanEvaluateSolution, CanCreateTask, CanAssignCurator
)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """Корневой endpoint с информацией об API"""
    return JsonResponse({
        'message': 'Hackathon API - Система для проведения хакатонов',
        'version': '1.0',
        'endpoints': {
            'authentication': {
                'register': '/api/auth/users/',
                'login': '/api/auth/token/login/',
                'me': '/api/auth/users/me/',
                'logout': '/api/auth/token/logout/'
            },
            'tasks': {
                'list': '/api/tasks/',
                'detail': '/api/tasks/{id}/',
                'create': '/api/tasks/ (Admin only)',
                'add_file': '/api/tasks/{id}/add_file/ (Curator)',
                'add_link': '/api/tasks/{id}/add_link/ (Curator)'
            },
            'teams': {
                'list': '/api/teams/',
                'detail': '/api/teams/{id}/',
                'create': '/api/teams/ (Captain)',
                'select_task': '/api/teams/{id}/select_task/ (Captain)',
                'add_member': '/api/teams/{id}/add_member/ (Captain)'
            },
            'solutions': {
                'list': '/api/solutions/',
                'detail': '/api/solutions/{id}/',
                'create': '/api/solutions/ (Captain)',
                'evaluations': '/api/solutions/{id}/evaluations/'
            },
            'evaluations': {
                'list': '/api/evaluations/',
                'detail': '/api/evaluations/{id}/',
                'create': '/api/evaluations/ (Jury)',
                'my_evaluations': '/api/evaluations/my_evaluations/ (Jury)',
                'solutions_by_date': '/api/evaluations/solutions_by_date/ (Jury)'
            }
        },
        'documentation': '/docs/ (run: mkdocs serve)',
        'admin': '/admin/'
    })


class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet для задач"""
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TaskDetailSerializer
        return TaskSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), CanCreateTask()]
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), CanAssignCurator()]
        return super().get_permissions()
    
    def get_queryset(self):
        queryset = Task.objects.all()
        # Капитан видит только задачи, которые он может выбрать
        if self.request.user.is_captain():
            return queryset
        # Куратор видит свою задачу
        if self.request.user.is_curator():
            return queryset.filter(curator=self.request.user)
        # Жюри и админ видят все задачи
        return queryset
    
    @action(detail=True, methods=['post'], permission_classes=[IsCurator])
    def add_file(self, request, pk=None):
        """Добавление файла к задаче (только куратор)"""
        task = self.get_object()
        if task.curator != request.user:
            return Response(
                {'error': 'Вы не являетесь куратором этой задачи'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = TaskFileCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[IsCurator])
    def add_link(self, request, pk=None):
        """Добавление ссылки к задаче (только куратор)"""
        task = self.get_object()
        if task.curator != request.user:
            return Response(
                {'error': 'Вы не являетесь куратором этой задачи'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = TaskLinkCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsCurator])
    def set_consultation_link(self, request, pk=None):
        """Установка ссылки на консультацию (только куратор)"""
        task = self.get_object()
        if task.curator != request.user:
            return Response(
                {'error': 'Вы не являетесь куратором этой задачи'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        consultation_link = request.data.get('consultation_link')
        task.consultation_link = consultation_link
        task.save()
        return Response(TaskSerializer(task).data)


class TaskFileViewSet(viewsets.ModelViewSet):
    """ViewSet для файлов задач"""
    queryset = TaskFile.objects.all()
    serializer_class = TaskFileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = TaskFile.objects.all()
        task_id = self.request.query_params.get('task', None)
        if task_id:
            queryset = queryset.filter(task_id=task_id)
        return queryset
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsTaskCurator()]
        return super().get_permissions()


class TaskLinkViewSet(viewsets.ModelViewSet):
    """ViewSet для ссылок задач"""
    queryset = TaskLink.objects.all()
    serializer_class = TaskLinkSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = TaskLink.objects.all()
        task_id = self.request.query_params.get('task', None)
        if task_id:
            queryset = queryset.filter(task_id=task_id)
        return queryset
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsTaskCurator()]
        return super().get_permissions()


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet для команд"""
    queryset = Team.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TeamDetailSerializer
        return TeamSerializer
    
    def get_queryset(self):
        queryset = Team.objects.all()
        # Капитан видит только свою команду
        if self.request.user.is_captain():
            return queryset.filter(captain=self.request.user)
        # Остальные роли видят все команды
        return queryset
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsCaptain()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsTeamCaptain()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        # При создании команды автоматически назначается капитан
        serializer.save(captain=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsTeamCaptain])
    def add_member(self, request, pk=None):
        """Добавление участника в команду (только капитан)"""
        team = self.get_object()
        serializer = TeamMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(team=team)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsTeamCaptain])
    def select_task(self, request, pk=None):
        """Выбор задачи командой (только капитан)"""
        team = self.get_object()
        task_id = request.data.get('task_id')
        if not task_id:
            return Response(
                {'error': 'Необходимо указать task_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task = get_object_or_404(Task, id=task_id)
        team.selected_task = task
        team.save()
        return Response(TeamSerializer(team).data)


class TeamMemberViewSet(viewsets.ModelViewSet):
    """ViewSet для участников команд"""
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = TeamMember.objects.all()
        team_id = self.request.query_params.get('team', None)
        if team_id:
            queryset = queryset.filter(team_id=team_id)
        # Капитан видит только участников своей команды
        if self.request.user.is_captain():
            queryset = queryset.filter(team__captain=self.request.user)
        return queryset
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Проверяем, что капитан команды
            return [IsAuthenticated(), IsTeamCaptain()]
        return super().get_permissions()


class SolutionViewSet(viewsets.ModelViewSet):
    """ViewSet для решений"""
    queryset = Solution.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SolutionDetailSerializer
        return SolutionListSerializer
    
    def get_queryset(self):
        queryset = Solution.objects.all()
        # Капитан видит только решения своей команды
        if self.request.user.is_captain():
            return queryset.filter(team__captain=self.request.user)
        # Куратор видит решения по своей задаче
        if self.request.user.is_curator():
            return queryset.filter(task__curator=self.request.user)
        # Жюри и админ видят все решения
        return queryset
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsCaptain()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsTeamCaptain()]
        if self.action == 'retrieve':
            return [IsAuthenticated(), CanViewSolution()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        # При создании решения автоматически назначается команда капитана
        team = get_object_or_404(Team, captain=self.request.user)
        serializer.save(team=team)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated, CanViewSolution])
    def evaluations(self, request, pk=None):
        """Получение оценок решения"""
        solution = self.get_object()
        evaluations = solution.evaluations.all()
        serializer = EvaluationSerializer(evaluations, many=True, context={'request': request})
        return Response(serializer.data)


class EvaluationViewSet(viewsets.ModelViewSet):
    """ViewSet для оценок"""
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Evaluation.objects.all()
        solution_id = self.request.query_params.get('solution', None)
        if solution_id:
            queryset = queryset.filter(solution_id=solution_id)
        # Жюри видит только свои оценки
        if self.request.user.is_jury():
            return queryset.filter(jury=self.request.user)
        # Остальные видят все оценки
        return queryset
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsJury()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsJury()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        # При создании оценки автоматически назначается жюри
        solution_id = serializer.validated_data.get('solution').id
        solution = get_object_or_404(Solution, id=solution_id)
        # Проверяем, что жюри еще не оценивал это решение
        if Evaluation.objects.filter(solution=solution, jury=self.request.user).exists():
            raise ValidationError({'error': 'Вы уже оценили это решение'})
        serializer.save(jury=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[IsJury])
    def my_evaluations(self, request):
        """Получение всех оценок текущего жюри"""
        evaluations = Evaluation.objects.filter(jury=request.user).order_by('-created_at')
        serializer = self.get_serializer(evaluations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsJury])
    def solutions_by_date(self, request):
        """Получение решений, отсортированных по дате публикации (для жюри)"""
        solutions = Solution.objects.all().order_by('-published_at')
        serializer = SolutionListSerializer(solutions, many=True, context={'request': request})
        return Response(serializer.data)
