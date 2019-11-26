from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime as T

from pymongo import MongoClient as mc
client = mc("mongodb://localhost:27017/myProject")
db=client.nayan
entries=db.entries
hosts=db.hosts

import smtplib
gmail_user = 'you@email.com-enter your gmail' 
gmail_password = 'password-enter your password'  


def checkout(request):
    if request.method== 'POST':
        visitor=entries.find_one({'visitorName':request.POST.get('visitorName'),'checkoutTime':None})
        if visitor==None:
            return render(request ,'home/msg.html',{'msg':"Not Found"})
        checkoutTime=T.now()
        entries.update_one(visitor,
            {"$set": {'checkoutTime':checkoutTime}}
             )
        to = visitor["visitorEmail"]
        subject = 'OMG Super Important Message'
        body1= f'hostName:{visitor["hostName"]}\nhostEmail:{visitor["hostEmail"]}\nhostPhoneNo:{visitor["hostPhoneNo"]}\nhostAdress:{visitor["hostAdress"]}\n'
        
        body2=f'visitorName:{visitor["visitorName"]}\nvisitorEmail:{to}\nvisitorPhoneNo:{visitor["visitorPhoneNo"]}\nvisitorAdress:{visitor["visitorAdress"]}\n'
        
        body3=f'checkinTime:{visitor["checkinTime"]}\ncheckoutTime:{checkoutTime}\n'
        
        email_text = """\
To: %s
Subject: %s

%s
""" % (to,subject,body1+body2+body3)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to, email_text)
        server.close()
        return render(request ,'home/msg.html',{'msg':"Done"})
    else:
        return render(request ,'home/checkout.html')

def index(request):
    if request.method== 'POST':
        hostName=request.POST.get('hostName')
        visitors=list(entries.find({'hostName':hostName}))
        return render(request ,'home/visitors.html',{'visitors':visitors,'host':hostName})
    else:
        hostsList=hosts.find_one({})['list']
        return render(request ,'home/index.html',{'hosts':hostsList})
def new(request):
    if request.method== 'POST':
        hostName=request.POST.get('hostName')
        hostEmail=request.POST.get('hostEmail')
        hostPhoneNo=request.POST.get('hostPhoneNo')
        hostAdress=request.POST.get('hostAdress')
        visitorName=request.POST.get('visitorName')
        visitorEmail=request.POST.get('visitorEmail')
        visitorPhoneNo=request.POST.get('visitorPhoneNo')
        visitorAdress=request.POST.get('visitorAdress')
        checkinTime=T.now()
        entries.insert_one({'hostName':hostName,'hostEmail':hostEmail,'hostPhoneNo':hostPhoneNo,
                                    'hostAdress':hostAdress,'visitorName':visitorName,'visitorEmail':visitorEmail,
                                    'visitorPhoneNo':visitorPhoneNo,'visitorAdress':visitorAdress,'checkinTime':checkinTime,'checkoutTime':None})

        hosts.update_one({},{ '$addToSet' : { "list": hostName } })
        to = hostEmail
        subject = 'OMG Super Important Message'
        body = f'visitorName:{visitorName}\nvisitorEmail:{visitorEmail}\nvisitorPhoneNo:{visitorPhoneNo}\nvisitorAdress:{visitorAdress}\ncheckinTime:{checkinTime}\n'

        email_text = """\
To: %s
Subject: %s

%s
""" % (to,subject,body)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to, email_text)
        server.close()

        return render(request ,'home/msg.html',{'msg':"Done"})
    else:
        return render(request ,'home/new.html')
