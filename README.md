=====
SteamGames
=====

SteamGames is a Django app which allows you to find games you have in common with a friend.

The app also aggregates metadata about the games, allowing you to see their categories, tags, price etc.

Quick start
-----------

Make sure you have the required packages & django apps. SteamGames requires SteamAPI and urllib2.

1. Add "SteamGames" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'steamgames',
    )

2. Add a "STEAM_API_KEY" config entry to your settings.py. This is necessary for accessing Steam objects via API.

3. Include the SteamGames URLconf in your project urls.py like this::

    url(r'^steamgames/', include('steamgames.urls', namespace="steamgames")),
    
4. Run python manage.py migrate to create the necessary DB objects.

5. Start the development server and visit http://127.0.0.1:8000/steamgames
   
6. Start comparing games!
