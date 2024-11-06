from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView


# Create your views here.

class RequestDetailsView(DetailView):
    pass


class NewRequestView(CreateView):
    pass


class EditRequestView(UpdateView):
    pass


class DeleteRequestView(DeleteView):
    pass

