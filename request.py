import requests
import json
import os
import base64
from constants import *


# write log data into a log file
# log_str_arr is an array of log string
def writeLog(log_arr):

    if not os.path.exists(LOGS_FILE_PATH):
        os.makedirs(LOGS_FILE_PATH)
    logs_file = os.path.join(LOGS_FILE_PATH, "patient-api-logs.dat")
    with open(logs_file, "w") as outfile:
        outfile.write('\n'.join(log_arr))


# main function
def main():

    log_str_arr = []

    auth_header = base64.b64encode(
        (CLIENT_ID + ":" + CLIENT_SECRET).encode()).decode()
    payload = {"grant_type": "client_credentials", "client_id": CLIENT_ID}
    headers = {'Authorization': "Basic " + auth_header,
               'Content-Type': 'application/x-www-form-urlencoded'
               }

    response = requests.request(
        "POST", OAUTH_ENDPOINT, headers=headers, data=payload)
    # stop if we fail to get access code
    if response.status_code != 200:
        log_str_arr.append(STR_CRED_INCORRECT)
        writeLog(log_str_arr)
        return

    access_token = response.json()['access_token']

    # Feel free to change the start and length here
    START_INDEX = 1
    PATIENT_LENGTH = 10
    query = {'length': PATIENT_LENGTH, 'start': START_INDEX}
    headers = {"Authorization": "Bearer " + access_token}
    patient_list_endpoint = BASE_URL + "/patients"
    response = requests.get(
        patient_list_endpoint, headers=headers, params=query)

    print("Status Code", response.status_code)

    # Stop in case oAuth credential is incorrect
    if response.status_code == 401:  # Unauthorized
        log_str_arr.append(STR_CRED_INCORRECT)
        writeLog(log_str_arr)
        return

    patient_list = response.json()['content']
    # Stop in case there are no patients in the organization
    if len(patient_list) == 0:
        log_str_arr.append(STR_NO_PATIENTS)
        writeLog(log_str_arr)
        return

        # Otherwise, we are good to move on
    log_str_arr.append(patient_list_endpoint)

    for patient in patient_list:
        patient_id = patient['patient_id']
        patient_detail_endpoint = BASE_URL + "/patient/" + patient_id

        response = requests.get(
            patient_detail_endpoint, headers=headers)

        # Stop in case we meet error calling GetPatientByID
        if response.status_code != 200:
            log_str_arr.append(STR_SERVER_ERROR)
            writeLog(log_str_arr)
            return

        log_str_arr.append(patient_detail_endpoint)

        # Writing to data file
        if not os.path.exists(DATA_FILE_PATH):
            os.makedirs(DATA_FILE_PATH)
        data_file = os.path.join(
            DATA_FILE_PATH, "patient-" + patient_id + ".json")
        with open(data_file, "w+") as outfile:
            outfile.write(json.dumps(response.json()))

        # Writing to log file
    writeLog(log_str_arr)
    print("successfully printed data and log")
    return


if __name__ == "__main__":
    main()
