# -*- coding: utf-8 -*-

# Sample code for the WhatIsMyBrowser.com API - Version 2
#
# User Agent Database Search
# This sample code shows you how to search the database for useragents
# which match your query. It's not for decoding/parsing user agents,
# you should use the User Agent Parse API Endpoint instead.
#
# It should be used as an example only, to help you get started
# using the API. This code is in the public domain, feel free to
# take it an integrate it with your system as you require.
# Refer to the "LICENSE" file in this repository for legal information.
#
# For further documentation, please refer to the Integration Guide:
# https://developers.whatismybrowser.com/api/docs/v2/integration-guide/
#
# For support, please refer to our Support section:
# https://developers.whatismybrowser.com/api/support/

import requests
import json

# Your API Key
# You can get your API Key by following these instructions:
# https://developers.whatismybrowser.com/api/docs/v2/integration-guide/#introduction-api-key
api_key = ""

# The various search parameters
# This is a basic search for Safari user agents... but it includes
# other sample parameters which have been commented out. Change the
# parameters which get sent to fetch the results you need.
#
# You can also use the Web Based form to experiment and see which
# parameter values are valid:
# https://developers.whatismybrowser.com/api/docs/v2/sample-code/database-search

search_params = {
    "software_name": "Safari",  # "Internet Explorer" "Chrome" "Firefox"
    #"software_version": 71,
    #"software_version_min": 64,
    #"software_version_max": 79,

    #"operating_system_name": "macOS", # "OS X", "Windows", "Linux", "Android" etc
    #"operating_system_version": "Snow Leopard", # Vista, 8.2

    #"operating_platform": "iPhone", #"iPad", "iPhone 5", "Galaxy Gio", "Galaxy Note", "Galaxy S4"
    #"operating_platform_code": "GT-S5660",

    #"software_type": "browser", # "bot" "application"
    #"software_type_specific": "web-browser",  # "in-app-browser", "analyser" "application" "bot" "crawler" etc

    #"hardware_type": "computer", # "computer" "mobile" "server"
    #"hardware_type_specific": "computer", # "phone", "tablet", "mobile", "ebook-reader", "game-console" etc

    #"layout_engine_name": "NetFront", # Blink, Trident, EdgeHTML, Gecko, NetFront, Presto

    #"order_by": "times_seen desc",  # "times_seen asc" "first_seen_at asc" "first_seen_at desc" "last_seen_at desc" "last_seen_at asc" "software_version desc"
    #"times_seen_min": 100,
    #"times_seen_max": 1000,
    #"limit": 250,
}


# Where will the request be sent to
api_url = "https://api.whatismybrowser.com/api/v2/user_agent_database_search"

# -- Set up HTTP Headers
headers = {
    'X-API-KEY': api_key,
}

# -- Make the request
result = requests.get(api_url, params=search_params, headers=headers)

# -- Try to decode the api response as json
result_json = {}
try:
    result_json = result.json()
except Exception as e:
    print(result.text)
    print("Couldn't decode the response as JSON:", e)
    exit()

# -- Check that the server responded with a "200/Success" code
if result.status_code != 200:
    print("ERROR: not a 200 result. instead got: %s." % result.status_code)
    print(json.dumps(result_json, indent=2))
    exit()

# -- Check the API request was successful
if result_json.get('result', {}).get('code') != "success":
    print("The API did not return a 'success' response. It said: result code: %s, message_code: %s, message: %s" % (result_json.get('result', {}).get('code'), result_json.get('result', {}).get('message_code'), result_json.get('result', {}).get('message')))
    #print(json.dumps(result_json, indent=2))
    exit()

# Now you have "result_json" and can store, display or process any part of the response.

# -- Print the entire json dump for reference
print(json.dumps(result_json, indent=2))

# -- Display the user agent and times seen for each parse result in the list
# Don't forget that all the parse data is included in each user agent record as well.
for user_agent_record in result_json.get("search_results").get("user_agents"):
    print("%s - seen: %s times" % (user_agent_record.get("user_agent"), user_agent_record.get("user_agent_meta_data").get("times_seen")))
