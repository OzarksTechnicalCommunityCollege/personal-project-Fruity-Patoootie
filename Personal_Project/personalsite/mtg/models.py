from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from django.conf import settings
from django.utils.text import slugify

# To allow my computer to use the virtual environment run powershell command below
# Set-ExecutionPolicy Unrestricted -Scope Process
# then activate the environment with .\[VIRTUAL ENV NAME]\Scripts\activate




# Creating a custom manager to sort cards by commander legality
class LegalityManager(models.Manager):
    def get_queryset(self):
        return(
            super().get_queryset().filter(commander_legality=Card.Commander_Legality.LEGAL)
        )


# Creating a model for magic cards
class Card(models.Model):
    # a subclass to define the card's legality in the gamemode commander
    class Commander_Legality(models.TextChoices):
        LEGAL = 'LG', 'Legal'
        NONLEGAL = 'NL', 'Nonlegal'
    #Defining properties of the card class that pertains to database fields
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    type = models.CharField(max_length=250)
    set = models.CharField(max_length=100)
    oracle_text = models.TextField()
    mana_value = models.SmallIntegerField()
    power = models.SmallIntegerField()
    toughness = models.SmallIntegerField()
    rarity = models.CharField(max_length=1)
    set_abbreviation = models.CharField(max_length=3)
    tags= TaggableManager()
    # Setting the default of cards to be legal in commander
    commander_legality = models.CharField(
        max_length=2,
        choices=Commander_Legality,
        default=Commander_Legality.LEGAL
    )
    
    # default manager declared first so can still sort by objects
    objects = models.Manager()
    # and custom manager to sort by commander legality
    legality = LegalityManager()


    #Setting up the default ordering when the data is displayed
    class Meta:
        ordering = ['name']
        # Setting up an index so the database can be queried based on card name
        indexes = [
            models.Index(fields=['name']),
            ]

    # String override
    def __str__(self):
        return self.name
    
    #using the URL reverse function to build URLs dynamically
    def get_absolute_url(self):
        return reverse(
            'mtg:card_detail',
            args=[self.id, self.slug]
        )

# Comment class so people can discuss their favorite cards!
class Comment(models.Model):
    #Foreign key so that comments stick to their associated cards
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    #username
    name = models.CharField(max_length=80)
    #user's email
    email=models.EmailField()
    #user's comment
    body = models.TextField()
    #date created, updated, and if it's an active comment
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    #Ordering the comments based on when they were created, indexing on the same stipulation
    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    # string override so we can know what object we are accessing if needed during debugging
    def __str__(self):
        return f'Comment by {self.name} on {self.card}'



#Deck class
class Deck(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='decks_created',
        on_delete=models.CASCADE
    )
    cards = models.ManyToManyField(Card, related_name='added_cards', blank=True)
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name ='decks_liked',
        blank=True
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])
    
