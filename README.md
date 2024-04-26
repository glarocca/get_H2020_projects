# get_H2020_projects
This repository contains python client to extract statistics about the list of running H2020 projects from the CORDIS portal.

## Creating a Google Service Account

In order to read from and write data to Google Sheets in Python,
we will have to create a **Google Service Account**.

**Instructions** to create a Google Service Account are the following:

* Head over to [Google developer console](https://console.cloud.google.com/)
* Click on **Create Project** to create a new project
* Fill in the required fields and click on **Create**
* From the APIs & Services menu, click on **Enable API and Services**
* Search for "Google Drive API" and click on **Enable**
* Search for the "Google Sheets API" and click on **Enable**
* From the APIs & Services menu, click on **Credentials**
* From the "Credentials" menu, click on **Create Credentials** to create a new credentials account
* From the Credentials account, select **Service Account**
* Fill in the web form providing the name of the Service account name and click on "Create" and Continue
* Skip the step 3 to grant users access to this service account
* Click on **Done**
* Once the Service Account has been created, click on **Keys** and click on "Add new Keys" and select JSON
* The credentials will be created and downloaded as a JSON file
* Copy the JSON file to your code directory and rename it to `credentials.json`
* Ask the [Owner](mailto:giuseppe.larocca@egi.eu) to grant **Edit** rights to the **Service Account** in the [Google Spread-sheet](https://docs.google.com/spreadsheets/d/18jLSH_IYCmrDOPyaEZqXz1DUfDLLU0v7COS7p6-jv_Y/edit)

## Pre-requisites

* `Python 3.10.12+` installed on your local computer
* Install pip3: `apt-get install -y python3-pip`
* Install gspread API: `sudo pip3 install gspread`

## Download all Horizon Europe projects

* From the [CORDIS portal](https://cordis.europa.eu/projects)
* Click on `Download all Horizon Europe projects`
* Unzip the file `cordis-HORIZONprojects-json.zip` in the current working director

## Install the credentials of the Google Service Account

Install the JSON file downloaded when you created a Google Service Account and rename it as `service_account.json`

```bash
]$ mkdir $PWD/.config
]$ cat .config/service_account.json
{
  "type": "service_account",
  "project_id": "striped-rhino-395008",
  "private_key_id": "<ADD_PRIVATE_KEY_ID> HERE",
  "private_key": "<ADD PRIVATE_KEY> HERE",
  "client_email": "python-google-sheet-service-ac@striped-rhino-395008.iam.gserviceaccount.com",
  "client_id": "<ADD CLIENT_ID> HERE",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/python-google-sheet-service-ac%40striped-rhino-395008.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
```
## Generate statistics from the CORDIS portal

This python client generates statistics about the list of running EC-funded projects registered in the [CORDIS Portal](https://cordis.europa.eu/)

Edit the `openrc.sh`, and configure the `KEYWORD` to be used for the investigation.

```bash
export CORDIS_FILENAME="json/project.json"

# Possible keywords = 'cloud', 'Artificial Intelligence', 'Edge computing', 'IoT'
export KEYWORD="cloud"

export SERVICE_ACCOUNT_PATH=${PWD}"/.config/"
export SERVICE_ACCOUNT_FILE=${SERVICE_ACCOUNT_PATH}"service_account.json"
export GOOGLE_SHEET_NAME="CORDIS H2020 projects"
export GOOGLE_CLOUD_WORKSHEET="Cloud projects"
export GOOGLE_AI_WORKSHEET="AI projects"
export GOOGLE_EDGE_WORKSHEET="Edge projects"
export GOOGLE_IoT_WORKSHEET="IoT projects"

# LOG=INFO, no verbose logging is 'OFF'
# LOG=DEBUG, verbose logging is 'ON'
#export LOG="INFO"
export LOG="DEBUG"
```

Source the environment settings and run the client

```bash
]$ clear && source openrc.sh && python3 get_H2020_projects.py

Verbose Level = DEBUG

[DEBUG]  Variables settings
{
    "CORDIS_FILENAME": "json/project.json",
    "KEYWORD": "cloud",
    "SERVICE_ACCOUNT_PATH": "/home/larocca/modules/APIs/CORDIS/.config/",
    "SERVICE_ACCOUNT_FILE": "/home/larocca/modules/APIs/CORDIS/.config/service_account.json",
    "GOOGLE_SHEET_NAME": "CORDIS H2020 projects",
    "GOOGLE_CLOUD_WORKSHEET": "Cloud projects",
    "GOOGLE_AI_WORKSHEET": "AI projects",
    "GOOGLE_EDGE_WORKSHEET": "Edge projects",
    "GOOGLE_IoT_WORKSHEET": "IoT projects",
    "LOG": "DEBUG"
}

[DEBUG]  Parsing H2020 projects from the CORDIS portal in progress
	 This operation may take few minutes to complete. Please wait!

[INFO] Updated the project [AC3] at the row: 2
[INFO] Updated the project [RISER] at the row: 3
[INFO] Updated the project [DETERMINISTIC6G] at the row: 4
[INFO] Updated the project [6G-XR] at the row: 5
[INFO] Updated the project [ORBIT-D] at the row: 6
[INFO] Updated the project [POLIIICE] at the row: 7
[INFO] Updated the project [XR5.0] at the row: 8
[..]
[INFO] Existing projects statistics updated in the Google worksheet!
[INFO] Adding the [CREDIT Vibes] H2020 project at row: 238
[INFO] Adding the [PQ-REACT] H2020 project at row: 239
[INFO] Adding the [iBEMS-SeLiBat] H2020 project at row: 240
[INFO] Adding the [finapp cosmic ray neutron sensing] H2020 project at row: 241
[INFO] Adding the [EINSTEIN] H2020 project at row: 242
[INFO] Adding the [SUPREME] H2020 project at row: 243
[INFO] Adding the [CONNECT] H2020 project at row: 244
[INFO] Adding the [ANIMATE] H2020 project at row: 245
[INFO] Adding the [CODE] H2020 project at row: 246
[INFO] Adding the [QOMUNE] H2020 project at row: 247
[INFO] Adding the [HAVEN] H2020 project at row: 248
[INFO] Adding the [AURORA] H2020 project at row: 249
[INFO] Adding the [CLEVER] H2020 project at row: 250
```

The statistics are updated in the Google worksheet [CORDIS H2020 project](https://docs.google.com/spreadsheets/d/18jLSH_IYCmrDOPyaEZqXz1DUfDLLU0v7COS7p6-jv_Y/edit) (in the `Cloud projects` tab)


## References
* [gspread APIs documentation](https://docs.gspread.org/en/v5.10.0/)
* [How to connect Python to GoogleSheets](https://blog.coupler.io/python-to-google-sheets/)
* [Google Developer Console](https://console.cloud.google.com/apis/dashboard)
