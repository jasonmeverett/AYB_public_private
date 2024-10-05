import pandas as pd
import cml.models_v1 as models

working_dir = "/home/cdsw/"
# This is a simple representation of what can be a more complex external tool. A larger dataset would utilize a real query engine and can be AI powered to handle Natural Language requests.

# Load a dataset containing recent consumption metrics
CONSUMPTION_DF = pd.read_csv(working_dir + 'sample_external_applications/usage_consumption_query_app/data/usage_metrics/consumption-workload-secs.csv')

#Price per core hour
CORE_HOUR_PRICE = .15

# Search the support cases dataset and return a list in json form
@models.cml_model
def get_consumption_trends(args):
    account = args["product"]

    # Get current week series data of consumption
    current_filtered_df = CONSUMPTION_DF.loc[CONSUMPTION_DF['week'].str.contains("current", na=False, case=False)]
    current_sum_group_df = current_filtered_df.groupby('account_name')['daily_core_hours'].sum()

    # Get previous week series data of consumption
    previous_filtered_df = CONSUMPTION_DF.loc[CONSUMPTION_DF['week'].str.contains("previous", na=False, case=False)]
    previous_sum_group_df = previous_filtered_df.groupby('account_name')['daily_core_hours'].sum()

    # Calculate spend difference between current and previous week
    combined_series = current_sum_group_df.combine(previous_sum_group_df, lambda x, y: (x - y)*CORE_HOUR_PRICE)
    combined_series = combined_series.rename("weekly_consumption_spend_delta")
    print(combined_series)
    return combined_series.to_json(orient="table")


# Run a simple test at startup to make sure things work
testQuery = get_consumption_trends({"product":"Cloudera Machine Learning"})
print(testQuery)