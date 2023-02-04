import pandas as pd

eventbrite_data = pd.read_csv('eventbrite.csv')
eventbriteList = eventbrite_data[["Order #", "First Name", "Last Name"]]
print("First Name and Last Names are:")
print(eventbriteList)

zoom_data = pd.read_csv('zoom.csv')
colsToSum = ['Duration (Minutes)']
zoom_data['Leave Time'] = pd.to_datetime(zoom_data['Leave Time'])
attendeeDuration = zoom_data.groupby(by='Name (Original Name)').aggregate({'Duration (Minutes)':['sum'],'Leave Time':['max']})
attendeeDuration.columns = ['Total Duration (Mins)', 'Leave Time']
pd.options.display.max_rows = 200

zoomList = [[attendeeDuration]]
print(zoomList)