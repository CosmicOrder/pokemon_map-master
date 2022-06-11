from django.db import models


class Pokemon(models.Model):
    title = models.CharField("Название на русском", max_length=200)
    title_en = models.CharField("Название на анлийском", max_length=200, \
                                blank=True)
    title_jp = models.CharField("Название на японском", max_length=200, \
                                blank=True)
    image = models.ImageField("Изображение", blank=True)
    description = models.TextField("Описание", blank=True)
    previous_evolution = models.ForeignKey("Pokemon",
                                           on_delete=models.SET_NULL,
                                           null=True,
                                           related_name="next_evolutions")

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE,
                                verbose_name='Покемон')
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField("Появится", null=True, blank=True)
    disappeared_at = models.DateTimeField("Исчезнет", null=True, blank=True)
    level = models.IntegerField("Уровень", null=True, blank=True)
    Health = models.IntegerField("Здоровье", null=True, blank=True)
    Strength = models.IntegerField("Сила", null=True, blank=True)
    Defence = models.IntegerField("Защита", null=True, blank=True)
    Stamina = models.IntegerField("Выносливость", null=True, blank=True)

    def __str__(self):
        return self.pokemon.title
