from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import FormParser, MultiPartParser
from .serializers import *
from .models import *
# Create your views here.


class RecipeAPi(APIView):

    parser_classes = (FormParser, MultiPartParser)

    @swagger_auto_schema(
        operation_description="create Recipe",
        request_body=RecipeSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # question = serializer.save()
            # serializer = RecipeSerializer(question)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)     


class IngredientAPi(APIView):

    parser_classes = (FormParser, MultiPartParser)

    @swagger_auto_schema(
        operation_description="create Ingredients",
        request_body=IngredientSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            question = serializer.save()
            serializer = RecipeSerializer(question)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)         
    