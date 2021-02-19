from django.db import models

# Create your models here.
class Event(models.Model):
    site_name = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=500,unique=True)
    event_type = models.CharField(max_length=100)
    description = models.TextField()
    interest_group = models.ForeignKey('Group',on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    group_name = models.CharField(max_length=100)
    group_class = models.ForeignKey('self',on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.group_name

class interesting_url(models.Model):
    url = models.URLField(max_length=500)
    event = models.ForeignKey('Event',on_delete=models.CASCADE)

class non_interesting_url(models.Model):
    url = models.URLField(max_length=500)
