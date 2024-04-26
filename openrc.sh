#!/bin/bash

export CORDIS_FILENAME="json/project.json"

# Possible keywords = 'cloud', 'Artificial Intelligence', 'Edge computing', 'IoT'
export KEYWORD="cloud"

###########################################################
# G O O G L E ** S P R E A D S H E E T ** S E T T I N G S #
###########################################################
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
