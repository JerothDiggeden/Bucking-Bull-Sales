import pandas as pd
import math
import numpy as np
import customtkinter as ctk
from icecream import ic
from collections import Counter
from tkinter import filedialog, messagebox


# CUSTOMTKINTER THEME
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("C:/Generate Charts/Day_Grey.json")
# ROOT SETTINGS
root = ctk.CTk()
root.geometry("300 x 700")
root.title("Generate Charts")

global df
global times
global unique_id
global unique_drinks
global unique_sauces
global clerk
global final_drink_count
global final_sauce_count

drinks = {}
sauces = {}
times = pd.DataFrame
clerk_dict = {}


def win_main():
    fme_main.pack(fill=ctk.BOTH, expand=True)


def contains_pc(cell):
    return 'PC' in str(cell)


def contains_ml(cell):
    return 'ML' in str(cell)


def generate_data():
    global df
    global times
    global unique_id
    global unique_drinks
    global unique_sauces
    global final_drink_count
    global final_sauce_count

    unique_drinks = list(set(unique_drinks))
    unique_sauces = list(set(unique_sauces))

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
    clerk = list(df["Clerk"].unique())
    clerk2 = clerk
    for i, v in enumerate(clerk2):
        try:
            clerk[i] = float(v)
        except ValueError:
            continue

    clerk = [v for v in clerk if isinstance(v, str)]
    clerk.remove("Sales Inc")
    clerks = list(clerk)
    ic(type(clerks))
    ic(clerks)
    ic(clerk)

    employees_cnt = list(df["Clerk"])

    for i, v in enumerate(employees_cnt):
        try:
            employees_cnt[i] = float(v)
        except ValueError:
            continue
    employees_cnt = [v for v in employees_cnt if isinstance(v, str)]
    employees_cnt = [v for v in employees_cnt if v != 'Sales Inc']

    ic(employees_cnt)

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
                        # key = round(key)
                        value = v['Clerk']
                        clerk_add_dict[key] = value

    ic(clerk_add_dict)
    df['Transaction_ID'] = df['Transaction_ID'].replace('nan', np.nan)
    df['Transaction_ID'] = df['Transaction_ID'].ffill()

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
            # Convert the Transaction_Date to a string for comparison
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

    ic(add_ml_dict)

    for i in unique_drinks:
        for k, v in add_ml_dict.items():
            if isinstance(k, float) and math.isnan(k):
                continue
            if k != "NaN":
                # k = round(k)
                k = str(k)
                if i in v:
                    drink_cnt[k + "_" + i] = len(v)

    ic(drink_cnt)

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

    ic(add_pc_dict)

    for i in unique_sauces:
        for k, v in add_pc_dict.items():
            # k = round(k)
            k = str(k)
            if i in v:
                sauce_cnt[k + "_" + i] = len(v)

    ic(sauce_cnt)

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

    # How many transactions per Clerk per day

    ic(final_drink_cnt)
    ic(final_sauce_cnt)
    ic(employees_tot_sales)
    ic(clerk)
    unique_id_str = unique_id
    for i, v in enumerate(unique_id):
        unique_id_str[i] = str(unique_id[i])

    update_ddn_clerks(clerks, employees_tot_sales, unique_id_str)
    return final_drink_cnt, final_sauce_cnt, clerk_add_dict

count_sales_time_total = {}


def from_to_times():
    global clerk_add_dict
    global df
    global count_sales_time_total
    global clerk_dict
    from_time = txt_box_from.get("1.0", "6.0")
    to_time = txt_box_to.get("1.0", "6.0")
    from_time = int(from_time)
    to_time = int(to_time)

    times = df
    times['Transaction_Date'] = times['Transaction_Date'].str[10:-9]

    times_dict = {}

    for i, row in times.iterrows():
        transaction_id = row["Transaction_ID"]
        transaction_date = row["Transaction_Date"]

        # Check if transaction_date can be converted to an integer
        try:
            # transaction_date = float(transaction_date)
            # transaction_date = round(transaction_date)
            # transaction_date = str(transaction_date)
            # transaction_date = transaction_date[:-2]
            transaction_date = int(transaction_date)
        except ValueError:
            continue  # Skip this row if transaction_date is not numeric

        # Check if transaction_date falls within the specified range
        if from_time < transaction_date < to_time:
            times_dict[transaction_id] = transaction_date

    count_sales_time = []

    ic(times_dict)
    ic(clerk_dict)

    for i, v in times_dict.items():
        for id, clerk in clerk_dict.items():
            if id == i:
                v = str(v)
                count_sales_time.append(clerk)
                count_sales_time_total = Counter(count_sales_time)
                count_sales_time_total = dict(count_sales_time_total)

    ic(count_sales_time_total)
    lbl_times.configure(text=count_sales_time_total)

