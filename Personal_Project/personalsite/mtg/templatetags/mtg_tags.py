from django import template
from ..models import Card
register = template.Library()
#Template tag to return the total number of cards in the database
@register.simple_tag
def total_cards():
    return Card.objects.count()


#Template tag to return the posts with the highest number of comments
from django.db.models import Count
@register.simple_tag
def get_most_commented_cards(count=5):
    return Card.objects.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

#Markdown format tags
import markdown
from django.utils.safestring import mark_safe
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))