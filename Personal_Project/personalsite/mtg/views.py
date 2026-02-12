from django.shortcuts import render
from .models import Card
from django.http import Http404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .forms import EmailCardForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count


# Create your views here.
# creating a list of card objects
def card_list(request, tag_slug=None):
    # a list of all cards in the databse
    card_list = Card.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        card_list = card_list.filter(tags__in=[tag])

    #Paginator with 3 posts per page
    paginator = Paginator(card_list, 3)
    #use a simple get request to fetch the page number,
    #if none are returned we default to 1
    page_number = request.GET.get('page',1)
    #returns a page object
    try:
        cards = paginator.page(page_number)

    #if url has words in it, throw error
    except PageNotAnInteger:
        cards = paginator.page(1)
    #if url has nothing, throw error
    except EmptyPage:
        cards = paginator.page(paginator.num_pages)



    # return the request, the url, and the list of cards
    return render(
        request,
        'mtg/card/list.html',
        {
            'cards' : cards,
            'tag': tag
        }
    )

# A method that returns a specific card from the database
def card_detail(request, id, card):
    # setting the card var equal to the object returned from the database
    # if successful, return the request, url, and card data
    card = get_object_or_404(Card, id=id, slug=card)
    
    # List of active comments for this card
    comments = card.comments.filter(active=True)

    # Form for users to comment
    form = CommentForm()
    card_tags_ids = card.tags.values_list('id', flat=True)
    similar_cards = Card.objects.filter(tags__in=card_tags_ids).exclude(id=card.id)
    similar_cards = similar_cards.annotate(same_tags=Count('tags')).order_by('-same_tags')[:4]
    
    return render(
        request,
        'mtg/card/detail.html',
        {
            'card': card,
            'comments': comments,
            'form': form,
            'similar_cards' : similar_cards
        }
    )

def card_share(request, card_id):
    #Retrieve post by id with error handling
    card = get_object_or_404(
        Card,
        id=card_id,
    )

    sent = False

    
    if request.method == 'POST':
        #Form was submitted
        form = EmailCardForm(request.POST)
        # if form fields pass validation
        if form.is_valid():
            #send email
            cd = form.cleaned_data
            card_url = request.build_absolute_uri(
                card.get_absolute_url()
            )
            sent = True
    else:
        #else, make them re-enter the form
        form = EmailCardForm()
    return render(
        request,
        'mtg/card/share.html',
        {
            'card': card,
            'form': form,
            'sent': sent
        }
    )

def card_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = (
                    Card.objects.annotate(similarity=TrigramSimilarity('name', query),)
                .filter(similarity_gt=0.1)
                .order_by('-similarity')
            )
    return render(
        request,
        'mtg/card/search.html',
        {
            'form': form,
            'query': query,
            'results': results
        }
    )

# Class based view 
class CardListView(ListView):
    """
    Alternative post list view    
    """
    # Django builds the generic card.object.all() Query set for us here
    model = Card
    #Overrideing the default name
    context_object_name = 'cards'
    #Set the paginator to have 3 items
    paginate_by = 3
    #Determining a custom url for the template
    template_name = 'mtg/card/list.html'


# View logic for comments
@require_POST
def card_comment(request, card_id):
    card = get_object_or_404(
        Card,
        id=card_id,
    )
    comment = None
    # a comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        #Create a comment object without saving it to the database
        comment = form.save(commit=False)
        #assign the card to the comment
        comment.card = card
        # Save the comment to the databse
        comment.save()
    return render(
        request,
        'mtg/card/comment.html',
        {
            'card': card,
            'form': form,
            'comment': comment
        }
    )
