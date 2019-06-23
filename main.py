import requests
from bs4 import BeautifulSoup
l = []
base_url = "https://pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s=" ##t=0&s= is extension given in url for scrolling through different pages
for pagenum in range(0,30,10):
    print(base_url + str(pagenum) + ".html")
    r = requests.get(base_url + str(pagenum)+".html")
    c = r.content
    code = BeautifulSoup(c,"html.parser")
    ##print(code.prettify())
    all = code.find_all("div",{"class":"propertyRow"})
    
    
    for item in all:
        d = {}

        d["Address"] = item.find_all("span",{"class":"propAddressCollapse"})[0].text
        d["Locality"] = item.find_all("span",{"class":"propAddressCollapse"})[1].text
        d["Price"] = item.find_all("h4",{"class":"propPrice"})[0].text.replace("\n","")

        try:
            d["Beds"] = item.find("span",{"class":"infoBed"}).find("b").text
        except:
            d["Beds"] = "Not Available"

        try:
            d["Area"] = item.find("span",{"class":"infoSqFt"}).find("b").text
        except:
            d["Area"] = "Not Available"


        try:
            d["Full Baths"] = item.find("span",{"class":"infoValueFullBath"}).find("b").text
        except:
            d["Full Baths"] = "Not Available"

        try:
            d["Half Baths"] = item.find("span",{"class":"infoValueHalfBath"}).find("b").text
        except:
            d["Half Baths"] = "Not Available"    

        for column_group in item.find_all("div",{"class":"columnGroup"}):
            for feature_group, feature_name in zip(column_group.find_all("span",{"class":"featureGroup"}),column_group.find_all("span",{"class":"featureName"})):
                #print(feature_group.text, feature_name.text)
                if "Lot Size" in feature_group.text:
                    d["Lot Size"] = feature_name.text

        l.append(d)
    
    

import pandas as pd
df = pd.DataFrame(l)
df.to_csv("Century21Data.csv")
