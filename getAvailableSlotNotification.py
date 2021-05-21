import json
import requests
import sys
import os
from twilio.rest import Client

############ URLS #################
baseurl = "https://cdn-api.co-vin.in/api/v2/"
generateOTP = "auth/generateMobileOTP"
confirmOTP = "auth/validateMobileOtp"
getBenificiaries = "appointment/beneficiaries"
schedule = "appointment/schedule"
getCalendarbyPin = "appointment/sessions/public/calendarByPin"
getCalendarbyDistrict = "appointment/sessions/public/calendarByDistrict"


def twilio_notification(message_body):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message_body, from_='whatsapp:+14155238886', to='whatsapp:+919739283896')
    print(message.sid)


def getSlotsCalendarByPin():
    with open("./requirements_pincode.json") as f:
        queryString = json.load(f)
    calendar_headers = {'content-type': 'application/json',
                        'accept': 'application/json', 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36'}
    calendar_response = requests.get(
        baseurl+getCalendarbyPin, headers=calendar_headers, params=queryString)
    # print(type(calendar_response))  ## Remove , for debugging Purpose
    calendar_response_json = calendar_response.json()
    print("")
    # # Remove , used for Debugging
    # print("Debug:---Calendar Response",
    #       json.dumps(calendar_response_json, indent=2))
    for slots in calendar_response_json['centers']:
        for items in slots['sessions']:
            if items['available_capacity'] > 0 and items['min_age_limit'] == 18:
                print(items['min_age_limit'])
                print(items['available_capacity'])
                print(items['session_id'])
                print(items['slots'])
                print("Proceeding for Scheduling..................")
                print("")
                session_id = items['session_id']
                slot = items['slots']
                if slot is None:
                    print("No Results Found for Slots ..It's None")
                    # return session_id, slot[0]
                else:
                    notification_message = "Slots Available for Pincode...Hurry for Booking"
                    twilio_notification(notification_message)
                    return session_id, slot[0]
            else:
                print("NO Slots available for 18 - 44 yrs Range...Try Later")
                sys.exit()


def getSlotsCalendarByDistrict():
    with open("./requirements_district.json") as f:
        queryString = json.load(f)
    calendar_headers = {'content-type': 'application/json',
                        'accept': 'application/json', 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36'}
    calendar_response = requests.get(
        baseurl+getCalendarbyDistrict, headers=calendar_headers, params=queryString)
    # print(type(calendar_response))    ## Remove , For Debugging Purpose
    calendar_response_json = calendar_response.json()
    print("")
    # # Remove , used for Debugging
    # print("Debug:---Calendar Response",
    #       json.dumps(calendar_response_json, indent=2))
    for slots in calendar_response_json['centers']:
        for items in slots['sessions']:
            if items['available_capacity'] == 0 and items['min_age_limit'] == 18:
                print(items['min_age_limit'])
                print(items['available_capacity'])
                print(items['session_id'])
                print(items['slots'])
                print("Proceeding for Scheduling..................")
                print("")
                session_id = items['session_id']
                slot = items['slots']
                if slot is None:
                    print("No Results Found for Slots ..It's None")
                    # return session_id, slot[0]
                else:
                    notification_message = "Slots Available for District...Hurry for Booking"
                    twilio_notification(notification_message)
                    return session_id, slot[0]
            else:
                print("NO Slots available for 18 - 44 yrs Range...Try Later")
                sys.exit()


# print("Trying getSlotsCalendarByDistrict.... ")
# dsession_id_resp, dslot = getSlotsCalendarByDistrict()
# print(dsession_id_resp)
# print(dslot)


print("Trying getSlotsCalendarByPin.... ")
psession_id_resp, pslot = getSlotsCalendarByPin()
print(psession_id_resp)
print(pslot)


# * * * * * /Users/bikrdas/Desktop/coWin/venv/bin/python /Users/bikrdas/Desktop/coWin/getAvailableSlotNotification.py > demo.log
