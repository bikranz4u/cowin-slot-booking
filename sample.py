import json
from datetime import datetime
from datetime import timedelta

with open("/Users/bikrdas/Desktop/coWin/out.json") as f:
    benificiaries_response_json = json.load(f)
    print(json.dumps(benificiaries_response_json, indent=2))
    for beneficiaries_details in benificiaries_response_json['beneficiaries']:
        if beneficiaries_details['vaccination_status'] == "Not Vaccinated":
            # beneficiaries_arr = []
            print("Below users are yet to vaccinate....")
            print("************************************")
            print(beneficiaries_details['beneficiary_reference_id'] +
                  ' : ' + beneficiaries_details['name'])
            reference_id = beneficiaries_details['beneficiary_reference_id']
            beneficiaries_arr = reference_id.split()
            print(type(beneficiaries_arr))
            print(beneficiaries_arr)
            print("Seaching for Slots:- ")
            print("")
        elif beneficiaries_details['dose1_date'] != '' and beneficiaries_details['dose2_date'] == '':
            print("Below users are got One Shot , waiting for 2nd Dose....")
            print("************************************")
            print("")
            print(beneficiaries_details['name']+' : '+beneficiaries_details['beneficiary_reference_id'] + ' : ' +
                  " Dose1_Date "+beneficiaries_details['dose1_date'])
            reference_id = beneficiaries_details['beneficiary_reference_id']
            Begindatestring = beneficiaries_details['dose1_date']
            Begindate = datetime.strptime(Begindatestring, "%d-%m-%Y")
            # calculating end date by adding 28 days
            reminder_date = Begindate + timedelta(days=28)
            print("Dose 2 Shot can be Tried after 28th day from ", beneficiaries_details['dose1_date'] + ", i;e ",
                  reminder_date.date())
        else:
            print("Below users Completed Vaccination....")
            print("************************************")
            print("")
            print(beneficiaries_details['name']+' : ' +
                  beneficiaries_details['beneficiary_reference_id'])
            reference_id = beneficiaries_details['beneficiary_reference_id']
            Begindatestring = beneficiaries_details['dose2_date']
            Begindate = datetime.strptime(Begindatestring, "%d-%m-%Y")
            # calculating end date by adding 20 days
            reminder_date = Begindate + timedelta(days=20)
            print("")
            print("You have vaccinated ,be at home till  ", reminder_date.date())
            print("************************************")
