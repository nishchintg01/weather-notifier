import requests
import json
import subprocess
import notify2
import pprint
openweatherapi='http://api.openweathermap.org/data/2.5/weather?'
apikey='APPID=09a589b23d3e65029f00268d33badda4'
find_addr='https://ipinfo.io/'

def find_ip(url):
    ip=requests.get(url)
    data=ip.json()
    ipaddr=data['ip']
    loc=data['loc']
    service_provider=data['org']
    country=data['country']
    region=data['region']
    return ipaddr,loc,service_provider,country,region

def weather_forcast(*args,**kwargs):
    location=kwargs['location']
    lat,lon=location.split(',')
    url=args[0]
    token=args[1]
    r=requests.get(url+'lat='+lat+'&lon='+lon+"&"+token)
    data=r.json()
    return data

def send_desktop_notification(**kwargs):
    notify2.init("Weather Notification")
    title="TODAY'S WEATHER"
    temp=kwargs['main']['temp']
    humidity=kwargs['main']['humidity']
    t_min=kwargs['main']['temp_min']
    t_max=kwargs['main']['temp_max']
    wind_speed=kwargs['wind']['speed']
    weather=kwargs['weather'][0]['description']
    icon_path=kwargs['weather'][0]['icon']
    details="Temperature : {} \n Humidity : {} \n Maximum Temperature  : {} \n Minimum Temperature  : {} \n Wind Speed  : {} \n Weather : {}".format(temp,humidity,t_min,t_max,wind_speed,weather)
    n=notify2.Notification(title,details,icon="{}.png".format(icon_path))
    n.set_urgency(2)
    n.show()
    
def main():
    ip,location,ser_pro,county,region=find_ip(find_addr)
    p_data={'ip_addr':ip,'location':location,'service_provider':ser_pro,'country':county,'region':region}
    a=weather_forcast(openweatherapi,apikey,**p_data)
    send_desktop_notification(**a)

if __name__ == '__main__':
    main()
