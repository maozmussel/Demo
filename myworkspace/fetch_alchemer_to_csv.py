import os
import logging
import json
import requests
from surveygizmo import SurveyGizmo
import pandas as pd
import environ
from .constant import constant
from django.conf import settings

def fetch_survey_data_into_csv(output_file, from_date, to_date):
    """Fetch data from Alchemer using REST API and save it as csv file
       output_file - the file path to save data into 
       from_date, to_date - define date range
       the method assumes valid parameters were provided after checked in the page form,
    """
    client = SurveyGizmo(
        api_version='v5'
    )
    # reading .env file for getting system variables
    env = environ.Env()
    environ.Env.read_env(os.path.join(settings.BASE_DIR, '.env'))
    client.config.api_token = env("API_KEY")
    client.config.api_token_secret = env("API_SECRET_KEY")

    try:
        # fetch the data into a json file
        json_content = (client.api.survey.filter('date_created', '<=', to_date) \
            .filter('date_created', '>', from_date).list()) 
    except requests.exceptions.HTTPError as err:
        # error accessing Alchemer
        logging.error(err)
        raise

    # get only the 'data' key from the content
    json_content = json_content["data"]
    new_json_content=[]
    for item_row in json_content:
        # now item_row is a dictionary
        for attribute, value in item_row.items():
            if (attribute == "id"):
                # this is the id, initiate next item
                item = {"id": value}
            elif (attribute == "modified_on"):
                # ignore this key 
                continue
            elif (attribute == "statistics"):
                # ignore this key 
                continue
            elif (attribute == "links"):
                # out of the links key, only the 'publish' key is relevant 
                item['survey_link'] = value['publish']
            else:
                item[attribute] = value
        new_json_content.append(item)

    try:
        json_file = open(f"{constant.OUTPUT_DIR}/output.json", "w")
    except FileNotFoundError as err:
        logging.error(err)
        raise

    try:
        json_file.write(json.dumps(new_json_content))
    except PermissionError as err:
        logging.error(err)
        raise
    finally:
        json_file.close()

    try:
        # convert json into csv format
        csv_file = pd.read_json (f"{constant.OUTPUT_DIR}/output.json")
        csv_file.to_csv (output_file, index = None)
        os.remove(f"{constant.OUTPUT_DIR}/output.json")
    except ValueError as err:
        logging.error(err)
        raise
    except OSError as err:
        logging.error(err)
        raise

    return True
