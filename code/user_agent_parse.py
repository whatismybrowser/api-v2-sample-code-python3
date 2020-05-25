# -*- coding: utf-8 -*-

# Sample code for the WhatIsMyBrowser.com API - Version 2
#
# User Agent Parse
# This sample code provides a very straightforward example of
# sending an authenticated API request to parse a user agent
# and display some basic results to the console.
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


# An example user agent to parse:
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"


# Where will the request be sent to
api_url = "https://api.whatismybrowser.com/api/v2/user_agent_parse"


# -- Set up HTTP Headers
headers = {
    'X-API-KEY': api_key,
}


# -- prepare data for the API request
# This shows the `parse_options` key with some options you can choose to enable if you want
# https://developers.whatismybrowser.com/api/docs/v2/integration-guide/#user-agent-parse-parse-options
post_data = {
    'user_agent': user_agent,
    "parse_options": {
        #"allow_servers_to_impersonate_devices": True,
        #"return_metadata_for_useragent": True,
        #"dont_sanitize": True,
    },
}


# -- Make the request
result = requests.post(api_url, data=json.dumps(post_data), headers=headers)


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

# -- print the entire json dump for reference
print(json.dumps(result_json, indent=2))


# -- Copy the data to some variables for easier use
parse = result_json.get('parse')
version_check = result_json.get('version_check')

# Now you can do whatever you need to do with the parse result
# Print it to the console, store it in a database, etc
# For example - printing to the console:

if parse.get('simple_software_string'):
    print(parse.get('simple_software_string'))
else:
    print("Couldn't figure out what software they're using")

if parse.get('simple_sub_description_string'):
    print(parse.get('simple_software_string'))

if parse.get('simple_operating_platform_string'):
    print(parse.get('simple_operating_platform_string'))

if version_check:
    # Your API account has access to version checking information

    if version_check.get('is_checkable') is True:
        # This software will have information about whether it's up to date or not
        if version_check.get('is_up_to_date') is True:
            print("%s is up to date" % parse.get('software_name'))
        else:
            print("%s is out of date" % parse.get('software_name'))

            if version_check.get('latest_version'):
                print("The latest version is %s" % ".".join(version_check.get('latest_version')))

            if version_check.get('update_url'):
                print("You can update here: %s" % version_check.get('update_url'))

# Refer to:
# https://developers.whatismybrowser.com/api/docs/v2/integration-guide/#user-agent-parse-field-definitions
# for descriptions of all the fields you can access and what they are used for.
