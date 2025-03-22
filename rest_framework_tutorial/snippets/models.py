from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]] # get the programming languages meta data
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS]) # arranged the languages tuple in alphabetical order
STYLE_CHOICES = sorted([(style, style) for style in get_all_styles()]) # arranged the styles tuple in alphabetical order

# Create your models here.
class Snippet(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    # set the ordering on the basis of created_at timestamp
    class Meta: 
        ordering=['created_at']