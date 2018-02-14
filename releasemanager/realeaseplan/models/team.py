from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)
    velocity = models.FloatField(default=1.0)
    resource_count = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name
