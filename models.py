from django.db import models

class BlogData(models.Model):
    title=models.CharField(max_length=200)
    link=models.URLField()
    image = models.ImageField()

class Blog(models.Model):
    storename = models.CharField(max_length = 25)
    mainmenuname =  models.CharField(max_length = 25)
    foodimage = models.ImageField(blank=True, upload_to="blog/%Y/%m/%d")
    price = models.DecimalField(max_digits=19, decimal_places=10)
    content = models.TextField()
 