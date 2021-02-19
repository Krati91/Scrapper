from django.shortcuts import render
from django.http import HttpResponse
from .models import (
    Event,
    interesting_url,
    non_interesting_url
)    

import requests
from bs4 import BeautifulSoup
import json 

main_context = []

# Create your views here.
def show_list(request): 
    main_context.clear()
    sites = [
            {
                'title':'Eventbrite',
                'url':'https://www.eventbrite.com/d/online/all-events/'
            },
            {
                'title':'Insider',
                'url':'https://insider.in/all-digital-events-in-online'
            },
            {
                'title':'Naad Yoga Council',
                'url':'https://www.naadyogacouncil.com/en/events/'
            }
            ]

    for site in sites:
        html_content = requests.get(site['url']).text
        soup = BeautifulSoup(html_content,'lxml')

        if site['title'] == 'Eventbrite':
            event_tag = soup.find('ul',{'class':'search-main-content__events-list'})
            events = event_tag.find_all('li')

            event_list = []
            for i in range(10):
                href = events[i].find('a').get('href')
                title = events[i].find('div',{'data-spec':'event-card__formatted-name--content'}).getText()

                event_list.append({'title':title,'url':href})

        elif site['title'] == 'Insider':
            event_tag = soup.find('div',{'class':'card-list-wrapper'}).find('ul',{'class':'card-list'})
            events = event_tag.find_all('li')

            event_list = []
            for i in range(10):
                href = events[i].find('a').get('href')
                title = events[i].find('span',{'class':'event-card-name-string'}).getText()

                event_list.append({'title':title,'url':'https://insider.in'+href})
                       
        else:
            event_tag = soup.find('div',{'class':'tribe-events-loop'})
            events = event_tag.find_all('div',{'class':'type-tribe_events'})

            event_list = []
            for i in range(10):
                href = events[i].find('a',{'class','url'}).get('href')
                title = events[i].find('a',{'class','url'}).getText()

                title = title.replace('\n','').replace('\t','')
    
                event_list.append({'title':title,'url':href})
        
        
        context = {
            'page_title':site['title'],
            'event_list':event_list
        }
        
        main_context.append(context)
    
    #print(*main_context, sep='\n')        
    
    return render(request,'scrapper/eventList.html',{'context':main_context})

def collect_structured_data(request):
    for item in main_context:
        for event in item['event_list']:
            url = event['url']

            html_content = requests.get(url).text
            soup = BeautifulSoup(html_content,'lxml')
            data_tag = soup.find('script',{'type':'application/ld+json'})
                    
            #print("".join(data_tag))
            if item['page_title'] == 'Naad Yoga Council':
                jsonData = json.loads("".join(data_tag.contents))[0]
            else:
                jsonData = json.loads("".join(data_tag.contents))    
                
            print(jsonData)
            event = Event.objects.create(site_name=item['page_title'],start_date=jsonData['startDate'],end_date=jsonData['endDate'],name=jsonData['name'],url=jsonData['url'],event_type=jsonData['@type'],description=jsonData['description'])            
    main_context.clear()
    return render(request,'scrapper/details.html',{'data':'Collected'})
    
def categorize_url(request):
    events = Event.objects.all()
    for event in events:
        if event.interest_group:
            interesting_url.objects.create(url=event.url,event=event)
        else:
            non_interesting_url.objects.create(url=event.url)

    return HttpResponse("Categorized")                
       