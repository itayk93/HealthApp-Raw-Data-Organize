# Code by Itay Karkason
import pandas as pd
import glob
from datetime import date
from openpyxl import load_workbook
import os
from datetime import datetime
import datetime

# Read defined labels from final_files_to_make file and add them to the output
labels_to_add = pd.read_excel(folder_location + "final_files_to_make.xlsx", sheet_name="Main Files")

for index, row in labels_to_add.iterrows():
    name_filter = str(row['name_filter'])
    unit = str(row['unit'])
    file_name_new = str(row['file_name_new'])

    # Make and output for each defined file in the final_files_to_make file
    data_walking_step_length = pd.read_csv(name_filter + '.csv', parse_dates=['date'], dayfirst=False)

    data_walking_step_length_group = data_walking_step_length.groupby('date').mean('value').to_csv(
        folder_location + name_filter + '.csv' + ' - Output Group.csv')
    data_walking_step_length_group = pd.read_csv(folder_location + name_filter + '.csv' + ' - Output Group.csv',
                                                 parse_dates=['date'], dayfirst=False)

    # Add columns with the defined data from device_holder file
    data_walking_step_length_group['sourceName'] = device_holder
    data_walking_step_length_group['unit'] = unit
    data_walking_step_length_group['type'] = name_filter

    data_walking_step_length_group[[
        'date', 'sourceName', 'unit', 'value', 'type']].to_excel(
        folder_location_output + file_name_new + ".xlsx", index=False, sheet_name=file_name_new)
