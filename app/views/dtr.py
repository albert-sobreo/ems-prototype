from rest_framework.views import APIView
import datetime
from datetime import date as now
from django.http.response import JsonResponse
from django.views import View
from ..models import *
import sweetify
from django.shortcuts import redirect, render, HttpResponse
from ..serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class DTRList(View):
    def get(self, request, format=None):
        return render(request, 'ems-dtr-list.html')

class DTRView(View):
    def get(self, request, format=None):

        return render(request, 'ems-dtr.html')

# RETURN MESSAGES
# 0 - SUCCESS
# 1 - DID NOT TIMEOUT

class DTRProcess(APIView):
    def timeIn(self, userID):
        employee = User.objects.get(idUser=userID)
        
        dtr = DTR()
        dtr.dateTimeIn = datetime.datetime.now()
        dtr.user = employee
        dtr.date = datetime.date.today()
        dtr.save()
    
    def timeOut(self, userID):
        employee = User.objects.get(idUser=userID)
    
        dtr = employee.dtr.all().latest('pk')
        dtr.dateTimeOut = datetime.datetime.now()
        dtr.save()
        
    def post(self, request, format=None):
        
        id = request.data['idNum']
        employee = User.objects.get(idUser = id)
        try:   
            if employee.dtr.all().latest('pk').dateTimeOut == None:
                if employee.dtr.all().latest('pk').date == datetime.date.today():
                    self.timeOut(id)
                    serializer = UserWithDTRSZ(employee)
                    x = serializer.data
                    x['dtr'] = serializer.data['dtr'][-1]
                    print(x)
                    return Response(x)
                else:
                    self.timeOut(id)
                    self.timeIn(id)
                    # sweetify.sweetalert(request, icon='warning', title='Warning!', text= 'Did not timeout yesterday! Uncertain Timeout recorded', persistent='Dismiss')
                    return JsonResponse({'message':1}, safe=False)
            else:
                self.timeIn(id)
                serializer = UserWithDTRSZ(employee)
                x = serializer.data
                x['dtr'] = serializer.data['dtr'][-1]
                print(x)
                return Response(x)
        except Exception as e:
            print(e)
            self.timeIn(id)
            serializer = UserWithDTRSZ(employee)
            x = serializer.data
            print(x)
            return Response(x)
        
        