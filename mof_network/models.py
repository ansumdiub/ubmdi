from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


# Each model is a Python class that subclasses django.db.models.Model
# Each attribute of the model represents a database field.
# With all of this, Django gives you an automatically-generated database-access API.

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    date_create = models.DateTimeField(default=timezone.now)
    date_publish = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.date_publish = timezone.now()
        self.save()

    # def approve_comments(self):
    #     return self.comments.filter(approved=True)

    def get_absolute_url(self):
        return reverse('mof:post_detail_view', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Mof(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    lcd = models.FloatField()
    pld = models.FloatField()
    area = models.FloatField()
    density = models.FloatField()
    formula = models.CharField(max_length=255)
    space_group = models.CharField(max_length=255)
    vol_frac = models.FloatField()
    fingerprint = models.ImageField(upload_to='comm_contrib', blank=True)
    # approved = models.BooleanField(default=False)
    #
    # def approve(self):
    #     self.approved = True
    #     self.save()

    def get_absolute_url(self):
        return reverse('mof:mof_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Connection(models.Model):
    source = models.ForeignKey('mof_network.Mof', related_name='A', on_delete=models.CASCADE)
    target = models.ForeignKey('mof_network.Mof', related_name='B', on_delete=models.CASCADE)

    # def get_absolute_url(self):
    #     return reverse('mof:post_detail_view', kwargs={'pk': self.pk})

    def __str__(self):
        return '{} is correlated with {}'.format(self.source, self.target)


class Comment(models.Model):
    mof = models.ForeignKey('mof_network.Mof', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=255)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    publish_date = models.DateTimeField(blank=True, null=True)
    approved = models.BooleanField(default=False)

    def approve(self):
        self.approved = True
        self.save()

    def get_absolute_url(self):
        return reverse('mof:mof_list')

    def __str__(self):
        return self.text
