import pandas as pd
import math
import numpy as np
import customtkinter as ctk
from icecream import ic
from collections import Counter


def contains_pc(cell):
    return 'PC' in str(cell)


def contains_ml(cell):
    return 'ML' in str(cell)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 1223)
df = pd.read_excel("data/DetailedAudit_ORIG.xls")
df.drop(columns=['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 6', 'Unnamed: 7'], inplace=True)
df.drop([0, 1, 2, 3, 4, 5, 6], axis=0, inplace=True)
df = df.reset_index(drop=True)
column_names = ["Transaction_ID", "Transaction_Date", "Terminal_ID", "Receipt_Number",
                "Clerk", "Sales_Total", "Tax", "Sales_Ex_Tax"]
df.columns = column_names

replacements = {'\n': "", "/": "", ":": "", "  ": "_", " ": "_"}

# Apply replacements
for old, new in replacements.items():
    df = df.replace(old, new, regex=True)


file_path = 'data/output_data.xlsx'
df.to_excel(file_path, index=False)

times = df
ic(df)

for col in df.columns:
    df[col] = df[col].ffill()

all_trans_id = list(round(df["Transaction_ID"].dropna()))
unique_id = list(df["Transaction_ID"].dropna().unique())

unique_drinks = []
unique_sauces = []

for v in df["Transaction_Date"]:
    if "ML" in str(v):
        unique_drinks.append(v)

for v in df["Transaction_Date"]:
    if "PC" in str(v):
        unique_sauces.append(v)

unique_drinks = list(set(unique_drinks))
unique_sauces = list(set(unique_sauces))

for i, v in enumerate(unique_id):
    unique_id[i] = int(v)

for i, v in enumerate(all_trans_id):
    all_trans_id[i] = int(v)

trans_date = list(df["Transaction_Date"])
clerk = list(df["Clerk"])

assoc = df[(df["Transaction_ID"] == 12382776.0) & (df["Clerk"] == "RENSCHE")][["Transaction_Date", "Clerk"]]

assoc2 = df[df["Transaction_ID"] == 12382776.0][["Transaction_ID", "Transaction_Date", "Clerk"]]

mask_pc = df.map(contains_pc)
mask_ml = df.map(contains_ml)

pc = df[mask_pc]
ml = df[mask_ml]

add_ml_day = list(ml["Transaction_Date"].dropna().drop_duplicates())
add_pc_day = list(pc["Transaction_Date"].dropna().drop_duplicates())

add_pc_dict = {}
add_ml_dict = {}
clerk_add_dict = {}

# EMPLOYEE LIST
employees_cnt = []
for v in df["Clerk"]:
    if isinstance(v, str) and v != "Sales Inc":
        employees_cnt.append(v)

employees_tot_sales = Counter(employees_cnt)
employees_tot_sales = dict(employees_tot_sales)

employees = list(set(employees_cnt))
ic(employees)

# CREATE A DICTIONARY LINKING ALL TRANS IDS TO A CLERK
for i, v in df.iterrows():
    # Ensure 'Clerk' column value is a string before checking for substring membership
    if isinstance(v['Clerk'], (float, int)):
        pass
    else:
        for emp in employees:
            if emp in v['Clerk']:
                key = v['Transaction_ID']
                if isinstance(key, float) and math.isnan(key):
                    continue
                if key != "NaN":
                    key = round(key)
                    value = v['Clerk']
                    clerk_add_dict[key] = value

ic(clerk_add_dict)

# CREATE DICT OF ALL OCCURANCES OF SAUCES SOLD PER TRANS ID
for i, v in df.iterrows():
    for pc in add_pc_day:
        if pc in str(v['Transaction_Date']):
            key = v['Transaction_ID']
            value = v['Transaction_Date']

            # Check if key already exists in add_ml_dict
            if key in add_pc_dict:
                # Ensure the value is stored as a list
                if not isinstance(add_pc_dict[key], list):
                    add_pc_dict[key] = [add_pc_dict[key]]
                # Append the new value
                add_pc_dict[key].append(value)
            else:
                # If key doesn't exist, initialize with a list containing the value
                add_pc_dict[key] = [value]

