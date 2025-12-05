import os

from django.contrib import auth
from django.db import models
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

RESTAURANTS = [
    os.getenv('RESTAURANT_URL'),
]


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default="")
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, default="python", max_length=100
    )
    style = models.CharField(choices=STYLE_CHOICES, default="friendly", max_length=100)
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="snip")

    def get_absolute_url(self):
        return "http://127.0.0.1:8000/snippets/"+str(self.id)+'/'

    def save(self, *args, **kwargs):
        lexer = get_lexer_by_name(self.language)
        linenos = "table" if self.linenos else False
        options = {"title": self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos, full=True,
                                  **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        self.owner = auth.get_user_model().objects.get(id=1)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["created"]