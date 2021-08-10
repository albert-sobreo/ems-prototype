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
from decimal import Decimal

import datetime

class DTRList(View):
    def get(self, request, format=None):
        context = {
            'User': User.objects.all()
        }
        return render(request, 'ems-dtr-list.html', context)

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

        rh = Decimal(0)
        ut = Decimal(0)
        ot = Decimal(0)
        

        tolerance = datetime.timedelta(minutes=5)

        breakStart = datetime.datetime.combine(datetime.date.today(), datetime.time(12))
        breakEnd = datetime.datetime.combine(datetime.date.today(), datetime.time(13))

        scheduleTimeIn = datetime.datetime.combine(datetime.date.today(), employee.schedule.timeIn)
        scheduleTimeOut = datetime.datetime.combine(datetime.date.today(), employee.schedule.timeOut)

        durationSchedule = scheduleTimeOut - scheduleTimeIn - datetime.timedelta(hours=1) #timedelta
        durationDTR = dtr.dateTimeOut - dtr.dateTimeIn #timedelta
        durationDiff = abs(durationSchedule - durationDTR)
        

        timeInDiff = abs(scheduleTimeIn - dtr.dateTimeIn) #timedelta
        timeOutDiff = abs(scheduleTimeOut - dtr.dateTimeOut) #timedelta

        durationDTR = durationDTR - datetime.timedelta(hours=1) if dtr.dateTimeOut >= breakEnd and dtr.dateTimeIn <= breakStart else durationDTR

        # EARLY OR ON TIME
        if dtr.dateTimeIn <= scheduleTimeIn or timeInDiff < tolerance:
            durationDTR = durationDTR - timeInDiff
            timeInDiff = datetime.timedelta(0)
        
        # TIME IN ON TIME AND TIME OUT ON TIME
        if timeInDiff < tolerance and timeOutDiff < tolerance:
            rh = Decimal(8.0)
        
        # IF TIME IN ON TIME
        print(timeInDiff, timeOutDiff, durationDTR, durationSchedule)
        
        # if timeInDiff == datetime.timedelta(0):
        print(1)
        # UNDERTIME TIME OUT
        if timeOutDiff > tolerance:
            if dtr.dateTimeOut < scheduleTimeOut:
                print(2)
                ut += Decimal(timeOutDiff.seconds/3600)
                print(ut)
        # OVERTIME TIME OUT
            else:
                ot += Decimal(timeOutDiff.seconds/3600)
        # if timeOutDiff > tolerance and durationDTR > durationSchedule:
        #     print(3)
        #     
        rh += Decimal(durationDTR.seconds/3600)
        # IF TIME IN LATE
        # else:
        #     print(4)
        #     # UNDERTIME TIME OUT
        #     if durationDTR < durationSchedule and durationDiff > 2*tolerance:
        #         print(5)
        #         ut += Decimal(durationDiff.seconds/3600)
        #     if durationDTR > durationSchedule and durationDiff > 2*tolerance:
        #         print(6)
        #         ot += Decimal(durationDiff.seconds/3600)
        #     if durationDiff < 2*tolerance:
        #         print(7)
        #         rh = Decimal(8.0)
        ut += Decimal(timeInDiff.seconds/3600)
        print(ut)
        rh = rh - ot
        print(rh)

        dtr.rh = rh
        dtr.ut = ut
        dtr.ot = ot
        dtr.save()
        
    def post(self, request, format=None):
        
        id = request.data['idNum']
        employee = User.objects.get(idUser = id)
        #try:   
        if employee.dtr.all().latest('pk').dateTimeOut == None:
            if str(employee.dtr.all().latest('pk').date) == str(datetime.date.today()):
                self.timeOut(id)
                serializer = UserWithDTRSZ(employee)
                x = serializer.data
                x['dtr'] = serializer.data['dtr'][-1]
                return Response(x)
            else:
                print('b0ss')
                self.timeOut(id)
                self.timeIn(id)
                # sweetify.sweetalert(request, icon='warning', title='Warning!', text= 'Did not timeout yesterday! Uncertain Timeout recorded', persistent='Dismiss')
                return JsonResponse({'message':1}, safe=False)
        else:
            self.timeIn(id)
            serializer = UserWithDTRSZ(employee)
            x = serializer.data
            x['dtr'] = serializer.data['dtr'][-1]
            return Response(x)
        # except Exception as e:
        #     print(e)
        #     print('b0ss2')
        #     self.timeIn(id)
        #     serializer = UserWithDTRSZ(employee)
        #     x = serializer.data
        #     return Response(x)
        
        