# CREATE DICT OF ALL OCCURANCES OF DRINKS SOLD PER TRANS ID
for i, v in df.iterrows():
    for ml in add_ml_day:
        if ml in str(v['Transaction_Date']):
            key = v['Transaction_ID']
            value = v['Transaction_Date']

            # Check if key already exists in add_ml_dict
            if key in add_ml_dict:
                # Ensure the value is stored as a list
                if not isinstance(add_ml_dict[key], list):
                    add_ml_dict[key] = [add_ml_dict[key]]
                # Append the new value
                add_ml_dict[key].append(value)
            else:
                # If key doesn't exist, initialize with a list containing the value
                add_ml_dict[key] = [value]

# COUNT DRINKS SOLD PER CLERK PER TRANS ID
drink_cnt = {}

for i in unique_drinks:
    for k, v in add_ml_dict.items():
        if isinstance(k, float) and math.isnan(k):
            continue
        if k != "NaN":
            k = round(k)
            k = str(k)
            if i in v:
                drink_cnt[k + "_" + i] = len(v)

final_drink_cnt = {}

for k, v in drink_cnt.items():
    drink = k[9:]  # Extract the drink part from the key
    date_part = k[0:8]  # Extract the date part from the key

    for t_id, clerk in clerk_add_dict.items():
        if date_part in str(t_id):
            if t_id not in final_drink_cnt:
                final_drink_cnt[t_id] = {}
            if clerk not in final_drink_cnt[t_id]:
                final_drink_cnt[t_id][clerk] = {}
            final_drink_cnt[t_id][clerk][drink] = v

# COUNT SAUCES SOLD PER CLERK PER TRANS ID
sauce_cnt = {}

for i in unique_sauces:
    for k, v in add_pc_dict.items():
        k = round(k)
        k = str(k)
        if i in v:
            sauce_cnt[k + "_" + i] = len(v)

final_sauce_cnt = {}

for k, v in sauce_cnt.items():
    sauce = k[9:]  # Extract the drink part from the key
    date_part = k[0:8]  # Extract the date part from the key

    for t_id, clerk in clerk_add_dict.items():
        if date_part in str(t_id):
            if t_id not in final_sauce_cnt:
                final_sauce_cnt[t_id] = {}
            if clerk not in final_sauce_cnt[t_id]:
                final_sauce_cnt[t_id][clerk] = {}
            final_sauce_cnt[t_id][clerk][sauce] = v

times['Transaction_Date'] = times['Transaction_Date'].str[9:-2]

times_dict = {}

for i, row in times.iterrows():
    transaction_id = row["Transaction_ID"]
    # transaction_id = round(transaction_id)
    transaction_date = row["Transaction_Date"]

    # Check if transaction_date can be converted to an integer
    try:
        transaction_date = int(transaction_date)
    except ValueError:
        continue  # Skip this row if transaction_date is not numeric

    # Check if transaction_date falls within the specified range
    if 1129 < transaction_date < 1401:
        times_dict[transaction_id] = transaction_date

count_sales_time = []
count_sales_time_total = []

ic(times_dict)

for i, v in times_dict.items():
    for id, clerk in clerk_add_dict.items():
        ic(id)
        if id == i:
            v = str(v)
            ic(v)
            count_sales_time.append(clerk)
            count_sales_time_total = Counter(count_sales_time)
            count_sales_time_total = dict(count_sales_time_total)

# How many transactions per Clerk per day


ic(final_drink_cnt)
ic(final_sauce_cnt)
ic(employees_tot_sales)
ic(count_sales_time_total)
ic(f"Total Sales per Clerk between 11:30 & 14:00: {count_sales_time}")