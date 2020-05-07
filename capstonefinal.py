
import twitter
import re
import numpy as np
import operator
import pandas as pd

import googlemaps

gmaps = googlemaps.Client(key='')

import gmplot





api = twitter.Api(consumer_key='',
                  consumer_secret='',
                  access_token_key='',
                  access_token_secret='',
                  tweet_mode='extended')


def get_tweets(handle, since_id=0, max_id=0, count=2000):
    if max_id == 0:
        statuses = api.GetUserTimeline(screen_name=handle, count=count, exclude_replies=True, include_rts=False,
                                       since_id=since_id)
    else:
        statuses = api.GetUserTimeline(screen_name=handle, count=count, exclude_replies=True, include_rts=False,
                                       max_id=max_id)
    return statuses


# grabbing tweets from @DCPoliceDept
statuses = get_tweets(handle='DCPoliceDept')

# Writing tweets into CSV file:
"""
with open('tweet.csv',"w") as csvfile:
    for d in statuses:
        #print(d.full_text)
        csvfile.write(d.full_text+"\n\n\n")
"""

# Writing tweets into text file
with open("storedtweets.txt", "w", encoding="utf8") as outFile:
    for d in statuses:
        # print(d.full_text)
        outFile.write(d.full_text + "\n\n")  # +"\n")

# Testing regex

correcttest = "alert: shooting this is a test"
anothercorrecttest = "ALERT: shooting this is a test"
incorrecttest = "this should be wrong"
# Regex to find "alert" at the beginning of the file


testing = re.findall(r'^alert: shooting[a-zA-Z\s]*$', correcttest, re.IGNORECASE)
# print(testing)

testing = re.findall(r'^alert: shooting[a-zA-Z\s]*$', anothercorrecttest, re.IGNORECASE)
# print(testing)

testing = re.findall(r'^alert: shooting[a-zA-Z\s]*$', incorrecttest)
# print(testing)

# loop to implement regex and create new file with regexed lines.

# Alert shooting
global_matches = []
with open("storedtweets.txt", "r", encoding="utf8") as outFile:
    for line in outFile:
        # print(line)
        match = re.findall(r'^alert: shooting[a-zA-Z0-9.\s]*', line.strip(), re.IGNORECASE)
        # print(match)
        if match:
            global_matches.extend(match)
    with open("alertshooting.txt", "w", encoding="utf8") as refinedFile:
        for n in global_matches:
            # print(n)
            refinedFile.write(n + "\n\n")

# Alert Stabbing
global_matches = []
with open("storedtweets.txt", "r", encoding="utf8") as outFile:
    for line in outFile:
        # print(line)
        match = re.findall(r'^alert: stabbing[a-zA-Z0-9.\s]*', line.strip(), re.IGNORECASE)
        # print(match)
        if match:
            global_matches.extend(match)
    with open("alertstabbing.txt", "w", encoding="utf8") as refinedFile:
        for n in global_matches:
            # print(n)
            refinedFile.write(n + "\n\n")

# Alert robbery
global_matches = []
with open("storedtweets.txt", "r", encoding="utf8") as outFile:
    for line in outFile:
        match = re.findall(r'^alert: armed robbery[a-zA-Z0-9.\s]*', line.strip(), re.IGNORECASE)
        # print(match)
        if match:
            global_matches.extend(match)
with open("storedtweets.txt", "r", encoding="utf8") as outFile:
    for line in outFile:
        match = re.findall(r'^alert: robbery[a-zA-Z0-9.\s]+[(gun)a-zA-Z0-9.\s]*', line.strip(), re.IGNORECASE)
        # print(match)
        if match:
            global_matches.extend(match)
    with open("alertrobbery.txt", "w", encoding="utf8") as refinedFile:
        for n in global_matches:
            # print(n)
            refinedFile.write(n + "\n\n")

# Shooting adresses
global_matches = []
with open("alertshooting.txt", "r", encoding="utf8") as outFile:
    for line in outFile:
        # print(line)
        match = re.findall(r'\d{2,5}[\w\s]block[\w\s]{1,40}', line.strip(), re.IGNORECASE)
        # print(match)
        if match:
            global_matches.extend(match)
    with open("shootingaddress.txt", "w", encoding="utf8") as refinedFile:
        for n in global_matches:
            # print(n)
            refinedFile.write(n + "\n\n")

