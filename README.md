# HealthApp

Hey! This code purpose is to organise the xml file with all the data collected from Health App on Iphone.
It organises the data into several files which are ready to upload to any BI system (in my cace - Tableau)

How to run the software:

1. download the raw data (in xml file) from the Helth App on the Iphone
2. locate it in "Input" Folder
3. Define the "main_folder_location.xlsx" file with your folder location
4. Define the "final_files_to_make.xlsx" file with the files that you want to export at the end, There are a lot of different kinds of measurements in the original data, and there's no use in all of them.
5. Define the "device_holder.xlsx" file to show on the final data your name as the device's holder
6. Define the "dates_to_cancel.xlsx" file in case if there are dates you want to delete from the final data before uploading to a BI system
7. Define the "data_to_cancel.xlsx" file in case if there's any specific data you want to delete from the final data before uploading to a BI system (just copy the data from the output after running the software)

And finally you can run the "Health App Script.py" script


Thank you
