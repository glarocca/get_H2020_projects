#!/usr/bin/env python3
#
#  Copyright 2024 EGI Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import datetime
import json
import os
import re
import requests
import time

from utils import colourise, get_env_settings
from gspreadutils import init_GWorkSheet
from cordisutils import get_project_URL, get_project_details

__author__    = "Giuseppe LA ROCCA"
__email__     = "giuseppe.larocca@egi.eu"
__version__   = "$Revision: 0.2"
__date__      = "$Date: 25/04/2024 18:23:17"
__copyright__ = "Copyright (c) 2024 EGI Foundation"
__license__   = "Apache Licence v2.0"


def get_GWorkSheet_position(env, worksheet, project_acronym):
    ''' Get the rowID of the specific header (based on the project acronym) '''

    worksheet_dicts = worksheet.get_all_records()
    for worksheet_dict in worksheet_dicts:
        if worksheet_dict['Project Acronym'] <= project_acronym:
              row = row + 1
        else:
            flag = True
            break

    return(row)


def update_GWorkSheet(env, worksheet, index, project, project_coordinator):
    ''' Update the accounting records in the Google Worksheet '''

    # Formatting the header of the worksheet
    worksheet.format("A1:K1", {
      "horizontalAlignment": "LEFT",
      "textFormat": { "fontSize": 10, "bold": True }
    })

    # Formatting the cells of the worksheet
    worksheet.format("A2:K10", {
      "horizontalAlignment": "LEFT",
      "textFormat": { "fontSize": 10, "bold": False }
    })

    print(colourise("green", "[INFO]"), \
            "Adding the [%s]" %project['acronym'] + " H2020 project at row: %s" %index)

    body = [ 
        project['acronym'],
        project['title'],
        project['objective'],
        project['startDate'],
        project['endDate'],
        project['fundingScheme'],
        project['topics'],
        str(project['grantDoi']),
        project_coordinator,
        project['totalCost']
    ]

    worksheet.insert_row(body, index=index, inherit_from_before=False)


def get_projectId(projects, acronym):
    ''' Retrieve the position of the projectId in the python list() '''
   
    index = 0    
    for project in projects:
        if project['acronym'] == acronym:
            break
        else: 
            index = index + 1

    return(index)



def main():

    dt = datetime.datetime.now()
    # Convert dt to string in dd-mm-yyyy HH:MM:SS
    timestamp = dt.strftime("%d-%m-%Y %H:%M:%S")
    _now = dt.strftime("%Y-%m-%d")

    # Initialise the environment settings
    env = get_env_settings()
    verbose = env['LOG']
    print("\nVerbose Level = %s" %colourise("cyan", verbose))

    print(colourise("cyan", "\n[%s]" %env['LOG']), " Variables settings")
    if verbose == "DEBUG":
       print(json.dumps(env, indent=4))

    # Initialise the GWorkSheet
    worksheet = init_GWorkSheet(env)
    
    # Download the full list of the H2020 projcts 
    print(colourise("cyan", "\n[%s]" %env['LOG']), \
               " Parsing H2020 projects from the CORDIS portal in progress")
    print("\t This operation may take few minutes to complete. Please wait!\n")
    
    filename = open(env['CORDIS_FILENAME'])
    projects = json.load(filename)
    
    index = 2
    worksheet_dicts = worksheet.get_all_records()

    for worksheet_dict in worksheet_dicts:
        try:
            for project in projects:
                # 1.) Updated existing projects in the worksheet
                if (worksheet_dict['Project Acronym'] == project['acronym']) and \
                   (worksheet_dict['DOIs']  == project['grantDoi']):
    
                       # Find the proper cell where update the project metadata
                       project_cell = worksheet.find(worksheet_dict['Project Acronym'])

                       if project['grantDoi']:
                          # Get the project's coordinator from the CORDIS portal
                          project_url = get_project_URL(env['CORDIS_PORTAL'], project['grantDoi'])
                          project_coordinator = get_project_details(project_url)

                       # Update cells of the Google Worksheet
                       worksheet.update_cell(project_cell.row, 1, project['acronym'])
                       worksheet.update_cell(project_cell.row, 2, project['title'])
                       worksheet.update_cell(project_cell.row, 3, project['objective'])
                       worksheet.update_cell(project_cell.row, 4, project['startDate'])
                       worksheet.update_cell(project_cell.row, 5, project['endDate'])
                       worksheet.update_cell(project_cell.row, 6, project['fundingScheme'])
                       worksheet.update_cell(project_cell.row, 7, project['topics'])
                       worksheet.update_cell(project_cell.row, 8, str(project['grantDoi']))
                       worksheet.update_cell(project_cell.row, 9, project_coordinator)
                       worksheet.update_cell(project_cell.row, 10, str(project['totalCost']))
                       
                       if env['LOG'] == "DEBUG":
                          print(colourise("green", "[INFO]"), \
                              "Updated the project [%s] at the row: %s" \
                              %(project['acronym'], project_cell.row))

                          # Removing the project from the original list
                          projects.remove(projects[get_projectId(projects, project['acronym'])])

                          # Saving the last index
                          index = project_cell.row

        except:
              print(colourise("red", "[WARNING]"), \
              "Quota exceeded for metric 'Write requests' and 'Write requests per minute per user'")
              time.sleep (60)   

    print(colourise("cyan", "[INFO]"), "Existing projects statistics *UPDATED* in the Google worksheet!")

    try:
       for project in projects:
            if env['KEYWORD'] == "cloud":
               if re.search(r'\bcloud\b', project['objective']) and (project['endDate'] > _now):

                  if project['grantDoi']:
                     # Get the project's coordinator from the CORDIS portal
                     project_url = get_project_URL(env['CORDIS_PORTAL'], project['grantDoi'])
                     project_coordinator = get_project_details(project_url)

                  update_GWorkSheet(env, worksheet, index, project, project_coordinator)
                  index = index + 1
        
            if env['KEYWORD'] == "IoT":
               if re.search(r'\bIoT\b', project['objective']) and (project['endDate'] > _now):

                  if project['grantDoi']:
                     # Get the project's coordinator from the CORDIS portal
                     project_url = get_project_URL(env['CORDIS_PORTAL'], project['grantDoi'])
                     project_coordinator = get_project_details(project_url)
 
                  update_GWorkSheet(env, worksheet, index, project, project_coordinator)
                  index = index + 1

            if env['KEYWORD'] == "Artificial Intelligence":
               if re.search(r'\bArtificial Intelligence\b', project['objective']) and (project['endDate'] > _now):
                  
                  if project['grantDoi']:
                     # Get the project's coordinator from the CORDIS portal
                     project_url = get_project_URL(env['CORDIS_PORTAL'], project['grantDoi'])
                     project_coordinator = get_project_details(project_url)

                  update_GWorkSheet(env, worksheet, index, project, project_coordinator)
                  index = index + 1
        
            if env['KEYWORD'] == "Edge computing":
               if re.search(r'\bEdge computing\b', project['objective']) and (project['endDate'] > _now):
                  update_GWorkSheet(env, worksheet, index, project)
                  index = index + 1

    except:
           print(colourise("red", "[WARNING]"), \
           "Quota exceeded for metric 'Write requests' and 'Write requests per minute per user'")
           time.sleep (60)

    print(colourise("cyan", "[INFO]"), "*NEW* projects statistics *ADDED* in the Google worksheet!")
    
    # Update the timestamp of the last update
    worksheet.insert_note("A1","Last update on: " + timestamp)
    


if __name__ == "__main__":
        main()

