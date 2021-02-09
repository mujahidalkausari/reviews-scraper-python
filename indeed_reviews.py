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
            data["post_review_link"] = base_url.group(1)+""+(soup.find('a', {'role': 'link'})).get('href')
            data["biz_logo_link"]  = str((soup.find('img', {'class': 'cmp-CompactHeaderCompanyLogo-logo'})).get('src'))
            data["biz_favicon"] = base_url.group(1)+""+(soup.find('link', {'rel': 'icon'})).get('href')
            
           
            review_title_list=[]
            for rev_title in soup.findAll('a', {'class': 'cmp-Review-titleLink'}):
                review_title_list.append(rev_title.get_text().strip()) 

            
            ratings_list=[]
            ratings = soup.findAll('button', {'class': 'cmp-ReviewRating-text'})  
            for rating in ratings:
                ratings_list.append(rating.get_text())
            
            
            desc_list=[]
            reviewDesc = soup.findAll('div', {'class': 'cmp-Review-text'})
            for desc in reviewDesc:
                desc_list.append(desc.get_text().strip())

            
            reviews_source_list=[]
            dtreviewed_list=[]
            reviewers_name_list=[]
            avatar_list=[]

            for revsource in soup.findAll('span', {'class': 'cmp-ReviewAuthor'}):
                reviewers_name_list.append((revsource.text).split("-")[0].strip())
                reviews_source_list.append((revsource.text).split("-")[1].strip())
                dtreviewed_list.append((revsource.text).split("-")[2].strip())
                avatar_list.append("")      
 
            
            reviews=[]
            keys_list=['name','date','avatar','rating','title','description','source']
            z = list(zip(reviewers_name_list, dtreviewed_list, avatar_list , ratings_list, review_title_list, desc_list, reviews_source_list))
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
