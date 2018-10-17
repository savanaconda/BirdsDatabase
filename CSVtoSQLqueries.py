# To do:
# Create Species ID
# Multiply coordinates data to have a scale of zero
# Add column names to bird query and identity insert on




# Takes in the CSV file and creates the SQL queries to
# insert data into SQL tables

import pandas as pd
import re
from datetime import timedelta
from datetime import datetime
import numpy as np
import time


def clean_data(my_data):
	# Remove problematic rows from data
	error_count = 0
	for (idx,row) in my_data.iterrows():
		# Skip will be used to skip around based on runtime errors
		error = False

		if error == False:
			#  Check latitude: error latitude cannot be converted to float or if it is not in range
			try:
				if not -180 < float(row['Latitude']) < 180:
					# print("Error: Latitude not in range")
					error = True
					error_count += 1
					my_data = my_data.drop([idx])
			except:
				# print("Error: Latitude not in range")
				error = True
				error_count += 1
				my_data = my_data.drop([idx])

		if error == False:
			# Check longitude: error longitude cannot be converted to float or if it is not in range
			try:
				if not -180 < float(row['Longitude']) < 180:
					# print("Error: Longitude not in range")
					error = True
					error_count += 1
					my_data = my_data.drop([idx])
			except:
				# print("Error: Longitude not in range")
				error = True
				error_count += 1
				my_data = my_data.drop([idx])

		if error == False:
			# Check date
			datepattern = re.compile(r'([\d]{4})-([\d]{2})-([\d]{2})')
			m = re.match(datepattern, row['SightingDate'])
			if m is None:
				# print('Error: Date is not proper format')
				error = True
				error_count += 1
				my_data = my_data.drop([idx])

		if error == False:
			# Try to synthesize data into the structure of a query
			# If this fails because of errors in the data, it will skip over line
			try:
				query_mid = "'" + row['Genus'] + "', '" + row['Species'] + "', '" + row['SightingDate'] + "', " + row['Latitude'] + ", " + row['Longitude']
			except Exception as ex:
				# print(ex)
				error_count += 1
				error = True
				my_data = my_data.drop([idx])
	return my_data



# x = cos(lat) * cos(lon)
def x_coord(row):
	lati = float(row['Latitude'])
	longi = float(row['Longitude'])
	x = np.cos(np.deg2rad(lati)) * np.cos(np.deg2rad(longi))
	x = int(round(x,5)*100000)
	return x

# y = cos(lat) * sin(lon)
def y_coord(row):
	lati = float(row['Latitude'])
	longi = float(row['Longitude'])
	y = np.cos(np.deg2rad(lati)) * np.sin(np.deg2rad(longi))
	y = int(round(y,5)*100000)
	return y

# z = sin(lat)
def z_coord(row):
	lati = float(row['Latitude'])
	longi = float(row['Longitude'])
	z = np.sin(np.deg2rad(lati))
	# Multiple by 100000 so that coordinates data is scale of zero so that it can be used as a primary key in SQL database
	z = int(round(z,5)*100000)
	return z



def write_to_tableQuery(data, SQLcolumns, SQLtablename, query_file):
	#Inputs:
	# data is a pandas dataframe with all data
	# SQLcolumns is a list of the names of the SQL columns
	# SQLtablename is the name of the table to be added to
	# query_file is the name of the text file to add SQL queries list to
	
	query_file_object = open(query_file,'w')
	query_start = 'INSERT INTO '
	query_table = SQLtablename
	query_posttable = '\nVALUES ('
	query_end = ');\n'

	for (idx,row) in data.iterrows():
		query_mid = ""
		num_col = len(SQLcolumns)
		idx = 0
		query_cols = '('
		for col in SQLcolumns:
			idx += 1
			# If it is a text type, add in ''
			if col == 'SightingDate' or col == 'Species' or col == 'Genus':
				query_mid = query_mid + "'" + row[col] + "'"
				query_cols = query_cols + col
				# add comma if not last element
				if idx != num_col:
					query_mid = query_mid + ", "
					query_cols = query_cols + ', '
			else:
				query_mid = query_mid + str(row[col])
				query_cols = query_cols + col  
				# add comma if not last element
				if idx != num_col:
					query_mid = query_mid + ", "
					query_cols = query_cols + ', '
		query_cols = query_cols + ')'
		query = query_start + query_table + query_cols + query_posttable + query_mid + query_end
		query_file_object.write(query)


