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
            data["post_review_link"] = base_url.group(1)+""+(soup.find('a', {'class': 'addReview'})).get('href')
            data["biz_logo_link"]  = "" #str((soup.find('img', {'alt': 'Tripadvisor'})).get('src'))
            data["biz_favicon"] = base_url.group(1)+""+soup.find('link', {'rel': 'icon'}).get('href')
            
           
            review_title_list=[]
            for rev_title in soup.findAll('a', {'class': 'reviewLink'}):
                review_title_list.append(rev_title.get_text().replace("\"", "")) 
            
            
            datet_list=[]
            date_reviewed = soup.findAll('time', {'class': 'date'})
            for date_rev in date_reviewed:
                date_text=date_rev.get_text().strip()
                datet_list.append(date_text) 

            ratings_list=[]
            for rating in soup.findAll('div', {'class': 'v2__EIReviewsRatingsStylesV2__ratingNum'}) :
                ratings_list.append(rating.get_text())
            
            avatar_list=[]
            for avatar in soup.findAll('img', {'alt': 'Apple Logo'}) :
                avatar_list.append(avatar.get('src'))

            
            
            #Please review it and fix the error of missing items, missing items are added menually
            
            reviews_source_list=[]
            reviewers_source = soup.findAll('span', {'class': 'authorLocation'})
            for source_item in reviewers_source:
                reviews_source_list.append(source_item.get_text())
            reviews_source_list.append(reviews_source_list[0])
            reviews_source_list.append(reviews_source_list[3])
            reviews_source_list.append(reviews_source_list[2])
            reviews_source_list.append(reviews_source_list[1])

            #print(json.dumps(reviews_source_list, sort_keys=True, indent=2))
            

            desc_list=[]
            for desc in soup.findAll('p', {'class': 'mainText'}):
                desc_list.append(desc.get_text().strip())
            
            desc_list_1=[]  
            index_1=0
            for descPros in soup.findAll('span', {'data-test': 'pros'}):
                desc_list_1.append(desc_list[index_1]+". Pros: "+descPros.get_text().strip())
                index_1+=1  
                
            desc_list_2=[]   
            index_2=0
            for descCons in soup.findAll('span', {'data-test': 'cons'}):
                desc_list_2.append(desc_list_1[index_2]+". Cons: "+descCons.get_text().strip())
                index_2+=1


            reviewers_name_list=[]
            for rev_name in soup.findAll('span', {'class': 'authorJobTitle'}):
                reviewers_name_list.append(rev_name.get_text())   

            reviews=[]
            keys_list=['name','date','avatar','rating','title','description','source']
            z = list(zip(reviewers_name_list, datet_list, avatar_list , ratings_list, review_title_list, desc_list_2, reviews_source_list))
            for item in z: 
                #users="user_"+str(z.index(item)+1)
                reviews.append(dict(list(zip(keys_list, item))))
            
            #print(json.dumps(reviews, sort_keys=True, indent=2))
            
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

