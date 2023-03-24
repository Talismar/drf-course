from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from core.models import *
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from rest_framework.views import APIView
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from core.serializers import *

@method_decorator(csrf_exempt, name="dispatch")
class CategoryView(View):
    def get(self, request, id=None):
        
        if id:
            qs = get_object_or_404(Category, id=id)
            data = {
                "id": qs.id,
                "description": qs.description
            }
            return JsonResponse(data)

        data = list(Category.objects.all().values())
        formatted_date = json.dumps(data, ensure_ascii=False)
        return HttpResponse(formatted_date, content_type="application/json")

    def post(self, request, *args, **kwargs):
        print("request")
        json_data = json.loads(request.body)
        new_category = Category.objects.create(**json_data)
        data = {"id": new_category.id, "description": new_category.description}
        return JsonResponse(data)
    
    def patch(self, request, id):
        json_data = json.loads(request.body)
        qs = Category.objects.get(id=id)
        qs.description = json_data["description"] if "description" in json_data else qs.description
        qs.save()
        
        print(qs)

        return JsonResponse({'id': qs.id, 'description': qs.description})
    
    def delete(self, request, id):
        qs = Category.objects.get(id=id)
        qs.delete()

        return JsonResponse({"message": "Item clean with sucess!"})


class CategoriesListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoriesDetailAPIView(APIView):
    def get(self, request, id):
        category = get_object_or_404(Category, id=id)    
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, id):
        category = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(category, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
    def delete(self, request, id):
        category = get_object_or_404(Category, id=id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "id"

class PublishingCompanyViewSet(ModelViewSet):
    queryset = PublishingCompany.objects.all()
    serializer_class = PublishingCompanySerializer

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    # serializer_class = BookSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BookDetailSerializer
        if self.action == 'retrieve':
            return BookDetailSerializer
        return BookSerializer

class PurchaseViewSet(ModelViewSet):
    queryset = Purchase.objects.all()
    # permission_classes = [DjangoModelPermissions]
    # serializer_class = PurchaseSerializer

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return PurchaseSerializer

        return CreateEditPurchaseSerializer
    
    # Se o usuario não faz parte de um grupo listar so as comprar dele
    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="Administrators"):
            return self.queryset
        
        return Purchase.objects.filter(user=user)
    
