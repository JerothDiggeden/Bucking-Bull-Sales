import pandas as pd
import numpy as np
import customtkinter as ctk
from icecream import ic
from collections import Counter


def contains_pc(cell):
    return 'PC' in str(cell)


def contains_ml(cell):
    return 'ML' in str(cell)


employees = ["RENSCHE", "ROB", "SAM"]
df = pd.read_excel("data/Detailed_Sales_05_16_2022_CLEAN2.xls")
times = df

for col in df.columns:
    df[col] = df[col].ffill()

all_trans_id = list(df["Transaction_ID"])
unique_id = list(df["Transaction_ID"].unique())

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

# time_cnt = list(times[(times['Transaction_Date'] > 1130) & (times['Transaction_Date'] < 2101)])
# CREATE A DICTIONARY LINKING ALL TRANS ID'S TO A CLERK
for i, v in df.iterrows():
    # Ensure 'Clerk' column value is a string before checking for substring membership
    if isinstance(v['Clerk'], (float, int)):
        pass
    else:
        for emp in employees:
            if emp in v['Clerk']:
                key = v['Transaction_ID']
                key = round(key)
                value = v['Clerk']
                clerk_add_dict[key] = value

# CREATE DICT OF ALL OCCURANCES OF SAUCES SOLD PER TRANS ID
for i, v in df.iterrows():
    for pc in add_pc_day:
        if pc in v['Transaction_Date']:
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
        if ml in v['Transaction_Date']:
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
        k = round(k)
        k = str(k)
        if i in v:
            drink_cnt[k + "_" + i] = len(v)

final_drink_cnt = {}

for k, v in drink_cnt.items():
    drink = k[9:]
    k = k[0:8]
    for t_id, clerk in clerk_add_dict.items():
        if k in str(t_id):
            final_drink_cnt[t_id] = clerk + "_" + drink + ": " + str(v)

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
    sauce = k[9:]
    k = k[0:8]
    for t_id, clerk in clerk_add_dict.items():
        if k in str(t_id):
            final_sauce_cnt[t_id] = clerk + "_" + sauce + ": " + str(v)

times['Transaction_Date'] = times['Transaction_Date'].str[9:-2]

times_dict = {}

for i, row in times.iterrows():
    transaction_id = row["Transaction_ID"]
    transaction_id = round(transaction_id)
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

for i, v in times_dict.items():
    for id, clerk in clerk_add_dict.items():
        if id == i:
            v = str(v)
            count_sales_time.append(clerk)
            count_sales_time_total = Counter(count_sales_time)
            count_sales_time_total = dict(count_sales_time_total)

# How many transaction s per Clerk per day. Count how many accurances of "Name" in "Clerk" Column
employees = ["RENSCHE", "ROB", "SAM"]
clerk_lst = list(df["Clerk"])
clerk = []
rensche = []
sam = []
rob = []


for v in clerk_lst:
    if v in employees:
        clerk.append(v)

for c in clerk:
    if c == "RENSCHE":
        rensche.append(c)
    if c == "ROB":
        rob.append(c)
    if c == "SAM":
        sam.append(c)

rensche_cnt = len(rensche)
rob_cnt = len(rob)
sam_cnt = len(sam)

final_sauce_cnt = sorted(final_sauce_cnt.items())
final_drink_cnt = sorted(final_drink_cnt.items())
ic(f"Total Sales per Clerk between 11:30 & 14:00: {count_sales_time_total}")
ic(final_sauce_cnt)
ic(final_drink_cnt)
ic(f"Rensche Total Sales: {rensche_cnt}")
ic(f"Rob Total Sales: {rob_cnt}")
ic(f"Sam Total Sales: {sam_cnt}")

ic(count_sales_time_total)



# for v in assoc2["Transaction_Date"]:
#         for d in add_pc_day:
#             if d in v:
#                 var = assoc2["Clerk"][d]

# ic(pc)
# ic(ml)


# isolate_sale.set_index(["Description", "PLU", "Quantity", "Sales Inc Sales Ex", "Original Item Disc."], inplace=True)
# ic(isolate_sale.columns)

# ic(isolate_sale["Description"])
#
# ic(isolate_sale)
