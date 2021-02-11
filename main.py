import re
import sys

if __name__ == "__main__":

    
    print ("\nScraper Started...\n")

    request_url=""

    site_modules = ["www.dealerrater.com","www.insiderpages.com","www.wellness.com","www.thumbtack.com","www.homeadvisor.com","www.avvo.com","www.tripadvisor.com","www.indeed.com","www.glassdoor.com","www.cargurus.com","www.caredash.com","www.zocdoc.com", "www.doctor.com","www.healthgrades.com"]
    input_urls = []
    
    
    url_list = [post_url for post_url in input("Enter Comma Seperated Post Urls (https://...)::\n").split(',')] 
    
    for post_url in url_list:
        _post_url_= post_url.strip(" ")
        base_url = re.search('https?://([A-Za-z_0-9.-]+).*', _post_url_)
        post_path = _post_url_.replace("https://"+base_url.group(1),"")
        
        input_urls.append({"base_url": base_url.group(1), "post_path" : post_path})
    
    for input_url in input_urls:
   
        if input_url["base_url"] in site_modules:
            request_url = "https://"+input_url["base_url"]+input_url["post_path"]

            module_name = str(input_url["base_url"]).split(".")[1]
            module = __import__(module_name+"_reviews")

            print("\n\nFetching reviews data for::\n"+str(request_url))
            module.get_data(request_url)
            
        else:
            request_url = "https://"+input_url["base_url"]+input_url["post_path"]
            print("The requested source is not in our listed urls::"+str(request_url))


