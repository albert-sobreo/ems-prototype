from rest_framework import fields, serializers
from .models import *

########## DTR FILTER ##########
class DateFilterDTRSZ(serializers.ListSerializer):
    @classmethod
    def many_init(cls, *args, **kwargs):
        # Instantiate the child serializer.
        kwargs['child'] = cls()
        # Instantiate the parent list serializer.
        return DateFilterDTRSZ(*args, **kwargs)

    def to_representation(self, data):
        data = data.filter(date__range=['2021-08-12', '2021-08-13'])
        return super(DateFilterDTRSZ, self).to_representation(data)





########## DTR ##########
class DTRSZ(serializers.ModelSerializer):
    class Meta:
        model = DTR
        fields = '__all__'

        list_serializer_class = DateFilterDTRSZ
        





########## USER ##########
class UserWithDTRSZ(serializers.ModelSerializer):
    dtr = DTRSZ(read_only=True, many=True, context='what')
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'idUser',
            'dtr'
        ]
        depth = 1