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

import requests
from bs4 import BeautifulSoup

__author__    = "Giuseppe LA ROCCA"
__email__     = "giuseppe.larocca@egi.eu"
__version__   = "$Revision: 0.1"
__date__      = "$Date: 26/04/2024 18:23:17"
__copyright__ = "Copyright (c) 2024 EGI Foundation"
__license__   = "Apache Licence v2.0"


def get_project_URL(cordis_url, doi):
    ''' Get the project's URL from the CORDIS portal starting from the DOI '''

    start = doi.find("/") + 1
    end = len(doi)
    short_doi = doi[start:end]

    url = cordis_url + \
          "/project" + \
          "/id/" + short_doi

    return(url)


def get_project_details(cordis_url):
    ''' Get the project's metadata from the CORDIS portal '''

    rn = requests.get(cordis_url)
    soup = BeautifulSoup(rn.text, "lxml")

    # Find the coordinated class to identify the coordinator of the H2020 proposal
    spans = soup.find_all('p', {'class' : 'coordinated coordinated-name'})
    lines = [span.get_text() for span in spans]
    coordinated_partner = " ".join(lines[0].split())

    # Find the fields of Science
    #spans = soup.find_all('ul', {'class' : 'c-factsheet__list bold-last'})
    #lines = [span.get_text() for span in spans]
    #fields = " ".join(lines[0].split())
    #print(fields)

    return(coordinated_partner)

