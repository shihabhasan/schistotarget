from django.db import models

class ImmunoLessConservative(models.Model):
    sequence = models.TextField(primary_key=True)
    prediction = models.TextField()
    features = models.TextField()
    access = models.IntegerField()
    time = models.DateTimeField()

    def __str__(self):
        return self.sequence


class ImmunoMoreConservative(models.Model):
    sequence = models.TextField(primary_key=True)
    prediction = models.TextField()
    features = models.TextField()
    access = models.IntegerField()
    time = models.DateTimeField()

    def __str__(self):
        return self.sequence