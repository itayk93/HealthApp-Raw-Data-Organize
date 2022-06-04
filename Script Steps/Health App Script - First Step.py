# Code by Itay Karkason
import pandas as pd
import glob
from datetime import date
from openpyxl import load_workbook
import os
from datetime import datetime
import datetime

# Reda the input xml and convert it to csv
df_xml = pd.read_xml(folder_location + 'Input/export.xml')
df_xml[['type', 'sourceName', 'sourceVersion', 'unit', 'creationDate', 'startDate',
        'endDate', 'value', 'device']].to_csv(folder_location + 'Input/Data - Health.csv',index=False)

# Read the input
data = pd.read_csv(folder_location + 'Input/Data - Health.csv',
                   parse_dates=['creationDate'], dayfirst=False, low_memory=False)

# Convert the _creationDate to a date format
data['creationDate'] = data['creationDate'].dt.date
data = data.rename(columns={'creationDate': 'date'})

# Create the data for output with the needed columns
data_to_output = data[['date', 'sourceName', 'unit', 'value', 'type']]

# Convert Date to datetime Values
pd.options.mode.chained_assignment = None
data_to_output['date'] = pd.to_datetime(data_to_output['date'])

# Delete data from chosen dates in dates_to_cancel.xlsx file
dates_to_cancel = pd.read_excel(folder_location + "dates_to_cancel.xlsx")
start_date_to_cancel = pd.to_datetime(dates_to_cancel['start_date_to_cancel'])
end_date_to_cancel = pd.to_datetime(dates_to_cancel['end_date_to_cancel'])

dates_to_output_to_drop = pd.DataFrame(columns=data_to_output.columns)

for index, row in dates_to_cancel.iterrows():
    start_date_to_cancel = row['start_date_to_cancel']
    end_date_to_cancel = row['end_date_to_cancel']

    data_to_output_filtered_to_drop = data_to_output[
        (data_to_output['date'] >= pd.Timestamp(start_date_to_cancel)) &
        (data_to_output['date'] < pd.Timestamp(end_date_to_cancel))
        ]
    print("The data between " + str(pd.Timestamp(start_date_to_cancel))[:-9] + " to " + str(
        pd.Timestamp(end_date_to_cancel))[:-9] + " was deleted")
    dates_to_output_to_drop = pd.concat([dates_to_output_to_drop, data_to_output_filtered_to_drop])

dates_to_output_to_drop_list = dates_to_output_to_drop['date'].values.tolist()
for date_to_cancel in dates_to_output_to_drop_list:
    data_to_output = data_to_output[(data_to_output['date'] != date_to_cancel)]

# Create raw data files for each type of workout from the input file
data_group = data_to_output.groupby('type').count().reset_index()['type']

for i in range(0, len(data_group)):
    name_filter = data_group.iloc[i]
    mask_data = data_to_output['type'] == name_filter
    data_to_output[mask_data][['date', 'sourceName', 'unit', 'value', 'type']].to_csv(name_filter + ".csv")

