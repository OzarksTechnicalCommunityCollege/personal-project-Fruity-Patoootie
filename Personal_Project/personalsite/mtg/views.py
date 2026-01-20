from django.shortcuts import render
from .models import Card
from django.http import Http404
# Create your views here.
# creating a list of card objects
def card_list(request):
    # a list of all cards in the databse
    cards = Card.objects.all()
    # return the request, the url, and the list of cards
    return render(
        request,
        'mtg/card/list.html',{'cards': cards}
    )

# A method that returns a specific card from the database
def card_detail(request, id):
    # setting the card var equal to the object returned from the database
    try:
        card = Card.objects.get(id=id)
    # if that fails, call a 404 page and return card not found
    except Card.DoesNotExist:
        raise Http404("No Card Found.")
    # if successful, return the request, url, and card data
    # Instead of try except, we could use the django shortcut 
    # get_object_or_404(object, id=id, sort_method), but I enjoy how verbose this method is
    return render(
        request,
        'mtg/card/detail.html',
        {'card': card}
    )






