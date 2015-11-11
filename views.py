from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import timezone
import time
from operator import itemgetter
from django.db.models import Count
from .models import SteamGame, User, Genre, Category, Developer
import steamapi
import urllib2
import re
import base64
import json
from .commonTasks import *


def index(request):
    if request.method == 'POST':
        steamid = str(request.POST['steamid'])

        if steamid.endswith('/'):
            steamid = steamid[:-1]
        steamapi.core.APIConnection(api_key=settings.STEAM_API_KEY)
        urllist = steamid.split("/")
        userid = urllist[len(urllist) - 1]
        user = steamapi.user.SteamUser(userurl="officials1mple")
        if "/id/" in steamid:
            user = steamapi.user.SteamUser(userurl=userid)
        elif "/profiles/" in steamid:
            user = steamapi.user.SteamUser(int(userid))
        else:
            error_message = "sif"
            return render(request, 'steamgames/index.html', {'error_message': error_message})

        the_user = create_or_get_user(user)

        for game in user.games:
            the_game = create_or_get_game(game)
            if the_user.games.filter(appid=the_game.appid).count() == 0:
                the_user.games.add(the_game)

        return HttpResponseRedirect(reverse('steamgames:detaillist', args=(the_user.steamid,)))
    return render(request, 'steamgames/index.html')


def addcomparison(request, steamusers, to_add):
    steamid_decoded = base64.b64decode(to_add)
    if steamid_decoded.endswith('/'):
        steamid_decoded = steamid_decoded[:-1]
    steamapi.core.APIConnection(api_key=settings.STEAM_API_KEY)
    urllist = steamid_decoded.split("/")
    userid = urllist[len(urllist) - 1]
    user = steamapi.user.SteamUser(userurl="officials1mple")
    if "/id/" in steamid_decoded:
        user = steamapi.user.SteamUser(userurl=userid)
    elif "/profiles/" in steamid_decoded:
        user = steamapi.user.SteamUser(int(steamid_decoded))
    else:
        error_message = "sif"
        return render(request, 'steamgames/index.html', {'error_message': error_message})

    the_user = create_or_get_user(user)

    for game in user.games:
        the_game = create_or_get_game(game)
        if the_user.games.filter(appid=the_game.appid).count() == 0:
            the_user.games.add(the_game)

    userlist = steamusers + "," + str(the_user.steamid)

    return HttpResponseRedirect(reverse('steamgames:detaillist', args=(userlist,)))


def detaillist(request, steamusers):
    if request.method == "POST":
        if steamusers.endswith(","):
            steamusers = steamusers[:-1]
        steamid = str(request.POST["steamid"])
        to_add = base64.b64encode(steamid)
        return HttpResponseRedirect(reverse('steamgames:addcomparison', args=(steamusers, to_add)))

    if steamusers.endswith(","):
        steamusers = steamusers[:-1]
    if "," in steamusers:
        steamidlist = steamusers.split(",")
        number = len(steamidlist)
        users = []
        for s_id in steamidlist:
            user = User.objects.get(steamid=s_id)
            users.append(user)
        common_games = []
        games = SteamGame.objects.all().order_by('-metacritic_score')
        for game in games:
            gameusers = game.user_set.filter(steamid__in=steamidlist)
            if len(gameusers) > 0:
                common_games.append((game, gameusers))
        common_games.sort(key=lambda t: len(t[1]), reverse=True)
        return render(request, 'steamgames/detail.html', {'users': users, 'common_games': common_games,
                                                          'steamusers': steamusers})

    else:
        user = User.objects.get(steamid=steamusers)
        games = user.games.all().order_by('name')

        return render(request, 'steamgames/detail_single.html', {'user': user, 'games': games})
