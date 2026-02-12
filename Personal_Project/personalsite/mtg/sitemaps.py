from django.contrib.sitemaps import Sitemap
from .models import Card
class CardSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    def items(self):
        return Card.objects.all()
    # def lastmod(self,obj):
    #     return obj.updated
