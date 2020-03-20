#!/usr/bin/env python
# coding: utf-8

# In[482]:


#imports

import requests 
from bs4 import BeautifulSoup as bs


# In[483]:


#defining which url to parse thru
url = "https://www.hackerearth.com/challenges/"


# In[484]:


#setting up beautifulsoup
page = requests.get(url)
soup = bs(page.content,'html.parser')


# In[485]:


#contents of the page
#print(soup.prettify())


# In[486]:


#to find all our cards, ie where our challenges are defined
b = soup.find_all('div',{"class": "challenge-card-modern"})


# In[487]:


#initialising a dictionary to store info as follows
#challenges = {serial-id : [hackathon-title, hackathon-type, hackathon-by, hackathon-url, reg_start, reg_end, team_size]}

challenges = dict()


# In[488]:


#Useful info from the scraped contents

count = 0
for i in b:
    challenge_title = i.find('span',class_ = 'challenge-list-title')
    challenge_type = i.find('div',class_ = 'challenge-type')
    challenge_by = i.find('div',class_ = 'company-details ellipsis')
    challenge_url = i.find('a',class_ = 'challenge-card-link')
    
    if  challenge_title:
        
        challenge_title = challenge_title.text
        challenge_type = challenge_type.text.strip()
        if challenge_type == "CodeArena":
            continue
        challenge_url = challenge_url['href']
        if not challenge_url.startswith('https'):
            challenge_url = "https://www.hackerearth.com"+challenge_url
        challenge_by = challenge_by.text.strip()
        count+=1
        challenges.update({count : [challenge_title, challenge_type, challenge_by, challenge_url]})


# In[489]:


#to find start and end date.    


# In[490]:


#x = [reg_start, reg_end, team_size]
# scraping thru each site url and then getting further info from that

for i in challenges:
    url = challenges[i][3]
    challenge_page = requests.get(url)
    soup = bs(challenge_page.content,'html.parser')
    x = []
    reg_start = None
    reg_end = None
    team_size = '1'
    if challenges[i][1]=="HACKATHON":
        x= soup.find_all('div',class_="time-div")
        reg_start = x[0].find_all('div')[1].text.strip()
        reg_end = x[1].find_all('div')[1].text.strip()

    else:
        x= soup.find_all('span',class_="timing-text")
        reg_start = x[0].text
        reg_end = x[1].text
        
    x= soup.find_all('span',class_="event-team-size")
    if x:
        team_size = x[0].strong.text.strip()
    challenges[i]+=[reg_start,reg_end,team_size]


# In[491]:


#displaying results
for i in challenges:
    print(i,challenges[i])
    #pass


# In[492]:


#<CODE FOR WRITING INTO A CSV FILE>

    

