from django.db import models

# Create your models here.


class Developer(models.Model):
    name = models.CharField(max_length=150)

    def __unicode__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=150)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    category_id = models.IntegerField()
    category_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.category_name


class Genre(models.Model):
    genre_id = models.IntegerField()
    genre_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.genre_name


class SteamGame(models.Model):
    appid = models.IntegerField()
    name = models.CharField(max_length=200)
    initial_price = models.FloatField(blank=True, null=True)
    sale_price = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=5, blank=True, null=True)
    required_age = models.IntegerField(blank=True, null=True)
    is_free = models.NullBooleanField(blank=True, null=True)
    detailed_description = models.CharField(max_length=1000, blank=True, null=True)
    metacritic_score = models.IntegerField(blank=True, null=True)
    metacritic_link = models.CharField(max_length=200, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    coming_soon = models.NullBooleanField(blank=True, null=True)
    developers = models.ManyToManyField(Developer, blank=True)
    publishers = models.ManyToManyField(Publisher, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    website = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return self.name


class User(models.Model):
    steamid = models.IntegerField()
    country_code = models.CharField(max_length=4)
    is_vac_banned = models.BooleanField()
    is_community_banned = models.BooleanField()
    name = models.CharField(max_length=50)
    profile_url = models.CharField(max_length=150)
    real_name = models.CharField(max_length=50)
    time_created = models.DateTimeField()
    games = models.ManyToManyField(SteamGame)
    last_updated = models.DateTimeField()

    def __unicode__(self):
        return self.profile_url




