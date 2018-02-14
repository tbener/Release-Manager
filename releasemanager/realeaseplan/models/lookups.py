from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100)
    role = models.ForeignKey("Role")

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
