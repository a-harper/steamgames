from django.utils import timezone
import time
from operator import itemgetter
from django.db.models import Count
from .models import SteamGame, User, Genre, Category, Developer, Publisher
import steamapi
import urllib2
import re
import base64
import json
from datetime import datetime


opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib2.install_opener(opener)


def create_or_get_user(user):
    if User.objects.filter(steamid=user.steamid).count() == 0:
        new_user = User()
        new_user.steamid = user.steamid
        new_user.country_code = user.country_code
        new_user.is_community_banned = user.is_community_banned
        new_user.is_vac_banned = user.is_vac_banned
        new_user.name = user.name
        new_user.real_name = user.real_name if hasattr(user, 'real_name') else "None"
        new_user.profile_url = user.profile_url
        new_user.time_created = user.time_created
        new_user.last_updated = timezone.now()

        new_user.save()
        the_user = new_user
    else:
        the_user = User.objects.get(steamid=user.steamid)

    return the_user


def create_or_get_developer(developer):
    if Developer.objects.filter(name=developer).count() == 0:
        new_developer = Developer()
        new_developer.name = developer

        new_developer.save()

        the_dev = new_developer
    else:
        the_dev = Developer.objects.get(name=developer)

    return the_dev


def create_or_get_publisher(publisher):
    if Publisher.objects.filter(name=publisher).count() == 0:
        new_publisher = Publisher()
        new_publisher.name = publisher

        new_publisher.save()

        the_pub = new_publisher
    else:
        the_pub = Publisher.objects.get(name=publisher)

    return the_pub


def create_or_get_genre(genre):
    if Genre.objects.filter(genre_id=genre['id']).count() == 0:
        new_genre = Genre()
        new_genre.genre_id = genre['id']
        new_genre.genre_name = genre['description']

        new_genre.save()

        the_genre = new_genre
    else:
        the_genre = Genre.objects.get(genre_id=genre['id'])

    return the_genre


def create_or_get_category(category):
    if Category.objects.filter(category_id=category['id']).count() == 0:
        new_category = Category()
        new_category.category_id = category['id']
        new_category.category_name = category['description']

        new_category.save()

        the_category = new_category
    else:
        the_category = Category.objects.get(category_id=category['id'])

    return the_category


def create_or_get_game(game):
    if SteamGame.objects.filter(appid=game.id).count() == 0:
        new_game = SteamGame()
        new_game.name = game.name
        new_game.appid = game.id
        gameid = str(game.id)
        time.sleep(2)
        appurl = "http://store.steampowered.com/api/appdetails/?appids=" + str(gameid) + "&cc=GB&l=english&v=1"

        data = json.load(urllib2.urlopen(appurl))
        if data[gameid]['success']:
            new_game.is_free = data[gameid]['data'].get('is_free')
            new_game.required_age = data[gameid]['data'].get('required_age')
            new_game.detailed_description = data[gameid]['data'].get('detailed_description')
            new_game.website = data[gameid]['data'].get('website')
            if data[gameid]['data'].get('price_overview'):
                new_game.currency = data[gameid]['data']['price_overview'].get('currency')
                new_game.initial_price = data[gameid]['data']['price_overview'].get('initial') / 100
                new_game.sale_price = data[gameid]['data']['price_overview'].get('final') / 100
            if data[gameid]['data'].get('metacritic'):
                new_game.metacritic_link = data[gameid]['data']['metacritic'].get('url')
                new_game.metacritic_score = data[gameid]['data']['metacritic'].get('score')
            else:
                new_game.metacritic_link = None
                new_game.metacritic_score = None
            try:
                new_game.release_date = datetime.strptime(data[gameid]['data']['release_date'].get('date'), "%d %b, %Y") if \
                    data[gameid]['data']['release_date'].get('date') else None
            except ValueError:
                new_game.release_date = datetime.strptime(data[gameid]['data']['release_date'].get('date'), "%b %Y") if \
                    data[gameid]['data']['release_date'].get('date') else None
            new_game.coming_soon = data[gameid]['data']['release_date'].get('coming_soon')

            new_game.save()

            if data[gameid]['data'].get('developers'):
                for developer in data[gameid]['data'].get('developers'):
                    the_dev = create_or_get_developer(developer)
                    new_game.developers.add(the_dev)

            if data[gameid]['data'].get('genres'):
                for genre in data[gameid]['data'].get('genres'):
                    the_genre = create_or_get_genre(genre)
                    new_game.genres.add(the_genre)

            if data[gameid]['data'].get('categories'):
                for category in data[gameid]['data'].get('categories'):
                    the_category = create_or_get_category(category)
                    new_game.categories.add(the_category)

            new_game.save()
            the_game = new_game
        else:
            new_game.save()
            the_game = new_game
    else:
        the_game = SteamGame.objects.get(appid=game.id)

    return the_game


