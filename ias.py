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

scraping_links = ["https://fellows.ias.ac.in/profile/v/FL1974002",
                  "https://fellows.ias.ac.in/profile/v/FL1969002"]
# for i in links_new:
#     if "https://fellows.ias.ac.in/profile/v/" in i:
#         scraping_links.append(i)
#     else:
#         continue


scrape_details = []

for i in scraping_links:
    link_code = requests.get(i)
    soup1 = BeautifulSoup(link_code.content, 'lxml')
    name = soup1.find_all('h1')[0]
    affiliation = soup1.find_all(class_="affiliation")[0]
    fellowship_details = soup1.find_all(class_="fellowship")[0]
    council_presence = soup1.find_all(class_="council-service")
    print(council_presence)
    council_presence_details = []
    for i in council_presence:
        council_presence_details.append(i.text)
        if len(council_presence_details) >= 2:
            for j in council_presence_details:
                if j.startswith('Year of Birth'):
                    year_of_birth = j[15:]
                else:
                    council_service = j[34:]
        else:
            year_of_birth = council_presence_details[0][15:]
    specialization = soup1.find_all(class_="specialization")[0]

    scrape_details.append([name.text, affiliation.text,
                           fellowship_details.text, year_of_birth, council_service, specialization.text[16:]])

tweet_df = pd.DataFrame(scrape_details, columns=[
                        'name', 'affiliation', 'fellow_details', 'year_of_birth', 'council_service', 'specialization'])

tweet_df.to_csv('results.csv', index=False)
