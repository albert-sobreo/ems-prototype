from rest_framework import fields, serializers
from .models import *

########## DTR ##########
class DTRSZ(serializers.ModelSerializer):
    class Meta:
        model = DTR
        fields = '__all__'
        





########## USER ##########
class UserWithDTRSZ(serializers.ModelSerializer):
    dtr = DTRSZ(read_only=True, many=True)
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'idUser',
            'dtr'
        ]
        depth = 1