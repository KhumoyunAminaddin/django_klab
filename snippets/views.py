from django.contrib import auth
import requests
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.reverse import reverse
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, DetailSnippetSerializer, UserSerializer
from snippets.models import Snippet
from snippets.models import RESTAURANTS

@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "snippets": reverse("snippet-list", request=request, format=format),
            "foodcourt": reverse("foodcourt-list", request=request, format=format),
        }
    )

@permission_classes(permissions.AllowAny)
@api_view(['PUT', 'GET'])
def snippet_detail(request, pk):
	try:
		snippet = Snippet.objects.get(pk=pk)
	except Snippet.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'PUT':
		serializer = SnippetSerializer(snippet, data=request.data)
		serializer.is_valid(raise_exception=True)
		return Response(serializer.data)

	if request.method == 'GET':
		return Response(SnippetSerializer(snippet).data)


class SnippetViewSet(viewsets.ModelViewSet):
	serializer_class = SnippetSerializer
	queryset = Snippet.objects.all()
	permission_classes = [IsOwnerOrReadOnly]
	pagination_class = PageNumberPagination

	def retrieve(self, request, pk=None):
		queryset = Snippet.objects.all()
		snippet = get_object_or_404(queryset, pk=pk)
		serializer = DetailSnippetSerializer(snippet)
		return Response(serializer.data)

	def list(self, request):
		queryset = Snippet.objects.all()
		serializer = SnippetSerializer(queryset, many=True)
		return Response(serializer.data)

	# def update(self, request, pk=None):
	# 	return snippet_detail(request, pk)

	def create(self, request):
		sr = SnippetSerializer(data=request.data)
		sr.is_valid(raise_exception=True)
		sr.save()
		return Response(sr.data, status=201)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = auth.get_user_model().objects.all()
	serializer_class = UserSerializer


class FoodCourtView(APIView):
	def get(self, request):
		data = {}
		for i, menu in enumerate(RESTAURANTS):
			try:
				response = requests.get(menu+'/menu', timeout=3)
				data[i] = response.json()
			except requests.exceptions.Timeout as e:
				return Response(status=504)

		return Response(data, status=200)