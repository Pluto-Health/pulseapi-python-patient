# pulseapi-python-patient

This python code gives a clear example of how to use the Pluto API to pull all Patients from the API and write their Patient data into a file
So that you can see the API operating and ensure that your own API oAuth credentials work. 

It calls the following Pluto API.
* Call the Patients API
```
/patients
```

* Call the API which retrieves a patient's detailed information
```
/patient/{patient-id}
```

# Configure your environment

Here are some important environment variables you need to configure before run the code.
```
CLIENT_ID = <INSERT YOUR CLIENT ID HERE>
CLIENT_SECRET = <INSERT YOUR CLIENT SECRET HERE>
```
Please replace those two placeholders with your own credentials.

```
LOGS_FILE_PATH = "patient_logs"
DATA_FILE_PATH = "patient_data_files"
```
You can change the folder to where to store the logs and data files of patients.

# Run the code
Python 3.10.6 is used for this repository.\
You can run the code with the following command.
```
python3.10 request.py
```
