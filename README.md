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
* Grant **Edit** rights to the **Service Account** in the Google Spread-sheet

## Configuring the environment

Use virtualenv to configure the working environment:

```shell
]$ virtualenv -p /usr/bin/python3.10 venv
created virtual environment CPython3.10.12.final.0-64 in 1748ms
[..]

]$ source venv/bin/activate
```

Install the library `gspread` with pip3:

```shell
]$ pip3 install gspread
[..]
```

