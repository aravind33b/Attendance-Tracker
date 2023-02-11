import pandas as pd
import numpy as np

date = pd.to_datetime('today').date()

writer = pd.ExcelWriter('attendance' + date.strftime("%Y%m%d") + '.xlsx', engine='xlsxwriter')

#read data from the excel sheets and have them objects
eboard_data = pd.read_csv('E-Board.csv')

senators_data = pd.read_csv('Senators.csv')

eventbrite_data = pd.read_csv('eventbrite_data.csv')

zoom_data = pd.read_csv('zoom_data.csv')

eventbrite_data["Full Name"] = eventbrite_data["First Name"].astype(str) +" "+ eventbrite_data["Last Name"].astype(str)

eventbrite_data["Role"] = eventbrite_data['Full Name'].isin(eboard_data['Full Name'])

eventbrite_data["Role"].replace(True, 'E-Board Member', inplace=True)

eventbrite_data["Role"] = eventbrite_data[eventbrite_data["Role"]!="E-Board Member"]['Full Name'].isin(senators_data['Full Name'])

eventbrite_data["Role"].replace(True, 'Senator', inplace=True)

eventbrite_data['Role'].replace(False, 'Member', inplace=True)

eventbrite_data['Role'].fillna('E-Board Member', inplace=True)

eventbriteList = eventbrite_data[["Order #", "Full Name", "Role"]]

print("Attendees List:", eventbriteList)

eventbriteList.index = range(1, eventbriteList.shape[0] + 1)

eventbriteList.to_excel(writer, sheet_name = "Eventbrite", index = True)

# colsToSum = ['Duration (Minutes)']

zoom_data['Leave Time'] = pd.to_datetime(zoom_data['Leave Time']).dt.time
colName = "User Email"
# if(zoom_data['User Email'].notna().values.any()):
#     zoom_data['Leave Time'] = zoom_data.groupby(['Name (Original Name)', 'User Email'])['Leave Time'].transform('max')
#     zoom_data['Total Duration (Mins)'] = zoom_data.groupby(['Name (Original Name)', 'User Email'])['Duration (Minutes)'].transform('sum')

# elif(zoom_data['User Email'].isna().values.any()):
#     zoom_data['Leave Time'] = zoom_data.groupby(['Name (Original Name)', 'User Email'])['Leave Time'].transform('max')
#     zoom_data['Total Duration (Mins)'] = zoom_data.groupby(['Name (Original Name)', 'User Email'])['Duration (Minutes)'].transform('sum')

zoom_data['Leave Time'] = zoom_data.groupby(['Name (Original Name)'])['Leave Time'].transform('max')
zoom_data['Total Duration (Mins)'] = zoom_data.groupby(['Name (Original Name)'])['Duration (Minutes)'].transform('sum')

attendeeList = zoom_data[['Name (Original Name)', 'Leave Time', 'Total Duration (Mins)']]

attendeeList.rename(columns={"Name (Original Name)": "Full Name"}, inplace=True)

pd.options.display.max_rows = 200

attendeeList = attendeeList.drop_duplicates(keep='last', ignore_index=True)

cmpTime = pd.to_datetime('01/14/2023 3:50:00 PM')
cmpTime = cmpTime.time()
# print(cmpTime)

attendeeList["Role"] = attendeeList['Full Name'].isin(eboard_data['Full Name'])

attendeeList["Role"].replace(True, 'E-Board Member', inplace=True)

attendeeList["Role"] = attendeeList.loc[attendeeList["Role"]!="E-Board Member"]['Full Name'].isin(senators_data['Full Name'])

attendeeList["Role"].replace(True, 'Senator', inplace=True)

attendeeList['Role'].replace(False, 'Member', inplace=True)

attendeeList['Role'].fillna('E-Board Member', inplace=True)

attendeeList["Attendance"] = np.where(((attendeeList['Total Duration (Mins)'] >= 75) & (attendeeList['Leave Time'] >= cmpTime)), 'Yes', 'No')

print(attendeeList)

attendeeList.index = range(1, attendeeList.shape[0] + 1)

attendeeList.to_excel(writer, sheet_name='Zoom', index = True)

writer.close()