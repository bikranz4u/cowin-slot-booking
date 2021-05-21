#! /usr/bin/env python

"""
Book Covid vaccination slot
Refs: https://documenter.getpostman.com/view/9564387/TzRPip7u#e35cdc70-42ac-474f-aad2-0172646527dd,
      https://apisetu.gov.in/public/marketplace/api/cowin/cowin-protected-v2#/
"""

__author__ = "Bikram Das"
__license__ = "MIT"

import requests
import json
import hashlib
import argparse
import time
import sys
from datetime import date, datetime, timedelta
from multiprocessing import Process
from requests.sessions import session

######### Timer for OTP #########
# define the countdown func.

####################### List Of URLs #####################
baseurl = "https://cdn-api.co-vin.in/api/v2/"
generateOTP = "auth/generateMobileOTP"
confirmOTP = "auth/validateMobileOtp"
getBenificiaries = "appointment/beneficiaries"
schedule = "appointment/schedule"
getCalendarbyPin = "appointment/sessions/public/calendarByPin"
getCalendarbyDistrict = "appointment/sessions/public/calendarByDistrict"
#########################################################

# Create the parser
parser = argparse.ArgumentParser(description='PROVIDE YOUR  MOBILE NUMBER')

# Add the arguments
parser.add_argument('-m', '--mobile', metavar='', type=str,
                    required=True, help='[Mandatory] Input your mobile number !!!')
args = parser.parse_args()

# Data Section for Generate OTP
json_obj = {
    'mobile': args.mobile,
    'secret': 'U2FsdGVkX1/l2tBuii9aPf1lzYS767R+EoXWUIO/j8gWS0M7gYWvqGX6GoqFgG084eRbGUKj8eUJ3ovR3/OA9w=='
}

#secret: "U2FsdGVkX1+MToL2D7o4DiuqYBdQC+9/cXjXZB3pM9xwr2M4o5DLIU7fZMN//ZHLsyRip9lsS8nx6mWzi02G7A=="
###################################  Generate OTP  ####################################

