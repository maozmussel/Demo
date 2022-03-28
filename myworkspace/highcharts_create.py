import pandas as pd
from pandas_highcharts.core import serialize
from .models import Survey_responses_aggregate

def create_and_define_dataframe(axis_name, **kwargs):
    #fetch data into data model and set all relevant parameters
    df = pd.DataFrame.from_records(
        Survey_responses_aggregate.objects.filter(**kwargs).values("option_value", "option_count"))
        #Survey_responses_aggregate.objects.filter(survey_id=surveyid, question_id=4).values("option_value", "option_count"))
    if not df.empty:
        df.set_index("option_value", inplace=True)
        df.sort_index(inplace=True)
        df.rename_axis(axis_name, axis="index", inplace=True)
    else:
        df = pd.DataFrame([])
    return df

def generate_highcharts_plot():
    surveyid = "4144303"
    chart_type = "pie"
    titles = ["Countries"]
    questions = [4]
    charts = []
    for i in range(len(questions)):
        df = create_and_define_dataframe(titles[i], survey_id=surveyid, question_id=questions[i])
        if not df.empty:
            charts.append(serialize(df, render_to="survey_container", title=titles[i], kind=chart_type, legend=None))
            print(charts[i])
        else:
            charts.append("")
    return charts
