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
        
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}
        
        with urllib_2.urlopen(urllib_2.Request(url_arg, headers=hdr)) as response:
            
            soup = BeautifulSoup(response.read(), features="html.parser")
            data = {}
            
            data["website"] = soup.title.text
            base_url = re.search('https?://([A-Za-z_0-9.-]+).*', url_arg)
            data["post_site_url"] = base_url.group(1)
            data["biz_logo_link"]  = " " #str((soup.find('img', {'height': '87'})).get('src'))
            data["biz_favicon"] = base_url.group(1)+""+(soup.find('link', {'rel': 'icon'})).get('href')
            
            for div in soup.findAll('div', {'id': 'reviews'}):
                for child in div.findAll('a', {'class': '@flex-initial'}):
                    data["post_review_link"]=data["post_site_url"]+""+child.get("href")
            
            review_title_list=[]
            for title in soup.findAll('div', {'class': 'list'}) :
                for child in title.findAll('ul'):
                      review_title_list.append(child.find('li').string.strip())
            
            
            ratings_list=[]
            for rating in soup.findAll('div', {'class': 'list-body'}) :
                    ratings_list.append(rating.find('span',{'class':'@text-gray-600'}).get_text())      

            desc_list=[]
            for div in soup.findAll('div', {'class': 'list'}) :
                for child in div.findAll('div', {'class': 'review-content'}):
                    desc_list.append(child.get_text().strip())    
            
            review_date_list=[]
            for review_date in soup.findAll('div', {'class': 'list'}) :
                for child in review_date.findAll('div', {'class': '@flex-initial'}):
                    review_date_list.append(child.get_text().strip())    
            
            reviewers_name_list=[]
            for review_name in soup.findAll('div', {'class': 'list'}) :
                for child in review_name.findAll('div', {'class': '@flex-auto'}):
                    reviewers_name_list.append(child.find('span',{'class':'@text-gray-navy'}).get_text().strip().replace("*.",""))    
            
            source_list=[]
            for review_source in soup.findAll('div', {'class': 'list'}) :
                for child in review_source.findAll('div', {'class': '@flex-auto'}):
                    source_list.append(child.find('span',{'class':'@text-link'}).get_text().strip().replace("*.",""))
            
            avatar_list=[]
            for review_avatar in soup.findAll('div', {'class': 'list'}) :
                for child in review_avatar.findAll('div', {'class': '@flex-auto'}):
                    avatar_list.append("")


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

