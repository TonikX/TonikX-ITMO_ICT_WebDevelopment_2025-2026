from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Task, TaskFile, TaskLink, Team, TeamMember,
    Solution, Evaluation
)

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'role_display', 'date_joined', 'created_at'
        ]
        read_only_fields = ['id', 'date_joined', 'created_at']


class CustomUserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания пользователя (регистрация)"""
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_retype = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_retype', 'first_name', 'last_name', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'password_retype': {'write_only': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_retype']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_retype')
        password = validated_data.pop('password')
        # По умолчанию при регистрации создается капитан
        if 'role' not in validated_data:
            validated_data['role'] = 'captain'
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class TaskFileSerializer(serializers.ModelSerializer):
    """Сериализатор файла задачи"""
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = TaskFile
        fields = ['id', 'task', 'file', 'file_url', 'name', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']
    
    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class TaskLinkSerializer(serializers.ModelSerializer):
    """Сериализатор ссылки задачи"""
    class Meta:
        model = TaskLink
        fields = ['id', 'task', 'url', 'title', 'created_at']
        read_only_fields = ['id', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор задачи"""
    curator_username = serializers.CharField(source='curator.username', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    files = TaskFileSerializer(many=True, read_only=True)
    links = TaskLinkSerializer(many=True, read_only=True)
    teams_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'created_by', 'created_by_username',
            'curator', 'curator_username', 'consultation_link',
            'files', 'links', 'teams_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_teams_count(self, obj):
        return obj.teams.count()


class TaskDetailSerializer(TaskSerializer):
    """Детальный сериализатор задачи с решениями"""
    solutions = serializers.SerializerMethodField()
    
    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ['solutions']
    
    def get_solutions(self, obj):
        solutions = obj.solutions.all()[:10]  # Последние 10 решений
        return SolutionListSerializer(solutions, many=True, context=self.context).data


class TeamMemberSerializer(serializers.ModelSerializer):
    """Сериализатор участника команды"""
    class Meta:
        model = TeamMember
        fields = ['id', 'team', 'first_name', 'last_name', 'email', 'created_at']
        read_only_fields = ['id', 'created_at']


class TeamSerializer(serializers.ModelSerializer):
    """Сериализатор команды"""
    captain_username = serializers.CharField(source='captain.username', read_only=True)
    captain_email = serializers.CharField(source='captain.email', read_only=True)
    selected_task_title = serializers.CharField(source='selected_task.title', read_only=True)
    members = TeamMemberSerializer(many=True, read_only=True)
    members_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'captain', 'captain_username', 'captain_email',
            'motto', 'selected_task', 'selected_task_title',
            'members', 'members_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_members_count(self, obj):
        return obj.members.count()


class TeamDetailSerializer(TeamSerializer):
    """Детальный сериализатор команды с решениями"""
    solutions = serializers.SerializerMethodField()
    
    class Meta(TeamSerializer.Meta):
        fields = TeamSerializer.Meta.fields + ['solutions']
    
    def get_solutions(self, obj):
        solutions = obj.solutions.all()
        return SolutionListSerializer(solutions, many=True, context=self.context).data


class SolutionListSerializer(serializers.ModelSerializer):
    """Сериализатор списка решений"""
    team_name = serializers.CharField(source='team.name', read_only=True)
    task_title = serializers.CharField(source='task.title', read_only=True)
    file_url = serializers.SerializerMethodField()
    evaluations_count = serializers.SerializerMethodField()
    average_score = serializers.SerializerMethodField()
    
    class Meta:
        model = Solution
        fields = [
            'id', 'team', 'team_name', 'task', 'task_title',
            'description', 'file', 'file_url',
            'evaluations_count', 'average_score',
            'published_at', 'updated_at'
        ]
        read_only_fields = ['id', 'published_at', 'updated_at']
    
    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None
    
    def get_evaluations_count(self, obj):
        return obj.evaluations.count()
    
    def get_average_score(self, obj):
        evaluations = obj.evaluations.all()
        if evaluations.exists():
            return round(sum(e.score for e in evaluations) / evaluations.count(), 2)
        return None


class SolutionDetailSerializer(SolutionListSerializer):
    """Детальный сериализатор решения с оценками"""
    evaluations = serializers.SerializerMethodField()
    
    class Meta(SolutionListSerializer.Meta):
        fields = SolutionListSerializer.Meta.fields + ['evaluations']
    
    def get_evaluations(self, obj):
        evaluations = obj.evaluations.all()
        return EvaluationSerializer(evaluations, many=True, context=self.context).data


class EvaluationSerializer(serializers.ModelSerializer):
    """Сериализатор оценки"""
    jury_username = serializers.CharField(source='jury.username', read_only=True)
    solution_team_name = serializers.CharField(source='solution.team.name', read_only=True)
    solution_task_title = serializers.CharField(source='solution.task.title', read_only=True)
    
    class Meta:
        model = Evaluation
        fields = [
            'id', 'solution', 'solution_team_name', 'solution_task_title',
            'jury', 'jury_username', 'score', 'comment',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TaskFileCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания файла задачи"""
    class Meta:
        model = TaskFile
        fields = ['task', 'file', 'name']


class TaskLinkCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания ссылки задачи"""
    class Meta:
        model = TaskLink
        fields = ['task', 'url', 'title']
