from rest_framework import serializers
from .models import Puzzle, UserPuzzle


class PuzzleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puzzle
        fields = '__all__'


class UserPuzzleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserPuzzle
        fields = '__all__'