def sel_file():
    global df
    global times
    global unique_id
    global unique_drinks
    global unique_sauces
    global drinks
    global sauces
    global clerk_dict
    # SELECT FILE
    file_sel = filedialog.askopenfilename()
    ext_len = len(file_sel)
    ext_len = ext_len - 3
    file_ext = file_sel[ext_len:]
    if file_ext == "lsx":
        df = pd.read_excel(file_sel)
    elif file_ext == "xls":
        df = pd.read_excel(file_sel)
    else:
        messagebox.showerror(message="Wrong File Type! Please Select a XLSX File.")
    df = pd.read_excel("data/DetailedAudit.xls")

    replacements = {'\n': "", "/": "", ":": "", "  ": "_", " ": "_", "_": " "}

    # Function to apply replacements
    def replace_symbols(text, replacements):
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    # Apply replacements to the entire DataFrame
    df = df.applymap(lambda x: replace_symbols(str(x), replacements))

    df.drop(columns=['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 6', 'Unnamed: 7'], inplace=True)
    df.drop([0, 1, 2, 3, 4, 5], axis=0, inplace=True)
    df = df.reset_index(drop=True)
    column_names = ["Transaction_ID", "Transaction_Date", "Terminal_ID", "Receipt_Number",
                    "Clerk", "Sales_Total", "Tax", "Sales_Ex_Tax"]
    df.columns = column_names

    times = df

    for col in df.columns:
        df[col] = df[col].ffill()

    all_trans_id = list(round(df["Transaction_ID"].dropna()))
    unique_id = list(df["Transaction_ID"].dropna().unique())

    all_trans_id = [v for v in all_trans_id if str(v) != 'nan']
    all_trans_id = [int(v) for v in all_trans_id]
    unique_id = [v for v in unique_id if str(v) != 'nan']
    unique_id = [int(v) for v in unique_id]

    ic(unique_id)

    unique_drinks = []
    unique_sauces = []

    for v in df["Transaction_Date"]:
        if "ML" in str(v):
            unique_drinks.append(v)

    for v in df["Transaction_Date"]:
        if "PC" in str(v):
            unique_sauces.append(v)

    drinks, sauces, clerk_dict = generate_data()


def update_ddn_clerks(clerks, sales, id):
    ddn_clerks.configure(values=clerks)
    counter = 0
    for c in clerks:
        clerk_one = clerks[counter]
        one = f"txt_box_clerks{counter + 1}.insert('0.0', clerk_one + ' - ' + str(sales['{clerk_one}']))"
        counter = counter + 1
        exec(one)
    ddn_orders.configure(values=id)


def disp_details():
    global drinks
    global sauces
    order_id = ddn_orders.get()
    lbl_order_sauces.configure(text="")
    lbl_order_drinks.configure(text="")
    if order_id in drinks:
        drink_data = drinks[order_id]
        lbl_order_drinks.configure(text=f"{drink_data}")
    elif order_id in sauces:
        sauce_data = sauces[order_id]
        lbl_order_sauces.configure(text=f"{sauce_data}")
    else:
        lbl_order_drinks.configure(text="No Drink.")
        lbl_order_sauces.configure(text="No Sauce.")


# MAIN WINDOW
fme_main = ctk.CTkFrame(root)
fme_main.pack()
fme_main.grid_columnconfigure(0, weight=1, minsize=200)
fme_main.grid_columnconfigure(1, weight=10, minsize=500)
lbl_space = ctk.CTkLabel(master=fme_main, text="Bucking Bull Sales", font=('Arial', 20))
lbl_space.grid(column=0, row=0, padx=5, pady=5)
btn_sel_file = ctk.CTkButton(master=fme_main, text="Select File", command=sel_file)
btn_sel_file.grid(column=0, row=1, padx=5, pady=5)
lbl_box_clerks = ctk.CTkLabel(master=fme_main, text="Clerk - Sales", font=("Arial 10 bold", 20))
lbl_box_clerks.grid(column=0, row=2, padx=5, pady=5)

