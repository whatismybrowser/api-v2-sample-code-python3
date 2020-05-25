# -*- coding: utf-8 -*-

# Sample code for the WhatIsMyBrowser.com API - Version 2
#
# Database Dump Url
# This sample code provides an example of querying the API
# to get the URLs of the latest user agent database dump.
# The database is not for decoding/parsing user agents,
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

# choose the format you want to download by uncommenting it
file_format = "mysql"
#file_format = "csv"
#file_format = "txt"


# Where will the request be sent to
api_url = "https://api.whatismybrowser.com/api/v2/user_agent_database_dump_url?file_format=%s" % file_format

# -- Set up HTTP Headers
headers = {
    'X-API-KEY': api_key,
}

# -- Make the request
result = requests.get(api_url, headers=headers)


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

# -- Copy the `user_agent_database_dump` data to a variable for easier use
user_agent_database_dump = result_json.get("user_agent_database_dump")

print("You requested the %s data format." % file_format)
print("The latest data file contains %s user agents" % user_agent_database_dump.get("num_of_useragents"))
print("You can download it from: %s" % user_agent_database_dump.get("url"))
