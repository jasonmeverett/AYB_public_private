import pandas as pd

#working_dir = "/home/cdsw"
working_dir = "/Users/mecha_alex/work/code/CML_AMP_AYB"

# This is a simple representation of what can be a more complex external tool. A larger dataset would utilize a real query engine and can be AI powered to handle Natural Language requests.

# Load a dataset containing recent support cases
SUPPORT_CASES_DF = pd.read_csv(working_dir + '/sample_external_applications/recent_support_cases_query_app/data/support_cases.csv')

# Search the support cases dataset and return a list in json form
def find_support_cases(account):
    # Process the search name for better results
    case_account = account.replace(" ", "")

    # Search for support cases opened by queried account
    filtered_cases_df = SUPPORT_CASES_DF.loc[SUPPORT_CASES_DF['account_name'].str.contains(case_account, na=False, case=False)]
    return filtered_cases_df.to_json(orient="table")


# Run a simple test at startup to make sure things work
testQuery = find_support_cases("Foo National Bank")
print(testQuery)