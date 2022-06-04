# Code by Itay Karkason
import pandas as pd
import glob
from datetime import date
from openpyxl import load_workbook
import os
from datetime import datetime
import datetime

# Making Sub-files to Active Energy Burned - By each kind of app
data_Active_energy_burned = pd.read_csv(folder_location + 'HKQuantityTypeIdentifierActiveEnergyBurned.csv',
                                        parse_dates=['date'], dayfirst=False)

data_Active_energy_burned_group = data_Active_energy_burned.groupby(
    ["date", "sourceName"]).sum('value').to_csv(
    folder_location + "HKQuantityTypeIdentifierActiveEnergyBurned - Output Group.csv")
data_Active_energy_burned_group = pd.read_csv(
    folder_location + 'HKQuantityTypeIdentifierActiveEnergyBurned - Output Group.csv',
    parse_dates=['date'], dayfirst=False)

data_Active_energy_burned_group["value"] = pd.to_numeric(data_Active_energy_burned_group["value"], downcast='integer')
data_Active_energy_burned_group['unit'] = "Total Calories per day"
data_Active_energy_burned_group['type'] = "HKQuantityTypeIdentifierActiveEnergyBurned"

data_Active_energy_burned_group = data_Active_energy_burned_group[['date', 'sourceName', 'unit', 'value', 'type']]

# Export the sub files by Apps (under sourceName column), defined in the filter final_files_to_make file
data_group_apps = data_Active_energy_burned_group.groupby('sourceName').sum().reset_index()['sourceName']

apps_to_show = pd.read_excel(folder_location + "final_files_to_make.xlsx", sheet_name="Apps")

for index, row in apps_to_show.iterrows():
    name_filter_app = str(row['name_filter_app'])

    mask_data_app = data_Active_energy_burned_group['sourceName'] == name_filter_app
    data_Active_energy_burned_group[mask_data_app][
        ['date', 'sourceName', 'unit', 'value', 'type']].to_excel(
        folder_location_output + "Active Energy Burned - " + name_filter_app + ".xlsx",
        index=False, sheet_name=name_filter_app)

len_folder_location = len(folder_location)
all_files = glob.glob(folder_location + "HK*.csv")
for filename in all_files:
    print("'" + filename[len_folder_location:] + "' was deleted")
    os.remove(filename)
