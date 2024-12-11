from django.contrib.auth import mixins
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, DetailView, UpdateView, DeleteView

from voya.common.forms import SearchForm
from voya.companies import models
from voya.companies.forms import CompanyProfileForm, AddressForm, PhoneNumberForm
from voya.companies.models import CompanyProfile
from voya.employees.models import EmployeeProfile


# Create your views here.

class CompanyCreateView(FormView):
    template_name = 'companies/create-company-page.html'
    success_url = reverse_lazy('home')

    company_profile_form_class = CompanyProfileForm
    address_form_class = AddressForm
    phone_number_form_class = PhoneNumberForm

    # def get_object(self, queryset=None):
    #     # Fetch the ClientProfile based on the URL pk
    #     return EmployeeProfile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['company_profile_form'] = context.get('company_profile_form', self.company_profile_form_class())
        context['address_form'] = context.get('address_form', self.address_form_class())
        context['phone_number_form'] = context.get('phone_number_form', self.phone_number_form_class())
        if self.request.user.is_authenticated and self.request.user.is_active:
            employee_profile = EmployeeProfile.objects.get(user=self.request.user)
            context['profile'] = employee_profile

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
            company_profile_form.is_active = True
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


class CompaniesDashboardView(mixins.LoginRequiredMixin, ListView):
    model = models.CompanyProfile
    template_name = 'companies/companies-dashboard-page.html'
    paginate_by = 10

    def get_object(self, queryset=None):
        # Fetch the ClientProfile based on the URL pk
        return EmployeeProfile.objects.get(user=self.request.user)

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['profile'] = self.get_object()

        search_form = SearchForm(self.request.GET)
        company_query = CompanyProfile.objects.all().order_by('-is_active', '-created_at')

        for company in company_query:
            company.first_addresses = company.addresses.all().first()

        if search_form.is_valid():
            search_query = search_form.cleaned_data.get('search')
            if search_query:
                context['companyprofile_list'] = company_query.filter(commercial_name__icontains=search_query)
            else:
                context['companyprofile_list'] = company_query

        context["search_form"] = search_form
        context['all_companies'] = company_query

        return context


class CompanyDetailsView(mixins.LoginRequiredMixin, DetailView):
    model = models.CompanyProfile
    template_name = 'companies/company-details-page.html'
    context_object_name = "company"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        company = self.get_object()

        context['address'] = company.addresses.first()
        context['phone_number'] = company.phone_numbers.first()

        if self.request.user.is_authenticated and self.request.user.is_active:
            try:
                employee_profile = EmployeeProfile.objects.get(user=self.request.user)
                context['profile'] = employee_profile

            except EmployeeProfile.DoesNotExist:
                redirect('login')

        return context


class CompanyEditView(mixins.LoginRequiredMixin, UpdateView):
    model = models.CompanyProfile
    form_class = models.CompanyProfile
    template_name = 'companies/company-edit-page.html'
    success_url = reverse_lazy('companies-dashboard')
    context_object_name = 'company'

    def get_form(self, form_class=None):
        # Override to prevent UpdateView from requiring a form class
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'company_profile_form' not in context:
            context['company_profile_form'] = CompanyProfileForm(instance=self.get_object())
        if 'address_form' not in context:
            address_instance = self.get_object().addresses.first()
            context['address_form'] = AddressForm(instance=address_instance)
        if 'phone_number_form' not in context:
            phone_number_instance = self.get_object().phone_numbers.first()
            context['phone_number_form'] = PhoneNumberForm(instance=phone_number_instance)

        if self.request.user.is_authenticated and self.request.user.is_active:
            try:
                employee_profile = EmployeeProfile.objects.get(user=self.request.user)
                context['profile'] = employee_profile

            except EmployeeProfile.DoesNotExist:
                redirect('login')

        return context

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

        company_profile_instance = self.get_object()
        address_instance = company_profile_instance.addresses.first()
        phone_number_instance = company_profile_instance.phone_numbers.first()

        company_profile_form = CompanyProfileForm(request.POST, request.FILES, instance=company_profile_instance)
        address_form = AddressForm(request.POST, instance=address_instance)
        phone_number_form = PhoneNumberForm(request.POST, instance=phone_number_instance)
        if not company_profile_form.is_valid():
            print(company_profile_form.errors)
        if all([company_profile_form.is_valid(), address_form.is_valid(), phone_number_form.is_valid()]):
            return self.form_valid(company_profile_form, address_form, phone_number_form)

        else:
            return self.form_invalid(company_profile_form, address_form, phone_number_form)

    def form_valid(self, company_profile_form, address_form, phone_number_form):
        with transaction.atomic():
            company_profile_form.instance.is_active = True

            company_profile_form.save()
            address_form.save()
            phone_number_form.save()

        return super().form_valid(company_profile_form)

    def form_invalid(self, company_profile_form, address_form, phone_number_form):
        return self.render_to_response(
            self.get_context_data(
                company_profile_form=company_profile_form,
                address_form=address_form,
                phone_number_form=phone_number_form,
            )
        )


class CompanyDeleteView(mixins.LoginRequiredMixin, DeleteView):
    model = CompanyProfile
    template_name = 'companies/company-delete-page.html'
    success_url = reverse_lazy('companies-dashboard')
    context_object_name = "company"

    def get_form(self, form_class=None):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated and self.request.user.is_active:
            try:
                employee_profile = EmployeeProfile.objects.get(user=self.request.user)
                context['profile'] = employee_profile

            except EmployeeProfile.DoesNotExist:
                redirect('home')

        return context

    def post(self, request, *args, **kwargs):
        company_profile = self.get_object()
        addresses = company_profile.addresses.all()
        phone_numbers = company_profile.phone_numbers.all()

        company_profile.is_active = not company_profile.is_active
        company_profile.save()

        for address in addresses:
            address.is_active = not address.is_active
            address.save()

        for number in phone_numbers:
            number.is_active = not number.is_active
            number.save()

        return redirect(self.success_url)
