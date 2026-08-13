from ninja import NinjaAPI,Router,Schema
import requests
from api_man.models import *
from api_man.tasks import *
from ninja.pagination import paginate

app=Router()

@app.get('push/supported/services/country/')
def get_support_sservice_by_country(request):
    
    url="https://streaming-availability.p.rapidapi.com/countries?output_language=en"
    headers = {
        "X-RapidAPI-Key": "f4a02c0783msh7bdc837fa6e133bp1ac29djsnfa175e5270ce",
        "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
    }
    
    response=requests.get(url=url,headers=headers)

    if response.status_code == 200:

        response_data=response.json()
        
        push_rapiad_movie_data.delay(response=response_data)    

        return {"status":True,"message":"Insertion OTT platform service by country wise has initilized! Will notify you as soon as gets completed!","data":""}
        
    return {"status":False,"message":"Something went wrong!","data":response.json()}



@app.get('supported/service/platform/list/')
def supported_service_platform(request,limit: int = 10, offset: int = 0):    
    avaiable_service=AvaiablePlatformServiceByCountry.objects.all()
    results=avaiable_service[offset:offset+limit]    
    return {"status":True,"message":"Avaiable services platform Fetched!","data":[result.detail_serializer() for result in results]}


@app.get('get/supported/platform/')
def get_supported_platform_country(request,name:str):
    
    try:
        country=Country.objects.filter(name__icontains=name).first()
    except Country.DoesNotExist:
        country=None
    
    if country:
        data=[counrty.detail_serializer() for counrty in country.countries.all()]    
        return {"status":True,"message":"Fetched Data by country wise","data":data}
    else:
        return {"status":True,"message":f"{name} requested country service not exist!","data":""}

@app.get('search/country/platform')
def get_supported_platform_country(request,cname:str,pname:str=None):
    
    try:
        country=Country.objects.filter(name__icontains=cname).first()
    except Country.DoesNotExist:
        country=None
    
    if country:
        if pname:
            data=[counrty.detail_serializer() for counrty in country.countries.filter(name__icontains=pname)]    
        else:
            data=[counrty.detail_serializer() for counrty in country.countries.all()]    
        return {"status":True,"message":"Fetched Data by country wise","data":data}
    else:
        return {"status":True,"message":f"{cname} requested country service not exist!","data":""}



@app.get('suggestion/supported/country/')
def get_supported_platform_country(request,name:str):
    
    try:
        country=Country.objects.filter(name__icontains=name)
    except Country.DoesNotExist:
        country=None
    
    if country:
        data=[counrty.serializer() for counrty in country]    
        return {"status":True,"message":"country suggestions!","data":data}
    else:
        return {"status":True,"message":f"{name} requested country service not exist!","data":""}




