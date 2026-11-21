from django.db import models
from django.contrib.auth.models import User


class category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class team(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class games(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    category = models.ForeignKey(category,on_delete=models.CASCADE,related_name='games',)
    team = models.ForeignKey(team,on_delete=models.CASCADE,related_name='games',)
    def __str__(self):
        return self.name


class order(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    game = models.ForeignKey(games,on_delete=models.CASCADE,related_name='orders',)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='ticket_orders',null=True,blank=True,)
    def __str__(self):
        return f'{self.name} - {self.game}'