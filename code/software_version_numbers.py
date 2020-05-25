# -*- coding: utf-8 -*-

# Sample code for the WhatIsMyBrowser.com API - Version 2
#
# Software Version Numbers
# This sample code provides an example of querying the API
# to get all the latest version numbers for software (ie. Browsers)
# operating systems and plugins.
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

# Where will the request be sent to
api_url = "https://api.whatismybrowser.com/api/v2/software_version_numbers/all"

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

# -- Copy the `version_data` data to a variable for easier use
version_data = result_json.get('version_data')

# -- Loop over all the different software version data elements
for software_key in version_data:

    print("Version data for %s" % software_key)

    software_version_data = version_data.get(software_key)

    for stream_code_key in software_version_data:

        #print(json.dumps(software_version_data.get(stream_code_key), indent=2))

        print("  Stream: %s" % stream_code_key)

        print("\tThe latest version number for %s [%s] is %s" % (software_key, stream_code_key, ".".join(software_version_data.get(stream_code_key).get("latest_version"))))

        if software_version_data.get(stream_code_key).get("update"):
            print("\tUpdate no: %s" % software_version_data.get(stream_code_key).get("update"))

        if software_version_data.get(stream_code_key).get("update_url"):
            print("\tUpdate URL: %s" % software_version_data.get(stream_code_key).get("update_url"))

        if software_version_data.get(stream_code_key).get("download_url"):
            print("\tDownload URL: %s" % software_version_data.get(stream_code_key).get("download_url"))

        if software_version_data.get(stream_code_key).get("release_date"):
            print("\tIt was released: %s" % software_version_data.get(stream_code_key).get("release_date"))

        print("  Some sample user agents with the latest version numbers:")

        # if there are sample user agents (eg. Flash and Java can't have sample user agents..), display them
        if software_version_data.get(stream_code_key).get("sample_user_agents") is not None:
            for sample_user_agent_group in software_version_data.get(stream_code_key).get("sample_user_agents"):
                print("\tUser agents for %s on %s [%s]" % (sample_user_agent_group, software_key, stream_code_key))
                for sample_user_agent in software_version_data.get(stream_code_key).get("sample_user_agents").get(sample_user_agent_group):
                    print("\t\t%s" % sample_user_agent)

    print("-------------------------------")
