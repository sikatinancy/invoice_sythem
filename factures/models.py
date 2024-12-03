from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    """
    Name: Customer model definition
    """
    SEX_TYPE = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    )
    name = models.CharField(max_length=132)
    email = models.EmailField()
    phone = models.CharField(max_length=132)
    address = models.CharField(max_length=64)
    sex = models.CharField(max_length=1, choices=SEX_TYPE)
    age = models.PositiveIntegerField()  # Utilisation de PositiveIntegerField pour l'âge
    city = models.CharField(max_length=32)
    zip_code = models.CharField(max_length=16)
    created_date = models.DateTimeField(auto_now_add=True)
    save_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Permettre NULL

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.name  # Méthode __str__ corrigée


class Invoice(models.Model):
    """
    Name: Invoice model definition
    Description:
    author: nancysikati@gmail.com
    """ 
    INVOICE_TYPE = (
        ('R', 'RECEIPT'),
        ('P', 'PROFORMA INVOICE'),
        ('F', 'INVOICE')

    )
    
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    save_by = models.ForeignKey(User, on_delete=models.PROTECT)  # Champ save_by
    invoice_date_time = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)  # Réduire max_digits
    last_updated_date = models.DateTimeField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    invoice_type = models.CharField(max_length=1, choices=INVOICE_TYPE)
    comments = models.TextField(null=True, max_length=1000)

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self):
        return f"{self.customer.name} - {self.invoice_date_time}"

    @property
    def get_total(self):
        articles = self.article_set.all()
        total = sum(article.get_total for article in articles)
        return total  # Ajouter un retour pour la propriété


class Article(models.Model):
    """
    Name: Article model definition
    Description:
    author: nancysikati@gmail.com
    """               
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    quantity = models.PositiveIntegerField()  # Utilisation de PositiveIntegerField
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # Réduire max_digits
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    @property
    def get_total(self):
        return self.quantity * self.unit_price  # Retourner le total