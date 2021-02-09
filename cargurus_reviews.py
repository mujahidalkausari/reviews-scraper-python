from bs4 import BeautifulSoup
import urllib.request as urllib_2
from urllib.error import HTTPError
from urllib.error import URLError
import json
import csv
import re
import sys

try:
    def get_data(url_arg):
        
        hdr = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset' : 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding' : 'none',
               'Accept-Language' : 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}
        
        with urllib_2.urlopen(urllib_2.Request(url_arg)) as response:
            
            soup = BeautifulSoup(response.read(), features="html.parser")
            data = {}
            
            data["website"] = soup.title.text
            base_url = re.search('https?://([A-Za-z_0-9.-]+).*', url_arg)
            data["post_site_url"] = base_url.group(1)
            data["biz_logo_link"]  = " " #str((soup.find('img', {'height': '87'})).get('src'))
            data["biz_favicon"] = (soup.find('link', {'rel': 'icon'})).get('href')
            data["post_review_link"]=url_arg+""+(soup.find('div', {'class': 'reviews-header'})).find('a').get('href')
            
                        
            review_title_list=[]
            for review_ in soup.findAll('meta', {'property': 'ratingValue'}):
                review_title_list.append("")
            #print(json.dumps(review_title_list, sort_keys=True, indent=2))
            
            ratings_list=[]
            for rating in soup.findAll('meta', {'property': 'ratingValue'}):
                ratings_list.append(rating.get('content'))
            #print(json.dumps(ratings_list, sort_keys=True, indent=2))
    
            desc_list=[]
            for desc in soup.findAll('div', {'class': 'cg-userReviewText'}):
                desc_list.append(desc.get_text().strip())    
            #print(json.dumps(desc_list, sort_keys=True, indent=2))
            
            review_date_list=[]
            for _date in soup.findAll('span', {'property': 'dateCreated'}):
                review_date_list.append(_date.get_text().strip())   
            #print(json.dumps(review_date_list, sort_keys=True, indent=2))
            
            reviewers_name_list=[]
            for _name in soup.findAll('span', {'property': 'name'}):
                reviewers_name_list.append(_name.get_text().strip())   
            #print(json.dumps(reviewers_name_list, sort_keys=True, indent=2))
            
            source_list=[]
            for review_avatar in soup.findAll('div', {'class': 'avatar-image'}) :
                review_avatar_url=review_avatar.find('span').get('style').replace("ackground-image: url(","").replace(");","")
                source_list.append("")
            #print(json.dumps(source_list, sort_keys=True, indent=2))
            
            avatar_list=[]
            for review_avatar in soup.findAll('div', {'class': 'avatar-image'}) :
                review_avatar_url=review_avatar.find('span').get('style').replace("background-image: url(","").replace(");","")
                avatar_list.append(review_avatar_url)
            #print(json.dumps(avatar_list, sort_keys=True, indent=2)) 

            reviews=[]
            keys_list=['name','date','avatar','rating','title','description','source']
            z = list(zip(reviewers_name_list, review_date_list, avatar_list , ratings_list, review_title_list, desc_list, source_list))
            for item in z: 
                #users="user"+str(z.index(item)+1)
                reviews.append(dict(list(zip(keys_list, item))))
            
            data["reviews"] = reviews
            print(json.dumps(data, sort_keys=True, indent=2))
            
            mainKeyword=(base_url.group(1).split("."))[1]
            with open('./json_files/'+ mainKeyword +'.json', 'w') as outfile:
                json.dump(data, outfile)

            #print(soup.prettify())
                        
    
except HTTPError as e:
    print("The server returned an HTTP error")
except URLError as e:
    print("The server could not be found!")
