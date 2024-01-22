
from time import sleep
from bs4 import BeautifulSoup
import requests
import csv

ask_name_file = input("Please type in the file to write to, or file name to create:") #create file 


headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15'}

sport_roster_links_list = []
while True:
    inp = input("Please type the link of a college sports website. Make sure it is the main page of the sports website:")
    response = requests.get(inp, headers=headers)
    if response.status_code == requests.codes.not_found:
        print("Error")
    else:
        break

load_page = BeautifulSoup(response.content, 'html.parser')

get_nav = load_page.find('nav')
get_a_elements = get_nav.find_all('a')
for element in get_a_elements:
        link = element.get('href')
        if 'roster' in link:
            sport_roster_links_list.append(inp + link)
            

sleep(5)

for sport_link in sport_roster_links_list: #go through each sport in the respective college
    player_profile_links_list= []
    majors_concentration_list = []

    request_sport_link = requests.get(sport_link) #get sport link (which is the link of the roster. Such as godolfins.com/sports/football/roster)
    examine_sport_page = BeautifulSoup(request_sport_link.content, 'html.parser')

    get_all_profile_links = examine_sport_page.find_all('div', attrs = {"class" : "sidearm-roster-player-bio hide-on-small-down"} ) #finds each player
   
    for player in get_all_profile_links:    
        link = player.find('a')['href']
        player_profile_links_list.append(inp + link) #appends all one player per time from the respective roster page
    sleep(5)

    for player_profile in player_profile_links_list:
        profile_request = requests.get(player_profile)
        load_profile = BeautifulSoup(profile_request.content, 'html.parser')
        find_details = load_profile.find_all('dl', class_ = "flex-item-1") #loading all details names using dl tag (I.e. Hometown, Major . But also gives major)

        for detail in find_details: #getting details
            detail_text = detail.get_text()
            if "Major" in detail_text or "Concentration" in detail_text:
                major_concentration = detail.find('dd').get_text()
                majors_concentration_list.append(major_concentration)

    data_file = open(ask_name_file, 'a+') 
    writer = csv.writer(data_file)
    writer.writerow([sport_link, ",", majors_concentration_list])
    data_file.close()
    sleep(5)
print("Success!")




    
