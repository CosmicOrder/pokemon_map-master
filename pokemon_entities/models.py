from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(null=True, blank=True)
    disappeared_at = models.DateTimeField(null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)
    Health = models.IntegerField(null=True, blank=True)
    Strength = models.IntegerField(null=True, blank=True)
    Defence = models.IntegerField(null=True, blank=True)
    Stamina = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.pokemon.title
