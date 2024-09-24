import json
import os
import glob
import sys

from typing import List 

def get_property(lines: List[str], prop_str: str) -> str:
    id_lines = list(filter(lambda x: x.startswith(f"{prop_str}:"), lines))
    assert len(id_lines) == 1
    account_id = id_lines[0].split(f"{prop_str}:")[1].strip()
    return account_id

def get_formatted_table(account_file: str, out_key: str, header_key: str, no_data_str: str, end_key: str) -> dict:
    """
    TODO: find a way to reconcile "lists within" fields here. In this case, "Products" is a list, but we have no
    heuristic to split up a set of words into products (where is the product split?)
    """

    # Loop until we hit the account team line.
    ii = 0
    while(not account_file[ii].startswith(header_key)):
        ii += 1
    ii += 1

    # Extract header information
    header_row = account_file[ii]
    if no_data_str in header_row:
        return {out_key: []}
    if "Empty DataFrame" in header_row: # TODO: make this scalable
        return {out_key: []}
        
    headers = [x.strip() for x in account_file[ii].split()]
    ii += 1
    indices = [0]
    for h in headers:
        indices.append(header_row.rindex(h) + len(h))

    # Extract account information
    entitlements = []
    while(True):
        # Next section is CDP Public Cloud, so stop before we get there
        if ii == len(account_file) or not account_file[ii] or account_file[ii].startswith(end_key):
            break
        row_str = account_file[ii]
        row_items = []
        for jj, index in enumerate(indices[:-1]):
            row_items.append(row_str[indices[jj]:indices[jj+1]])
        row_items = [x.strip() for x in row_items]
        assert len(row_items) == len(headers)
        row_items = [x if x != "None" else None for x in row_items]
        row_item = {x: y for x, y in zip(headers, row_items)}
        # Parsing original text files, there are occationally null lines. Don't write these out.
        if not all(row for row in row_items):
            ii += 1
            continue 
        entitlements.append(row_item)
        ii += 1

    # Return all of the team members
    return {
        out_key: entitlements
    }

def process_account(account_file: str) -> dict:
    """
    Process information from an account file. 
    """
    with open(account_file, "r") as f:
        account_raw = f.readlines()

    single_line_props = [
        "id",
        "account_type",
        "industry",
        "account_name",
        "description",
        "geo",
        "region",
        "subregion",
        "area"
    ]
    
    out_dict: dict = {
        p: get_property(account_raw, p) for p in single_line_props
    }
    out_dict.update(get_formatted_table(account_file=account_raw, out_key="account_team", header_key="Account team:", no_data_str="N/A", end_key="Entitlements:"))
    out_dict.update(get_formatted_table(account_file=account_raw, out_key="entitlements", header_key="Entitlements:", no_data_str="No entitlement", end_key="Public Cloud CML Workspaces:"))
    out_dict.update(get_formatted_table(account_file=account_raw, out_key="public_cloud_cml_workspaces", header_key="Public Cloud CML Workspaces:", no_data_str="No workspace", end_key="N/A"))

    return out_dict


def process_account_files(account_files):

    accs = []
    for account_file in account_files:
        acc = process_account(account_file)
        # print(json.dumps(acc, indent=2))
        print(acc["account_name"])
        accs.append(acc)

    # # print([a["entitlements"] for a in accs])
    # entitlements = []
    # for a in accs:
    #     es = a["entitlements"]
    #     if len(es) >= 1:
    #         entitlements.extend(es)
    # products = []
    # for e in entitlements:
    #     products.append(e["products"])

    with open("kg_data.json", "w") as fout:
        fout.write(json.dumps(accs, indent=2))



if __name__ == "__main__":
    glob_str = str(os.path.join(os.getenv("HOME"), "accounts", "*"))
    # print(glob_str)
    account_files = glob.glob(glob_str)
    # print(f"num of files: {len(account_files)}")

    process_account_files(account_files)
        
    # idx_test = int(sys.argv[1]) if len(sys.argv) >= 2 else 0
    # print(process_account(account_files[idx_test]))

    # print(json.dumps(process_account(sys.argv[1]), indent=2))
    