opt_headers = {'content-type': 'application/json',
               'accept': 'application/json', 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36'}

otp_response = requests.post(
    baseurl+generateOTP, json.dumps(json_obj), headers=opt_headers)


txnID = otp_response.json()

txnId = txnID['txnId']
# print("Your TransactionID:- ", txnId)
# print("")
print("")
print("OTP is sent to your mobile number .. Please enter that to proceed further !!!")
print("")


otp_received = (
    input("Enter Your OTP , received on mobile , within 45 Secs:- "))
#### Enter OTP #####
# otp_received = ''
# counter = 0
# while counter < 3:
#     if otp_received == '':
#         otp_received = (
#             input("Enter Your OTP , received on mobile , within 45 Secs:- "))
#     counter = counter+1

# print(" 3 Wrong OTPs ..aborting")
# sys.exit()
print("")
print("")
# ###Timer call for OTP input
# countdown(int(5))

# Convert the OTP into sha256

hash_object = hashlib.sha256(otp_received.encode())
otp_hash = hash_object.hexdigest()

# print(type(otp_hash))    # Remove , used for Debugging

# print("")
# print("sha256 value for OTP :-"+otp_hash)  # Remove , used for Debugging
# print("")

######################################  Confirm the OTP ######################################
opt_response_header = {'content-type': 'application/json',
                       'accept': 'application/json',
                       'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36'}

json_otp_confirmation = {
    "otp": otp_hash,
    "txnId": txnId
}
print("********************* OTP Confirmation Payload ***********************")
print(json_otp_confirmation)
print("*********************************************************************")

otp_confirm_response = requests.post(
    baseurl+confirmOTP, json.dumps(json_otp_confirmation), headers=opt_response_header, cookies=otp_response.cookies)

if otp_confirm_response.status_code == requests.codes.ok:
    confirm_response = otp_confirm_response.json()
    # print("")
    # print("Debug:---OTP Response", confirm_response)  # # Remove , used for Debugging
    # print("")
    token = confirm_response['token']
    isNewAccount = confirm_response['isNewAccount']
    if isNewAccount == 'Y':
        print("")
        # print("It's a New Account")
        # print("Your Token Is :", token)
        print("")
    else:
        print("")
        # print("It's an Old account")
        # print("Your Token Is :", token)
        # print("")
        # print("Your Account Is :", isNewAccount)
        print("")
else:
    otp_confirm_response.raise_for_status()

################# Get Details for Available Slot  By Calendar PIN and Calendar District #####################


def getSlotsCalendarByPin():
    with open("./requirements_pincode.json") as f:
        queryString = json.load(f)
    calendar_headers = {'content-type': 'application/json',
                        'accept': 'application/json', 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36'}
    calendar_response = requests.get(
        baseurl+getCalendarbyPin, headers=calendar_headers, params=queryString)
    # print(type(calendar_response))
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
                print("Proceeding for Scheduling..................")
                print("")
                session_id = items['session_id']
                slot = items['slots']
                if slot is None:
                    print("")
                    print("No Results Found for Slots ..It's None")
                    # return session_id, slot[0]
                else:
                    return session_id, slot[0]
            else:
                print("")
                print("NO Slots available for 18 - 44 yrs Range...Try Later")
                sys.exit()


def getSlotsCalendarByDistrict():
    with open("./requirements_district.json") as f:
        queryString = json.load(f)
    calendar_headers = {'content-type': 'application/json',
                        'accept': 'application/json', 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36'}
    calendar_response = requests.get(
        baseurl+getCalendarbyDistrict, headers=calendar_headers, params=queryString)
    print(type(calendar_response))
    calendar_response_json = calendar_response.json()
    print("")
    # # Remove , used for Debugging
    print("Debug:---Calendar Response",
          json.dumps(calendar_response_json, indent=2))
    for slots in calendar_response_json['centers']:
        for items in slots['sessions']:
            if items['available_capacity'] > 0 and items['min_age_limit'] == 18:
                # print(items['min_age_limit'])
                # print(items['available_capacity'])
                # print(items['session_id'])
                print("Proceeding for Scheduling..................")
                print("")
                session_id = items['session_id']
                slot = items['slots']
                if slot is None:
                    print("No Results Found for Slots ..It's None")
                    print("")
                    # return session_id, slot[0]
                else:
                    return session_id, slot[0]
            else:
                print("")
                print("NO Slots available for 18 - 44 yrs Range...Try Later")
                sys.exit()


# ############################################# Get Benificiaries #############################################
# --header 'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36'
# --header 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'


print("")
print("----------------- Pulling Benificiaries Details ---------------")
print("")
benificiaries_headers = {'authorization': 'Bearer '+token,
                         'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36'}
print(json.dumps(benificiaries_headers, indent=2))
print("")
benificiaries_response = requests.get(
    baseurl+getBenificiaries, headers=benificiaries_headers)
# print(type(benificiaries_response))   # Remove , used for Debugging
# print(benificiaries_response)         # Remove , used for Debugging
benificiaries_response_json = benificiaries_response.json()
print('*'*80)
print("")
# Remove , used for Debugging
print(json.dumps(benificiaries_response_json, indent=2))
print("")
print('*'*80)

for beneficiaries_details in benificiaries_response_json['beneficiaries']:
    if beneficiaries_details['vaccination_status'] == "Not Vaccinated":
        print("Below users are yet to vaccinate....")
        print("************************************")
        print("")
        print(beneficiaries_details['name']+' : ' +
              beneficiaries_details['beneficiary_reference_id'])
        reference_id = beneficiaries_details['beneficiary_reference_id']
        beneficiaries_arr = reference_id.split()
        # print(type(beneficiaries_arr))  # Remove, for debugging only
        print("Seaching for Slots ..Finger Crossed: ")
        session_id_resp, slot = getSlotsCalendarByPin()  # Search using Pincode
        # session_id_resp,slot = getSlotsCalendarByDistrict()  # Search Using District
        schedule_Payload = {"dose": 1, 'session_id': session_id_resp,
                            'beneficiaries': beneficiaries_arr, 'slot': slot}
        print(schedule_Payload)  # Remove, for debugging only
        scheduling_headers = {'authorization': 'Bearer '+token,
                              'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36'}
        schedule_response = requests.post(
            baseurl+schedule, data=json.loads(schedule_Payload), headers=scheduling_headers)
        schedule_response_json = schedule_response.json()
        print(schedule_response)
        # session_id_resp = getSlotsCalendarByDistrict()
        print("")

    elif beneficiaries_details['dose1_date'] == 'Partially Vaccinated' and beneficiaries_details['dose2_date'] == '':
        print("Below users are got One Shot , waiting for 2nd Dose....")
        print("************************************")
        print("")
        print(beneficiaries_details['name']+' : '+beneficiaries_details['beneficiary_reference_id'] + ' : ' +
              " Dose1_Date: "+beneficiaries_details['dose1_date'])
        reference_id = beneficiaries_details['beneficiary_reference_id']
        beneficiaries_arr = reference_id.split()
        Begindatestring = beneficiaries_details['dose1_date']
        Begindate = datetime.strptime(Begindatestring, "%d-%m-%Y")
        # calculating end date by adding 28 days
        reminder_date = Begindate + timedelta(days=28)
        today = date.today()
        if today > reminder_date:
            print("Seaching for Slots :- ")
            session_id_resp, slot = getSlotsCalendarByPin()  # Check Using Local PINCODE
            # session_id_resp,slot = getSlotsCalendarByDistrict()  # Search Using District
            schedule_Payload = {"dose": 2, 'session_id': session_id_resp,
                                'beneficiaries': reference_id, 'slot': slot}
            print(schedule_Payload)  # Remove, for debugging only
            scheduling_headers = {'authorization': 'Bearer '+token,
                                  'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36'}
            schedule_response = requests.post(
                baseurl+schedule, json.dumps(schedule_Payload), headers=scheduling_headers)
            schedule_response_json = schedule_response.json()
            print(schedule_response)
        else:
            print("Dose 2 Shot can be Tried after 40th day from ", beneficiaries_details['dose1_date'] + ", i;e ",
                  reminder_date.date())

    else:
        print("Below users Completed Vaccination....")
        print("************************************")
        print("")
        print(beneficiaries_details['name']+' : ' +
              beneficiaries_details['beneficiary_reference_id'])
        # Begindatestring = beneficiaries_details['dose2_date']
        # Begindate = datetime.strptime(Begindatestring, "%d-%m-%Y")
        # # calculating end date by adding 20 days
        # reminder_date = Begindate + timedelta(days=20)
        print("")
        print("You have vaccinated ,be at home till  ", reminder_date.date())
        print("************************************")
