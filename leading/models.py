from django.db import models

class Gbook(models.Model):
    o_name = models.CharField(max_length=20,null=False)
    time = models.DateTimeField(auto_now_add=True)
    cont = models.CharField(max_length=255,null=True)
    email = models.CharField(max_length=50,null=True)

    class Meta:
        db_table = 'gbook'