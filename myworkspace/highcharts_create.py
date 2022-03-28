import pandas as pd
from pandas_highcharts.core import serialize
from .models import Survey_responses_aggregate

def create_and_define_dataframe(axis_name, **kwargs):
    """Create a dataframe to the chart and set all its properties."""
    # fetch data based on given parameters
    df = pd.DataFrame.from_records(
        Survey_responses_aggregate.objects.filter(**kwargs).values("option_value", "option_count"))
    if not df.empty:
        # Define the coulmn the charrt will be based on and set it to be ordered
        df.set_index("option_value", inplace=True)
        df.sort_index(inplace=True)
        # Define thee title of  the chart X-axis
        df.rename_axis(axis_name, axis="index", inplace=True)
    else:
        df = pd.DataFrame([])
    return df

def generate_highcharts_plot(sid, chart_type):
    """Generate few highcharts based on given parameters:
           sid - the survey identifier
           chart_type - the type of the chart
    """
    #Define list of question ids and titles for each of the  charts to be created
    titles = ["Countries", "Ages", "Gender"]
    questions = [4, 3, 8]
    charts = ""
    for i in range(len(questions)):
        df = create_and_define_dataframe(titles[i], survey_id=sid, question_id=questions[i])
        if not df.empty:
            charts += serialize(df, render_to=f"survey_container{i+1}", title=titles[i], kind=chart_type, legend=None)
        else:
            charts += ""

    return charts
