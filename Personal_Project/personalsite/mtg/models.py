from django.db import models

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
    type = models.CharField(max_length=250)
    set = models.CharField(max_length=100)
    oracle_text = models.TextField()
    mana_value = models.SmallIntegerField()
    power = models.SmallIntegerField()
    toughness = models.SmallIntegerField()
    rarity = models.CharField(max_length=1)
    set_abbreviation = models.CharField(max_length=3)
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
    
