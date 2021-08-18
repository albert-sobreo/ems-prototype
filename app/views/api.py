from decimal import Decimal
from typing import List
from django import views
from django.contrib.auth.decorators import permission_required
from django.db.models import query
from django.http.response import Http404, JsonResponse
from rest_framework import viewsets
from ..serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response
import rest_framework.status as status

from ..models import *

from rest_framework.permissions import IsAuthenticated

from datetime import datetime

########## USER WITH DTR ##########
class UserWithDTRAPI(viewsets.ModelViewSet):
    serializer_class = UserWithDTRSZ
    queryset = User.objects.all()
