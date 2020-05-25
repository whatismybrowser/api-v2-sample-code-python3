# -*- coding: utf-8 -*-

# Sample code for the WhatIsMyBrowser.com API - Version 2
#
# User Agent Parse Batch
# This sample code provides a very straightforward example of
# sending an authenticated API request to parse a batch of user agents
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

# Some sample user agents to send in a batch
user_agents = {
    "1": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
    "2": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "3": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12",
    "4": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
    "5": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1",
    "6": "Mozilla/5.0 (PlayStation 4 5.55) AppleWebKit/601.2 (KHTML, like Gecko)",
    "7": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "8": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
}


# Where will the request be sent to
api_url = "https://api.whatismybrowser.com/api/v2/user_agent_parse_batch"


# -- Set up HTTP Headers
headers = {
    'X-API-KEY': api_key,
}


# -- prepare data for the API request
# This shows the `parse_options` key with some options you can choose to enable if you want
# https://developers.whatismybrowser.com/api/docs/v2/integration-guide/#user-agent-parse-batch-parse-options
post_data = {
    'user_agents': user_agents,
    "parse_options": {
        #"allow_servers_to_impersonate_devices": True,
        #"return_metadata_for_useragent": True,
        #"dont_sanitize": True,
    },
}

if len(user_agents) > 500:
    print("You are attempting to send more than the maximum number of user agents in one batch")
    exit()

print("Processing %s user agents in one batch. Please be patient." % len(user_agents))

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

# -- Now copy all of the parses to a different variable for easier use
parses = result_json.get("parses")

# -- Display some basic info about each parse result in the list
for parse_id in parses:
    # -- get the whole result from the batch
    parse_record = parses.get(parse_id)

    # This includes the `parse` dict, as well as `result`.
    # At this point - inside the loop - it's basically the same as working with
    # an individual user agent parse (as is done in user_agent_parse.py). There
    # is a `result`, `parse` and possibly a `version_check` and `user_agent_metadata` etc

    # Remember, the JSON will probably not be in the same order as you sent it,
    # so you need to match each key in `parses` (`parse_id`) back to the key you sent through.

    if parse_record.get('result', {}).get('code') != "success":
        print("There was a problem parsing the user agent with the id %s" % (parse_id))
        print(parse_record.get('result', {}).get('message'))
        continue  # to the next record in the batch

    # -- Print the individual parse result for this record
    #print(json.dumps(parse_record, indent=2))

    # -- Now copy the actual parse result to a different variable for easier use
    parse = parse_record.get("parse")

    # You can now access the parse results in the `parse` dict and use them however you would like.
    # For example:

    print("%s: [%s/%s] %s" % (parse_id, parse.get("hardware_type"), parse.get("software_type"), parse.get("simple_software_string"), ))

    # Refer to:
    # https://developers.whatismybrowser.com/api/docs/v2/integration-guide/#user-agent-parse-field-definitions
    # for descriptions of all the fields you can access and what they are used for.
