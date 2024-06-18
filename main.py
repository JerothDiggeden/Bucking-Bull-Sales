import pandas as pd
import numpy as np
import customtkinter as ctk
from icecream import ic


df = pd.read_excel("data/Detailed_Sales_05_16_2022_CLEAN2.xls")

for col in df.columns:
    df[col] = df[col].ffill()

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

ic(df)

ic(df[("Transaction_ID", "Transaction_Date")])

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
