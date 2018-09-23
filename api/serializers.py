from rest_framework import serializers

from .models import *

class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ('version',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'password', 'email', 'gender')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('c_id', 'name')

class PostModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostModel
        fields = ('name', 'content')
        extra_kwargs = {
            'name' : {'required' : True},
            'content': {'required': True},
        }

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('PostModel', 'content', 'user', 'reg_date')

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('image', 'value')

class ChangeWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeWordModel
        fields = ('id', 'original_sentence')
