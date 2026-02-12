import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Card
class LatestCardsFeed(Feed):
    title = 'My Cards!'
    link = reverse_lazy('mtg:card_list')
    description = 'New cards added to my site.'
    def items(self):
        return Card.objects.all()[:5]
    def item_title(self, item):
        return item.name
    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.oracle_text), 30)