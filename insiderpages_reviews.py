from bs4 import BeautifulSoup
import urllib.request as urllib_2
from urllib.error import HTTPError
from urllib.error import URLError
import json
import csv
import re

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
    
            data["website"] = soup.title.get_text() 
            base_url = re.search('https?://([A-Za-z_0-9.-]+).*', url_arg)
            data["post_site_url"] = base_url.group(1)
            data["post_review_link"] =  base_url.group(1)+""+(soup.find('a', {'id': 'war_link'})).get('href') 
            data["biz_logo_link"]  = str((soup.find('img', {'class': 'logo'})).get('src'))
            data["biz_favicon"] = base_url.group(1)+""+(soup.find('link', {'rel': 'icon'})).get('href')
            
            desc_list=[] 
            for desc in soup.findAll('p', {'class': 'description'}):
                if desc.get_text().strip() in desc_list:
                    continue
                else:
                    desc_list.append(desc.get_text().strip())             
            
            review_title_list=[]
            for rev_title in soup.findAll('span', {'class': 'review_title'}):
                review_title_list.append(rev_title.get_text().strip()) 
            
            reviewers_name_list=[]
            reviews_source_list=[]
            for reviewer in soup.findAll('p', {'class': 'reviewer'}):
                strr=((reviewer.find(text=True)).strip()).split(' ')
                if len(strr)!=1:
                    reviewers_name_list.append((strr[1:2])[0])
                    reviews_source_list.append((strr[3:4])[0])
                elif len(strr)==1:
                    reviewers_name_list.append("Empty")
                    reviews_source_list.append("Empty")    
            
            dtreviewed_list=[]
            for date_rev in soup.findAll('abbr', {'class': 'dtreviewed'}):
                dtreviewed_list.append(date_rev.get_text()) 
            
            ratings_list=[]
            ratings = soup.findAll('abbr', {'class': 'rating'})  
            for rating in ratings:
                ratings_list.append(rating.get('title'))           

            avatar_list=[]
            user_avatar1 = soup.findAll('img', {'class': 'home_content_photo'})  
            for avatar1 in user_avatar1:
                avatar_list.append(avatar1.get('src'))                
            
            for avatar2 in soup.findAll('img', {'rel': 'nofollow'})  :
                avatar_list.append(avatar2.get('src'))                
  
            reviews_list=[]
            reviewDesc = soup.findAll('p', {'class': 'review_text'})
            for review in reviewDesc:
                reviews_list.append(review.get_text())                
            
            reviews=[]
            keys_list=['name','date','avatar','rating','title','description','source']
            z = list(zip(reviewers_name_list, dtreviewed_list, avatar_list, ratings_list, review_title_list, desc_list, reviews_source_list))
            for item in z: 
                #users="user_"+str(z.index(item)+1)
                reviews.append(dict(list(zip(keys_list, item))))

            
            data["reviews"] = reviews
            print(json.dumps(data, sort_keys=True, indent=2))
            
            
            mainKeyword=(base_url.group(1).split("."))[1]
            with open('./completed scrapers/json_files/'+ mainKeyword +'.json', 'w') as outfile:
                json.dump(data, outfile)

            #print(soup.prettify())
       
        
except HTTPError as e:
    print("The server returned an HTTP error")
except URLError as e:
    print("The server could not be found!")
