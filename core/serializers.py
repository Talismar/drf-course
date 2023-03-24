from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers

from django.db.models import QuerySet
from typing import TypeVar, Union
_MT = TypeVar("_MT", bound=Purchase)  # Model Type
class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"

class PublishingCompanySerializer(ModelSerializer):
    class Meta:
        model = PublishingCompany
        fields = "__all__"

class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

class PublishingCompanyNestedSerializer(ModelSerializer):
    class Meta:
        model = PublishingCompany
        fields = ("id", "name")

class BookDetailSerializer(ModelSerializer):
    category = serializers.CharField(source="category.description")
    publishing_company = PublishingCompanyNestedSerializer()
    authors = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = "__all__"
        depth = 1

    def get_authors(self, instance):
        name_of_author = []
        authors = instance.authors.get_queryset()
        for author in authors:
            name_of_author.append(author.name)

        return name_of_author

class ItemsPurchaseSerializer(ModelSerializer):

    total = serializers.SerializerMethodField()

    class Meta:
        model = ItemsPurchase
        fields = ("book", "amount", "total")
        depth = 2

    def get_total(self, instance):
        return instance.amount * instance.book.price

class PurchaseSerializer(ModelSerializer):
    # user = serializers.CharField(source="user.id")
    status = serializers.SerializerMethodField()
    items = ItemsPurchaseSerializer(many=True)

    class Meta:
        model = Purchase
        fields = ("id", "user", "status", "items", "total")

    def get_status(self, instance):
        return instance.get_status_display()

class CreateEditItemsPurchaseSerialiser(ModelSerializer):
    class Meta:
        model = ItemsPurchase
        fields = ["id", "book", "amount"]

    def validate(self, attrs):
        if attrs["amount"] > attrs["book"].amount:
            raise serializers.ValidationError({
                "amount": "Quantidade solicitada não disponível em estoque"
            })
        return attrs
class CreateEditPurchaseSerializer(ModelSerializer):
    items = CreateEditItemsPurchaseSerialiser(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Purchase
        fields = ["id", 'user', 'items']

    # validated_data - É os dados que já foram validated pelo serializer
    def create(self, validated_data):
        items = validated_data.pop("items")
        purchase = Purchase.objects.create(**validated_data)

        for item in items:
            ItemsPurchase.objects.create(purchase=purchase, **item)
            book = Book.objects.get(id=item['book'].id)
            book.amount -= item['amount']
            book.save()
        
        purchase.save()
        return purchase
    
    def update(self, instance, validated_data):
        items = validated_data.pop("items")
        
        if items:
            instance.items.all().delete()
            for item in items:
                ItemsPurchase.objects.create(purchase=instance, **item)
            instance.save()
        
        return instance