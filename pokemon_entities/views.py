import folium
import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime

from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    active_pokemons = PokemonEntity.objects.filter(
        appeared_at__lt=localtime(), disappeared_at__gt=localtime())
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in active_pokemons:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_entity.pokemon.image.path
        )

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon_entity = PokemonEntity.objects.get(pk=pokemon_id)
    except ObjectDoesNotExist:
        return ('<h1>Информации о таком покемоне не найден</h1>')
    try:
        pokemon_db = Pokemon.objects.get(pk=pokemon_id)
    except ObjectDoesNotExist:
        return ('<h1>Такой покемон не найден</h1>')

    pokemon = {
        "pokemon_id": pokemon_db,
        "title_ru": pokemon_db.title,
        "title_en": pokemon_db.title_en,
        "title_jp": pokemon_db.title_jp,
        "description": pokemon_db.description,
        "img_url": pokemon_db.image.url,
    }

    if pokemon_db.previous_evolution:
        pokemon["previous_evolution"] = {
            "title_ru": pokemon_db.previous_evolution.title,
            "pokemon_id": pokemon_db.previous_evolution.pk,
            "img_url": pokemon_db.previous_evolution.image.url,
        }
    if pokemon_db.next_evolution:
        pokemon["next_evolution"] = {
            "title_ru": pokemon_db.next_evolution.first().title,
            "pokemon_id": pokemon_db.next_evolution.first().pk,
            "img_url": pokemon_db.next_evolution.first().image.url,
        }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    add_pokemon(
        folium_map, pokemon_entity.lat,
        pokemon_entity.lon,
        pokemon_entity.pokemon.image.path
    )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
