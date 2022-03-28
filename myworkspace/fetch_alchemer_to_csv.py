import os
import json
from surveygizmo import SurveyGizmo
import pandas as pd
from .constant import constant

def fetch_survey_data_into_csv(output_file, from_date, to_date):
    """Fetch data from Alchemer using REST API and save it as csv file
       output_file - the file path to save data into 
       from_date, to_date - define date range
       the method assumes valid parameters were provided after checked in the page form,
    """
    client = SurveyGizmo(
        api_version='v5'
    )
    client.config.api_token = "a99c37d10b08da6598bfd78934593189f6a6e847de5db36e70"
    client.config.api_token_secret = "A9RT6oZACQ1r2"

    try:
        # fetch the data into a json file
        json_content = (client.api.survey.filter('date_created', '<=', to_date) \
            .filter('date_created', '>', from_date).list()) 
    except:
        return("Problem connecting to Alchemer. Please check the given date values are correct.")

    try:
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
    except:
        return("Problem formating data.")

    try:
        json_file = open(f"{constant.OUTPUT_DIR}/output.json", "w")
    except:
        return("Cannot open a file to write to.")

    try:
        json_file.write(json.dumps(new_json_content))
    except:
        return("Problem writing data to file.")
    finally:
            json_file.close()

    try:
        # convert json into csv format
        csv_file = pd.read_json (f"{constant.OUTPUT_DIR}/output.json")
        csv_file.to_csv (output_file, index = None)
        os.remove(f"{constant.OUTPUT_DIR}/output.json")
    except:
        return("Problem converting data into CSV file")

    return("Success")
