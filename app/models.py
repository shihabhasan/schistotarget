from django.db import models

class Immuno(models.Model):
    sequence = models.TextField(primary_key=True)
    prediction = models.TextField()
    features = models.TextField()
    access = models.IntegerField()
    time = models.DateTimeField()

    def __str__(self):
        return self.sequence


class IgE(models.Model):
    sequence = models.TextField(primary_key=True)
    prediction = models.TextField()
    features = models.TextField()
    access = models.IntegerField()
    time = models.DateTimeField()

    def __str__(self):
        return self.sequence


class IgG1(models.Model):
    sequence = models.TextField(primary_key=True)
    prediction = models.TextField()
    features = models.TextField()
    access = models.IntegerField()
    time = models.DateTimeField()

    def __str__(self):
        return self.sequence


class IgG3(models.Model):
    sequence = models.TextField(primary_key=True)
    prediction = models.TextField()
    features = models.TextField()
    access = models.IntegerField()
    time = models.DateTimeField()

    def __str__(self):
        return self.sequence


class IgG4(models.Model):
    sequence = models.TextField(primary_key=True)
    prediction = models.TextField()
    features = models.TextField()
    access = models.IntegerField()
    time = models.DateTimeField()

    def __str__(self):
        return self.sequence
