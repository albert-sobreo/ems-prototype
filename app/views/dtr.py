from rest_framework.views import APIView
from datetime import datetime
from datetime import date as now
from django.http.response import JsonResponse
from django.views import View
from ..models import *
import sweetify
from django.shortcuts import redirect, render, HttpResponse

class DTRView(View):
    def get(self, request, format=None):

        return render(request, 'ems-dtr.html')

class DTRProcess(APIView):
    def timeIn():
        pass
    
    def timeOut():
        pass
    
    def post(self, request, format=None):
        
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)