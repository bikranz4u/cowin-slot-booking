# Description

This script is intended to help for getting a  Covid Vaccination Slot Schedule using registered Mobile OTP. Ensure you have registered on Cowin Portal prior.

Also you have to get information for  pincode and district_id ,which required for search all the Available Vaccination Centre for min_age = 18.

### Pre-Requisite

If you are looking to Use Get Vaccinated Any where in the District , update **requirements_district.json** file as per you distrcit_id, or else you can also search using Pincode **requirements_pincode.json**

Ex `"district_id": 294`   or  `"pincode": "123456"`  along with desired dates.

### How to use

1. Download code to your System
2. Update `requirements_district.json` or `requirements_pincode.json` which ever convinient.
3. Enable the Specific function call on `cowin.py` file. Comment out which you will not use.
   ```
           # session_id_resp = getSlotsCalendarByPin()  # Search using Pincode
           session_id_resp = getSlotsCalendarByDistrict()  # Search Using District
   ```

`python cowin.py -m mobileNumber`

Enter the OTP to proceed.

Note:- Dont try to overload cowin server . If you are trying something , you are trying somehting unethical  you stand responsible.
