from django.db import models

# Create your models here.
class Books(models.Model):
    bk_name=models.CharField(max_length=200)
    bk_author=models.CharField(max_length=200)
    bk_genre=models.CharField(max_length=200)
    bk_rate=models.PositiveIntegerField()
    bk_image=models.ImageField(upload_to="images",null=True,blank=True)


    def __str__(self):
        return self.bk_name
    

    