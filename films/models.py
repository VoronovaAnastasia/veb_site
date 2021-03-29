from django.db.models import *
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Genre(Model):
    name = CharField(max_length=30)

    def __str__(self):
        return str(self.name)

class Film(Model):
    title=CharField(max_length=90)
    release_date= DateField()
    poster=ImageField(null=True,blank=True,upload_to='images/')
    description=TextField(max_length=4096)
    rating=IntegerField(null=True,blank=True)
    genres = ManyToManyField(Genre)
    def __str__(self):
        return str(self.title)

class Feedback(Model):
    film=ForeignKey(Film,on_delete=CASCADE)
    rating = IntegerField()
    created_at=DateTimeField('Creation timestamp', auto_now_add=True)
    text = TextField(max_length=4096)
    author = ForeignKey(User, on_delete=CASCADE, default=1)
    def __str__(self):
        return str(self.text)


