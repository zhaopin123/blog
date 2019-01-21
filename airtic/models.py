from django.db import models

class User(models.Model):
    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=150, null=False)
    crate_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user'


class LanMu(models.Model):
    name = models.CharField(max_length=20)
    other_name = models.CharField(max_length=20,null=True)
    keyword = models.CharField(max_length=10,null=True)
    mshu = models.CharField(max_length=50,null=True)

    class Meta:
        db_table = 'lanmu'

class Article(models.Model):
    title = models.CharField(null=True,max_length=30)
    crate_time = models.DateField(auto_now_add=True)
    data = models.CharField(null=False,max_length=4000)
    icon = models.ImageField(upload_to='upload', null=True)
    lm = models.ForeignKey(LanMu,null=True,on_delete=models.SET_NULL)
    biaoqian = models.CharField(null=True,max_length=30)
    key = models.CharField(null=True,max_length=30)
    miaoshu = models.CharField(null=True,max_length=255)
    class Meta:
        db_table = 'article'
