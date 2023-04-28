from django.db import models
from urllib import parse
from django.core.exceptions import ValidationError

# Create your models here.

class Video(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=500)
    notes = models.TextField(blank=True, null=True)
    youtube_id = models.CharField(max_length=40, unique=True)

    def save(self, *args, **kwargs):
        if not self.url.startswith('https://www.youtube.com/watch'):
            raise ValidationError(f'Invalid Youtube URL {self.url}')

        #extract video id from youtube url
        url_components = parse.urlparse(self.url)
        query_string = url_components.query
        if not query_string:
            raise ValidationError(f'Invalid Youtube URL {self.url}')
        parameters = parse.parse_qs(query_string, strict_parsing=True)
        v_parameters_list = parameters.get('v')
        if not v_parameters_list:
            raise ValidationError(f'Invalid Youtube URL, missing parameters {self.url}')
        self.youtube_id = v_parameters_list[0]
        super().save(*args, **kwargs)


    def __str__(self):
        return f'ID: {self.pk}, Name: {self.name}, URL: {self.url}, Video ID: {self.youtube_id} Notes: {self.notes[:200]}'

        