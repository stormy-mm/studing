from django.shortcuts import render, redirect
from django.views.generic import FormView

from .forms import ItemForm, ExistingListItemForm
from .models import List


def home_page(request):
    """Домашняя страница"""
    return render(request, "home.html", {"form": ItemForm()})

def view_list(request, list_id):
    """Представление списка"""
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == "POST":
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, "list.html", {"list": list_, "form": form})

def new_list(request):
    """Новый список"""
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(list_)
        return redirect(list_)
    return render(request, "home.html", {"form": form})


class HomePageView(FormView):
    template_name = "home.html"
    form_class = ItemForm