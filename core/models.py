from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description
    
# Editora
class PublishingCompany(models.Model):
    name = models.CharField(max_length=255)
    site = models.URLField()

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        # ADMIN DISPLAY
        verbose_name_plural = "Authors"

class Book(models.Model):
    title = models.CharField(max_length=255)
    ISBN = models.CharField(max_length=32)
    amount = models.IntegerField()
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="books")
    publishing_company = models.ForeignKey(PublishingCompany, on_delete=models.PROTECT, related_name="books")
    authors = models.ManyToManyField(Author, related_name="books")

    def __str__(self):
        return "%s (%s)" % (self.title, self.publishing_company)
    

class Purchase(models.Model):

    class StatusPurchase(models.IntegerChoices):
        CARRINHO = 1, "Carinho"
        REALIZADO = 2, "Realizado"
        PAGO = 3, "Pago"
        ENTREGUE = 4, "Entregue"

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="purchases")
    status = models.IntegerField(choices=StatusPurchase.choices, default=StatusPurchase.CARRINHO)

    @property
    def total(self):
        queryset = self.items.all().aggregate(
            total=models.Sum(models.F("amount") * models.F("book__price"))
        )
        return queryset["total"]
class ItemsPurchase(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="+")
    amount = models.IntegerField()

    