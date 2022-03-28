import datetime
import csv
import logging
from .models import Project

def do_upload_projects_from_csv(request):
    """Upload project data from csv into the database.
       The given file should be in legal csv format and include the field names in its first row
    """
    # get the given csv file name parametr from the request
    file_name = request.POST['fname']
    try:
        csv_file = open(file_name)
    except (FileNotFoundError, IOError):
        return "Wrong file or file path."
    with csv_file:
        csvfile = csv.reader(csv_file, delimiter=',')
        # ignore first row and it expect it to include the field names
        header = next(csvfile)
        row_values = []
        try:
            # get all row values and try to insert it to the database
            for row in csvfile:
                obj, created = Project.objects.update_or_create(
                    survey_id = row[0],
                    team = row[1],
                    survey_type = row[2],
                    survey_status = row[3],
                    created_date = datetime.datetime.strptime(row[4].strip(), '%Y-%m-%d %H:%M:%S').date(),
                    project_name = row[5],
                    survey_url = row[6],
                )
        except:
            logging.info(f"User {request.user} had a problem uploading project from CSV file.")
            return "Problem on uploading projects, please check the file format."
        finally:
            csv_file.close()

    return "Success"
