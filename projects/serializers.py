from rest_framework import serializers
from .models import Project, Initiative, Article


class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    initiative_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='initiative_set')
    time_create = serializers.SerializerMethodField()
    time_update = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    @staticmethod
    def get_time_create(obj):
        return int(obj.time_create.timestamp())

    @staticmethod
    def get_time_update(obj):
        return int(obj.time_update.timestamp())


class InitiativeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    article_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='article_set')
    time_create = serializers.SerializerMethodField()
    time_update = serializers.SerializerMethodField()

    class Meta:
        model = Initiative
        fields = '__all__'

    @staticmethod
    def get_time_create(obj):
        return int(obj.time_create.timestamp())

    @staticmethod
    def get_time_update(obj):
        return int(obj.time_update.timestamp())

class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    project_id = serializers.SerializerMethodField()
    time_create = serializers.SerializerMethodField()
    time_update = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'

    @staticmethod
    def get_project_id(obj):
        return obj.initiative_id.project_id.id

    @staticmethod
    def get_time_create(obj):
        return int(obj.time_create.timestamp())

    @staticmethod
    def get_time_update(obj):
        return int(obj.time_update.timestamp())