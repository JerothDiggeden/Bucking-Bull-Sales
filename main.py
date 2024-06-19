import pandas as pd
import numpy as np
import customtkinter as ctk
from icecream import ic


def contains_pc(cell):
    return 'PC' in str(cell)

def contains_ml(cell):
    return 'ML' in str(cell)


employees = ["RENSCHE", "ROB", "SAM"]

df = pd.read_excel("data/Detailed_Sales_05_16_2022_CLEAN2.xls")

for col in df.columns:
    df[col] = df[col].ffill()

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

ic(df)

all_trans_id = list(df["Transaction_ID"])
unique_id = list(df["Transaction_ID"].unique())

for i, v in enumerate(unique_id):
    unique_id[i] = int(v)

for i, v in enumerate(all_trans_id):
    all_trans_id[i] = int(v)

ic(all_trans_id)
ic(unique_id)

trans_date = list(df["Transaction_Date"])
clerk = list(df["Clerk"])

dict = {}

assoc = df[(df["Transaction_ID"] == 12382776.0) & (df["Clerk"] == "RENSCHE")][["Transaction_Date", "Clerk"]]

ic(assoc)

assoc2 = df[df["Transaction_ID"] == 12382776.0][["Transaction_ID", "Transaction_Date", "Clerk"]]

ic(assoc2)

mask_pc = df.map(contains_pc)
mask_ml = df.map(contains_ml)
pc = df[mask_pc]
ml = df[mask_ml]

add_ml_day = list(ml["Transaction_Date"].dropna().drop_duplicates())
add_pc_day = list(pc["Transaction_Date"].dropna().drop_duplicates())

add_pc_dict = {}
add_ml_dict = {}
clerk_add_dict = {}

for i, v in df.iterrows():
    for pc in add_pc_day:
        if pc in v['Transaction_Date']:
            key = v['Transaction_ID']
            value = v['Transaction_Date']
            add_pc_dict[key] = value

for i, v in df.iterrows():
    for ml in add_ml_day:
        if ml in v['Transaction_Date']:
            key = v['Transaction_ID']
            value = v['Transaction_Date']
            add_ml_dict[key] = value

for i, v in df.iterrows():
    # Ensure 'Clerk' column value is a string before checking for substring membership
    if isinstance(v['Clerk'], (float, int)):
        pass
    else:
        for emp in employees:
            if emp in v['Clerk']:
                key = v['Transaction_ID']
                value = v['Clerk']
                clerk_add_dict[key] = value

ic(add_pc_dict)
ic(add_ml_dict)
ic(clerk_add_dict)

drink_clerk_cnt = {}

for k, c in clerk_add_dict.items():
    for id, d in add_ml_dict.items():
        if k == id:
            key = k
            value = c
            drink_clerk_cnt[key] = value

ic(drink_clerk_cnt)
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
