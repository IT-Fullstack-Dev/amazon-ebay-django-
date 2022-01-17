from rest_framework import serializers
from .models import Myapp
class MyappSerializer(serializers.ModelSerializer):
   class Meta:
       model = Myapp
       fields = ('id','title','description')