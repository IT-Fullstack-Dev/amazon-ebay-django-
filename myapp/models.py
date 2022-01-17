from django.db import models

# Create your models here.
class Myapp(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    
    def _str_(self):
        return self.title

class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        db_table = 'Todo'        