txt_box_clerks1 = ctk.CTkTextbox(master=fme_main, height=10, font=("Arial 10 bold", 20))
txt_box_clerks1.grid(column=0, row=3, padx=5, pady=5)
txt_box_clerks2 = ctk.CTkTextbox(master=fme_main, height=10, font=("Arial 10 bold", 20))
txt_box_clerks2.grid(column=0, row=4, padx=5, pady=5)
txt_box_clerks3 = ctk.CTkTextbox(master=fme_main, height=10, font=("Arial 10 bold", 20))
txt_box_clerks3.grid(column=0, row=5, padx=5, pady=5)
txt_box_clerks4 = ctk.CTkTextbox(master=fme_main, height=10, font=("Arial 10 bold", 20))
txt_box_clerks4.grid(column=0, row=6, padx=5, pady=5)
txt_box_clerks5 = ctk.CTkTextbox(master=fme_main, height=10, font=("Arial 10 bold", 20))
txt_box_clerks5.grid(column=0, row=7, padx=5, pady=5)
txt_box_clerks6 = ctk.CTkTextbox(master=fme_main, height=10, font=("Arial 10 bold", 20))
txt_box_clerks6.grid(column=0, row=8, padx=5, pady=5)
txt_box_clerks7 = ctk.CTkTextbox(master=fme_main, height=10, font=("Arial 10 bold", 20))
txt_box_clerks7.grid(column=0, row=9, padx=5, pady=5)
txt_box_clerks8 = ctk.CTkTextbox(master=fme_main, height=10, font=("Arial 10 bold", 20))
txt_box_clerks8.grid(column=0, row=10, padx=5, pady=5)
txt_box_clerks9 = ctk.CTkTextbox(master=fme_main, height=10, font=("Arial 10 bold", 20))
txt_box_clerks9.grid(column=0, row=11, padx=5, pady=5)
txt_box_clerks10 = ctk.CTkTextbox(master=fme_main, height=10, font=("Arial 10 bold", 20))
txt_box_clerks10.grid(column=0, row=12, padx=5, pady=5)

ddn_clerks = ctk.CTkOptionMenu(master=fme_main, values=["Clerk"])
ddn_clerks.grid(column=1, row=1, padx=5, pady=5, sticky="w")

ddn_orders = ctk.CTkOptionMenu(master=fme_main, values=["Orders"])
ddn_orders.grid(column=1, row=1, padx=5, pady=5)

win_main()

btn_disp_det = ctk.CTkButton(master=fme_main, text="Data", command=disp_details)
btn_disp_det.grid(column=1, row=1, padx=5, pady=5, sticky="e")

lbl_order_drinks = ctk.CTkLabel(master=fme_main, text="", font=("Arial 10 bold", 20))
lbl_order_drinks.grid(column=1, row=4, padx=5, pady=5)

lbl_order_sauces = ctk.CTkLabel(master=fme_main, text="", font=("Arial 10 bold", 20))
lbl_order_sauces.grid(column=1, row=5, padx=5, pady=5)

lbl_order_sauces = ctk.CTkLabel(master=fme_main, text="Time Period", font=("Arial 10 bold", 20))
lbl_order_sauces.grid(column=1, row=6, padx=5, pady=5)

txt_box_from = ctk.CTkTextbox(master=fme_main, height=10, font=("Arial 10 bold", 20))
txt_box_from.grid(column=1, row=7, padx=5, pady=5, sticky="w")

lbl_order_sauces = ctk.CTkLabel(master=fme_main, text=" - ", font=("Arial 10 bold", 20))
lbl_order_sauces.grid(column=1, row=7, padx=5, pady=5)

txt_box_to = ctk.CTkTextbox(master=fme_main, height=10, font=("Arial 10 bold", 20))
txt_box_to.grid(column=1, row=7, padx=5, pady=5, sticky="e")

btn_disp_det = ctk.CTkButton(master=fme_main, text="Data", command=from_to_times)
btn_disp_det.grid(column=1, row=8, padx=5, pady=5)

lbl_times = ctk.CTkLabel(master=fme_main, text="", font=("Arial 10 bold", 20))
lbl_times.grid(column=1, row=9, padx=5, pady=5)

root.mainloop()