def process_csvrawdata(rawdata):
	# Get only the columns I want from data
	# 'decimallongitude' and 'coordinateuncertaintyinmeters'
	# are technically latitude and longitude, respectively,
	# but they are labelled incorrectly in csv file
	my_columns =['species', 'decimallongitude', 'coordinateuncertaintyinmeters', 'day', 'genus', 'specieskey']
	my_data = rawdata[my_columns].copy()
	my_data = my_data.rename(index=str, columns={"species": "Species", "decimallongitude": "Latitude", 'coordinateuncertaintyinmeters':'Longitude','day':'SightingDate','genus':'Genus','specieskey':'SpeciesID'})

	return my_data

# Creates more meaningful features for date and location
def featureeng(my_data):
	
	# Oldest date in current data is 1960-02-28
	# So absolute time will be w.r.t. 1960-01-01
	start_time = '1960-01-01'
	dt_start_time = datetime.strptime(start_time, '%Y-%m-%d')

	# Create column with absolute time: number of days since start_time specified above
	my_data['AbsoluteDate'] = my_data['SightingDate'].map(lambda x: str((datetime.strptime(x, '%Y-%m-%d')-dt_start_time).days))

	# Create x,y,z 3D coordinates out of latitude and longitude
	my_data['X_coordinates'] = my_data.apply(x_coord, axis=1)
	my_data['Y_coordinates'] = my_data.apply(y_coord, axis=1)
	my_data['Z_coordinates'] = my_data.apply(z_coord, axis=1)

	return my_data


def write_to_CSV(data, filename):
	#Inputs:
	# data is a pandas dataframe with all data
	# filename is the name of the csv file to create
	data.to_csv(filename)



def main():

	# Read data from file
	st=time.time()
	file = 'birbdata_short.csv'
	fulldata = pd.read_csv(file, low_memory = False)
	print('Read File:', time.time()-st)

	# Extract only relevant data and rename columns
	st=time.time()
	my_data = process_csvrawdata(fulldata)
	print('Extract relevant data:', time.time()-st)

	# Truncate the day strings so that we get YYYY-MM-DD format
	# col = my_data.loc[:,'day'].copy()
	st=time.time()
	my_data['SightingDate'] = my_data['SightingDate'].map(lambda x: str(x)[0:10])
	print('Fix date format:', time.time()-st)

	# Removes any bad columns from data with some checks on reasonable values
	st=time.time()
	my_data = clean_data(my_data)
	print('Clean data:', time.time()-st)

	# Creates additional, more meaningful features
	st=time.time()
	my_data = featureeng(my_data)
	print('Feature engineer:', time.time()-st)

	# Main table variables:
	main_columns = ['SpeciesID', 'AbsoluteDate', 'X_coordinates', 'Y_coordinates', 'Z_coordinates']
	main_query_table = 'Birds.SpeciesSightings'
	main_query_out_file = 'SQLqueries_maintable.txt'

	# Classification table variables:
	class_columns = ['SpeciesID', 'Species', 'Genus']
	class_query_table = 'Birds.Classifications'
	class_query_out_file = 'SQLqueries_classtable.txt'

	# Date table variables:
	date_columns = ['AbsoluteDate', 'SightingDate']
	date_query_table = 'Birds.Dates'
	date_query_out_file = 'SQLqueries_datetable.txt'

	# Location table variables:
	location_columns = ['X_coordinates', 'Y_coordinates', 'Z_coordinates', 'Latitude', 'Longitude']
	location_query_table = 'Birds.Locations'
	location_query_out_file = 'SQLqueries_locationtable.txt'

	# Writes query structures to text files to paste into SQL query
	st=time.time()
	write_to_tableQuery(my_data, main_columns, main_query_table, main_query_out_file)
	write_to_tableQuery(my_data, class_columns, class_query_table, class_query_out_file)
	write_to_tableQuery(my_data, date_columns, date_query_table, date_query_out_file)
	write_to_tableQuery(my_data, location_columns, location_query_table, location_query_out_file)
	print('Write text files:', time.time()-st)

	#also write to csvs but only with relevant columns
	write_to_CSV(my_data, 'tensorflow_birddata.csv')



# To add in for timing
# st=time.time()
# print(time.time()-st)

if __name__ == '__main__':
   main()
	 
