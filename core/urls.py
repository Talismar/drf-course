from django.urls import path
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register("category", CategoryViewSet)
router.register("editora_viewset", PublishingCompanyViewSet)
router.register("author_viewset", AuthorViewSet)
router.register("book", BookViewSet)
router.register("purchase", PurchaseViewSet)

app_name = 'livraria'
urlpatterns = [    
    # path('categories/', CategoryView.as_view()),
    # path('categories/<int:id>/', CategoryView.as_view())
] + router.urls


