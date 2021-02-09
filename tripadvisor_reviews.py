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
            data["biz_url"] = base_url.group(1)
            data["post_review_link"] = base_url.group(1)+""+(soup.find('a', {'class': 'write_review'})).get('href')
            data["biz_logo_link"]  = str((soup.find('img', {'alt': 'Tripadvisor'})).get('src'))
            data["biz_favicon"] = soup.find('link', {'rel': 'icon'}).get('href')
            
            #print(json.dumps(data, sort_keys=True, indent=2))
            
            
           
            review_title_list=[]
            
            #for review_title in soup.findAll('li',{"class":"eqEzMP"}):
                #print(review_title)
            #print(json.dumps(review_title_list, sort_keys=True, indent=2))
            
            ratings_list=[]
            #ratings = soup.findAll('span', {'class': 'jCgDm'})  
            #for rating in ratings:
                #ratings_list.append(rating.get_text())

            #print(json.dumps(ratings_list, sort_keys=True, indent=2))
       
            desc_list=[]
            #reviewDesc = soup.findAll('p', {'class': 'partial_entry'})
            #for desc in reviewDesc:
                #desc_list.append(desc.get_text().strip())
            #print(json.dumps(desc_list, sort_keys=True, indent=2))
            
            reviewers_name_list=[]
            #reviewers_source = soup.findAll('span', {'class': 'cmp-ReviewAuthor'})
            #for revsource in reviewers_source:
                #eviewers_name_list.append((revsource.text).split("-")[0].strip())   
            #print(json.dumps(reviewers_name_list, sort_keys=True, indent=2)) 
            
            datet_list=[]
            date_reviewed = soup.findAll('span', {'class': 'ratingDate'})
            for date_rev in date_reviewed:
                date_text=date_rev.get_text().strip()
                str_list=date_text.split(" ", 1)
                datet_list.append(str_list[1]) 
                
                review_title_list.append("")
                reviewers_name_list.append("")
                desc_list.append("")
                ratings_list.append("")

            reviews_source_list=[]
            reviewers_source = soup.findAll('span', {'class': 'scrname'})
            for source_item in reviewers_source:
                str_split=source_item.find(text=True).split(" ")
                reviews_source_list.append(str_split[1].lower())         
            #print(json.dumps(reviews_source_list, sort_keys=True, indent=2))
            
            avatar_list=[]
            user_avatar = soup.findAll('img', {'class': 'basicImg'})  
            for avatar in user_avatar:
                avatar_list.append(avatar.get('src'))
            #print(json.dumps(avatar_list, sort_keys=True, indent=2))
            
            reviews=[]
            keys_list=['name','date','avatar','rating','title','description','source']
            z = list(zip(reviewers_name_list, datet_list, avatar_list , ratings_list, review_title_list, desc_list, reviews_source_list))
            for item in z: 
                #users="user"+str(z.index(item)+1)
                reviews.append(dict(list(zip(keys_list, item))))
            
            data["reviews"] = reviews
            print(json.dumps(data, sort_keys=True, indent=2))
            
            mainKeyword=(base_url.group(1).split("."))[1]
            with open('./completed scrapers/json_files/'+ mainKeyword +'.json', 'w+') as outfile:
                json.dump(data, outfile)

            #print(soup.prettify())
                    
        
except HTTPError as e:
    print("The server returned an HTTP error::"+str(e))
except URLError as e:
    print("The server could not be found!::"++str(e))
