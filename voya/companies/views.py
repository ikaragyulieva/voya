from django.db import transaction
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from voya.companies.forms import CompanyProfileForm, AddressForm, PhoneNumberForm
from voya.companies.models import CompanyProfile


# Create your views here.

class CompanyCreateView(FormView):
    template_name = 'companies/create-company-page.html'
    success_url = reverse_lazy('home')

    company_profile_form_class = CompanyProfileForm
    address_form_class = AddressForm
    phone_number_form_class = PhoneNumberForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['company_profile_form'] = context.get('company_profile_form', self.company_profile_form_class())
        context['address_form'] = context.get('address_form', self.address_form_class)
        context['phone_number_form'] = context.get('phone_number_form', self.phone_number_form_class)

        return context

    def post(self, request, *args, **kwargs):
        company_profile_form = self.company_profile_form_class(request.POST, request.FILES)
        address_form = self.address_form_class(request.POST)
        phone_number_form = self.phone_number_form_class(request.POST)

        if company_profile_form.is_valid() and address_form.is_valid() and phone_number_form.is_valid():
            return self.form_valid(company_profile_form, address_form, phone_number_form)
        else:
            return self.form_invalid(company_profile_form, address_form, phone_number_form)

    def get_form(self, form_class=None):
        return None

    def form_valid(self, company_profile_form, address_form, phone_number_form):
        with transaction.atomic():
            company_profile = company_profile_form.save()

            address = address_form.save(commit=False)
            address.company = company_profile
            address.save()

            phone_number = phone_number_form.save(commit=False)
            phone_number.company = company_profile
            phone_number.save()

            return super().form_valid(company_profile_form)

    def form_invalid(self, company_profile_form, address_form, phone_number_form):
        return self.render_to_response(
            self.get_context_data(
                company_profile_form=company_profile_form,
                phone_number_form=phone_number_form,
                address_form=address_form,
            )
        )
