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

ic(unique_drinks)
ic(unique_sauces)

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

ic(drink_cnt)
final_drink_cnt = {}

for k, v in drink_cnt.items():
    drink = k[9:]
    k = k[0:8]
    for t_id, clerk in clerk_add_dict.items():
        if k in str(t_id):
            final_drink_cnt[t_id] = clerk + "_" + drink + ": " + str(v)

ic(final_drink_cnt)
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


ic(final_sauce_cnt)


# drink_counts = Counter(drink_clerk_cnt.values())
# sauce_counts = Counter(sauce_clerk_cnt.values())


# ic(sauce_counts)
# ic(drink_counts)
# add_pc_dict = {key: value for key, value in zip(df['Transaction_ID'], df['Clerk'])}
#
# add_ml_dict = {}
#
#
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

# # How many transaction s per Clerk per day. Count how many accurances of "Name" in "Clerk" Column
# drinks = ['Pepsi', 'Pepsi Max', 'Sunkist', 'Lemonade', 'Solo', 'Pepsi Large',
#                   'Pepsi Max Large', 'Sunkist Large', 'Lemonade Large', 'Solo Large', 'Water',
#                   'Natural', 'Orange', 'Apple', 'Apple Black', 'Mango Orange',
#                   'Lemon Lipton Iced Tea', 'Peach Lipton Iced Tea', 'Mango Lipton Iced Tea',
#                   'Rasberry Lipton Iced Tea', 'Lemon Lime', 'Grape', 'Orange PT', 'Apple PT',
#                   'Apple Black PT', 'Wild Berry PT']
# employees = ["RENSCHE", "ROB", "SAM"]
# clerk_lst = list(df["Clerk"])
# clerk = []
# rensche = []
# sam = []
# rob = []
# ic(clerk_lst)
#
#
# for v in clerk_lst:
#     if v in employees:
#         clerk.append(v)
#
# for c in clerk:
#     if c == "RENSCHE":
#         rensche.append(c)
#     if c == "ROB":
#         rob.append(c)
#     if c == "SAM":
#         sam.append(c)
#
# rensche_cnt = len(rensche)
# rob_cnt = len(rob)
# sam_cnt = len(sam)
#
# ic(rensche_cnt)
# ic(rob_cnt)
# ic(sam_cnt)
