from numpy.testing._private.utils import KnownFailureException
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time

# source_code = requests.get(
#     "https://fellows.ias.ac.in/listing/a?profile.name.display=&contact.city=&fellowship.section=&fellowship.yearelected=&id=%40FL")
# soup = BeautifulSoup(source_code.content, 'lxml')
# data = []
# links = []


# def remove_duplicates(l):  # remove duplicates and unURL string
#     for item in l:
#         match = re.search("(?P<url>https?://[^\s]+)", item)
#         if match is not None:
#             links.append((match.group("url")))


# for link in soup.find_all('a', href=True):
#     data.append(str(link.get('href')))
# flag = True
# remove_duplicates(data)
# while flag:
#     try:
#         for link in links:
#             for j in soup.find_all('a', href=True):
#                 temp = []
#                 source_code = requests.get(link)
#                 soup = BeautifulSoup(source_code.content, 'lxml')
#                 temp.append(str(j.get('href')))
#                 remove_duplicates(temp)

#                 if len(links) > 162:  # set limitation to number of URLs
#                     break
#             if len(links) > 162:
#                 break
#         if len(links) > 162:
#             break
#     except Exception as e:
#         print(e)
#         if len(links) > 162:
#             break

# links_new = links.copy()

import pandas as pd

df = pd.read_csv('/Users/rajathcs/Desktop/Book1.csv')

scraping_links = list(set(df['urls'].tolist()))

scrape_details = []

for i in scraping_links:
    link_code = requests.get(i)
    soup1 = BeautifulSoup(link_code.content, 'lxml')
    fellow_url = i
    p_tags = soup1.findAll('p')
    try:
        name = soup1.find_all('h1')[0]
        name = name.text
        fellow_address = str(
            p_tags[(len(p_tags)-3):(len(p_tags)-1)][0].contents[2]) + str(
            p_tags[(len(p_tags)-3):(len(p_tags)-1)][0].contents[4])
        if '@' not in str(
                p_tags[(len(p_tags)-3):(len(p_tags)-1)][1].contents[1]):
            fellow_email = str(
                p_tags[(len(p_tags)-3):(len(p_tags)-1)][1].contents[-2]).strip()
            if '@' not in fellow_email:
                fellow_email = ""
                fellow_number = str(
                    p_tags[(len(p_tags)-3):(len(p_tags)-1)][1].contents[1]).strip()
            else:
                fellow_email = ""
                fellow_number = ""
        elif '@' in str(
                p_tags[(len(p_tags)-3):(len(p_tags)-1)][1].contents[1]):
            fellow_email = str(
                p_tags[(len(p_tags)-3):(len(p_tags)-1)][1].contents[1]).strip()
        affiliation = soup1.find_all(class_="affiliation")[0]
        affiliation = affiliation.text
        fellowship_details = soup1.find_all(class_="fellowship")[0]
        fellowship_details = fellowship_details.text
        council_presence = soup1.find_all(class_="council-service")
        council_presence_details = []
        for i in council_presence:
            council_presence_details.append(i.text)

        specialization = soup1.find_all(class_="specialization")[0]
        specialization = specialization.text[16:]
    except:
        # fellow_url = ""
        fellow_address = ""
        fellow_email = ""
        affiliation = ""
        fellowship_details = ""
        council_presence = ""
        council_presence_details = ""
        specialization = ""
        fellow_number = ""

    scrape_details.append([fellow_url, name, affiliation,
                           fellowship_details, council_presence_details, specialization, fellow_address, fellow_number, fellow_email])

ias_df = pd.DataFrame(scrape_details, columns=[
    'fellow_url', 'name', 'affiliation', 'fellow_details', 'council_presence_details', 'specialization', 'fellow_address', 'fellow_number', 'fellow_email'])


ias_df.to_csv('results.csv', index=False)