# Stabbing addresses
global_matches = []
with open("alertstabbing.txt", "r", encoding="utf8") as outFile:
    for line in outFile:
        # print(line)
        match = re.findall(r'\d{2,5}[\w\s]block[\w\s]{1,40}', line.strip(), re.IGNORECASE)
        # print(match)
        if match:
            global_matches.extend(match)
    with open("stabbingaddress.txt", "w", encoding="utf8") as refinedFile:
        for n in global_matches:
            # print(n)
            refinedFile.write(n + "\n\n")

# robbery addresses
global_matches = []
with open("alertrobbery.txt", "r", encoding="utf8") as outFile:
    for line in outFile:
        # print(line)
        match = re.findall(r'\d{2,5}[\w\s]block[\w\s]{1,40}', line.strip(), re.IGNORECASE)
        # print(match)
        if match:
            global_matches.extend(match)
    with open("robberyaddress.txt", "w", encoding="utf8") as refinedFile:
        for n in global_matches:
            # print(n)
            refinedFile.write(n + "\n\n")

latitude = []
longitude = []

# geocoding shooting
with open("shootingaddress.txt", "r", encoding="utf8") as outFile:
    for line in outFile:
        geocode_result = gmaps.geocode(line)
        # print(geocode_result)
        new_list = [i["geometry"] for i in geocode_result]
        # print(new_list)
        new_list1 = [i["location"] for i in new_list]
        # print(new_list1)
        lat = [i["lat"] for i in new_list1]
        lng = [i["lng"] for i in new_list1]
        if lat:
            latitude.extend(lat)

        if lng:
            longitude.extend(lng)

shooting_df = pd.DataFrame(columns=['latitude', 'longitude'])

shooting_df['latitude'] = latitude
shooting_df['longitude'] = longitude

print(shooting_df)

latitude = []
longitude = []

# geocoding stabbing
with open("stabbingaddress.txt", "r", encoding="utf8") as outFile:
    for line in outFile:
        geocode_result = gmaps.geocode(line)
        # print(geocode_result)
        new_list = [i["geometry"] for i in geocode_result]
        # print(new_list)
        new_list1 = [i["location"] for i in new_list]
        # print(new_list1)
        lat = [i["lat"] for i in new_list1]
        lng = [i["lng"] for i in new_list1]
        if lat:
            latitude.extend(lat)

        if lng:
            longitude.extend(lng)

stabbing_df = pd.DataFrame(columns=['latitude', 'longitude'])

stabbing_df['latitude'] = latitude
stabbing_df['longitude'] = longitude

print(stabbing_df)

latitude = []
longitude = []

# geocoding robbery
with open("robberyaddress.txt", "r", encoding="utf8") as outFile:
    for line in outFile:
        geocode_result = gmaps.geocode(line)
        # print(geocode_result)
        new_list = [i["geometry"] for i in geocode_result]
        # print(new_list)
        new_list1 = [i["location"] for i in new_list]
        # print(new_list1)
        lat = [i["lat"] for i in new_list1]
        lng = [i["lng"] for i in new_list1]
        if lat:
            latitude.extend(lat)

        if lng:
            longitude.extend(lng)

robbery_df = pd.DataFrame(columns=['latitude', 'longitude'])

robbery_df['latitude'] = latitude
robbery_df['longitude'] = longitude

print(robbery_df)

# locations = robbery_df[['latitude', 'longitude']]


# mapping robbery
latitude_list = robbery_df['latitude']
longitude_list = robbery_df['longitude']

gmap = gmplot.GoogleMapPlotter(38.9072, -77.0369, 12)

gmap.scatter(latitude_list, longitude_list, '#3B0B39', size=150, marker=False)
gmap.apikey = ""
gmap.draw("robbery_map.html")

# locations = robbery_df[['latitude', 'longitude']]


# mapping stabbing addresses
latitude_list = stabbing_df['latitude']
longitude_list = stabbing_df['longitude']

gmap1 = gmplot.GoogleMapPlotter(38.9072, -77.0369, 12)

gmap1.scatter(latitude_list, longitude_list, '#FF4500', size=150, marker=False)

gmap1.apikey = ""
gmap1.draw("stabbing_map.html")

# mapping shooting addresses


latitude_list = shooting_df['latitude']
longitude_list = shooting_df['longitude']

gmap2 = gmplot.GoogleMapPlotter(38.9072, -77.0369, 12)

gmap2.scatter(latitude_list, longitude_list, '#6A0DAD', size=150, marker=False)

gmap2.apikey = ""
gmap2.draw("shooting_map.html")
