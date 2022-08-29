from rest_framework import serializers
from .models import Puzzle, UserPuzzle


class PuzzleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puzzle
        fields = '__all__'


