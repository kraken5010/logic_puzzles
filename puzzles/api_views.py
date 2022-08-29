from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import *
from .permisiions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import PuzzleSerializer, UserPuzzleSerializer


class PuzzleAPIListPagination(PageNumberPagination):
    """Pagination class for list"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PuzzleAPIList(generics.ListCreateAPIView):
    """Puzzle list"""
    serializer_class = PuzzleSerializer
    queryset = Puzzle.objects.all()
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = PuzzleAPIListPagination


class PuzzleAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    """Puzzle detail"""
    serializer_class = PuzzleSerializer
    queryset = Puzzle.objects.all()
    permission_classes = (IsAdminUser, )


# Users Puzzles
class UserPuzzleAPIList(generics.ListAPIView):
    """User Puzzle list"""
    queryset = UserPuzzle.objects.all()
    serializer_class = UserPuzzleSerializer


class UserPuzzleAPIDetail(generics.RetrieveUpdateAPIView):
    """User Puzzle detail"""
    serializer_class = UserPuzzleSerializer
    queryset = UserPuzzle.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)


class UserPuzzleAPICreate(generics.CreateAPIView):
    """User Puzzle detail"""
    serializer_class = UserPuzzleSerializer
    queryset = UserPuzzle.objects.all()
    permission_classes = (IsAuthenticated,)