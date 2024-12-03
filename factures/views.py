from django.shortcuts import render
from django.views import View
from .models import *  # Assurez-vous d'importer votre modèle Invoice et Customer
from django.contrib import messages

class HomeView(View):
    """Main view"""
    template_name = 'index.html'  # Correction ici

    def get(self, request, *args, **kwargs):
        invoices = Invoice.objects.select_related('customer', 'save_by').all()  # Correction ici
        context = {
            'invoices': invoices
        }
        return render(request, self.template_name, context)

class AddCustomerView(View):
    """Add new customer"""
    template_name = 'add_customer.html'  # Ajoutez le nom du template ici

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'address': request.POST.get('address'),
            'sex': request.POST.get('sex'),
            'age': request.POST.get('age'),
            'city': request.POST.get('city'),
            'zip_code': request.POST.get('zip_code'),  # Corrigé pour correspondre à votre modèle
            'save_by': request.user  # Assigner l'utilisateur connecté
        }

        # Vérification des champs requis
        if not data['zip_code']:
            messages.error(request, "Zip code is required.")
            return render(request, self.template_name)

        try:
            # Créer un nouveau client
            Customer.objects.create(**data)
            messages.success(request, "Customer registered successfully")  # Message de succès
        except Exception as e:
            messages.error(request, f"Sorry, our system is detecting the following issues: {e}")

        return render(request, self.template_name)  # Rendre à nouveau le template en cas d'enregistrement
    
class AddInvoiceView(View):
    """add a new customer view"""

    template_name = 'add_invoice.html'
    customers = Customer.objects.select_related('save_by').all()  # Correction de 'Customers' en 'customers'
    context = {
        'customers': customers
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)  # Correction de 'self.template_name, self.context' en 'request, self.template_name, self.context'

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)