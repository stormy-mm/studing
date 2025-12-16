from django.shortcuts import render, redirect
from .models import Item

def home_page(request):
    """Домашняя страница"""
    if request.method == "POST":
        Item.objects.create(text=request.POST["item_text"])
        return redirect("/lists/only-list-in-the-world/")

    return render(request, "home.html")

def view_list(request):
    """Новый список"""
    items = Item.objects.all()
    return render(request, "list.html", {"items": items})