
#----------------------------Importing libraries----------------------------------------

import pandas as pd
import numpy as np
import geopy.distance
import matplotlib.pyplot as plt 
from matplotlib import style
style.use('ggplot')

#-----------------------------------------------------------------------------------------

#Function to find nearest Longitude/Latitude
def nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    # print(idx)
    return array[idx], idx


#---------------------Function that outputs the final DataFrame----------------------------

def merge_wrt_loc(file_1, file_2):

	#Reading CSV files
	df_x = pd.read_csv(file_1)
	df_y = pd.read_csv(file_2)

	#Numpy array of both CSV files
	X = np.array(df_x)
	Y = np.array(df_y)

	global df_x_long
	global df_y_long
	global df_x_lat
	global df_y_lat

	#Long and Lat of Planting Data
	df_x_long=df_x['long']
	df_x_lat=df_x['lat']

	#Long and Lat of Harvest Data
	df_y_long=df_y['long']
	df_y_lat=df_y['lat']

	# Length of both class
	print ('Planting Data size :',len(df_x_long),'\n' 'Harvest Data size :',len(df_y_long))	
	#6314,16626

	#Itterating through file2 to find nearest location corresponding to each sample of harvest data
	for i in range(len(Y)):
		a=Y[i][0]	#ith Long
		b=Y[i][1]	#ith Lat

		#Function call to find nearest Long & Lat
		nearest_long, id_long = nearest(df_x_long, a)
		nearest_lat, id_lat = nearest(df_x_lat, b)

		coords_0=(a,b)							#Itterative point 
		coords_1=(X[id_long][0],X[id_long][1])	#Coordinate corresponding nearest Longitude
		coords_2=(X[id_lat][0],X[id_lat][1])	#Coordinate corresponding nearest Latitude

		#Distace using Vincenty Function 
		dis_1=geopy.distance.vincenty(coords_0, coords_1).km
		dis_2=geopy.distance.vincenty(coords_0, coords_2).km

		#choosing the point with nearest location
		if dis_1 > dis_2:
			final_id = id_long
		else:
			final_id = id_lat

		#Appending data to corresponding list
		variety.append(X[final_id][2])
		seeding_rate.append(X[final_id][3])
		seed_spacing.append(X[final_id][4])

	#Creating DataFrame
	df = pd.DataFrame(df_y, columns = ['long', 'lat', 'yield'])
	df['variety'] = variety
	df['seeding_rate'] = seeding_rate
	df['seed_spacing'] = seed_spacing
	return df
#------------------------------------End of Function--------------------------------------

vinc_dis=[]
variety = []
seeding_rate = []
seed_spacing = []

#Function call with file path as arrguments
df_final= merge_wrt_loc('planting_sample_data.csv','harvest_sample_data.csv')

#-------------------Field visualization w.r.t location of data collected------------------

plt.scatter(df_x_long,df_x_lat, label='Planting Data', color='green', s=2, marker='x')
plt.scatter(df_y_long,df_y_lat, label='Harvest Data', color='red', s=2, marker='o')
plt.title("longitude vs latitude")
plt.xlabel("longitude")
plt.ylabel("latitude")
plt.legend(loc='upper right')
plt.show()

#-----------------------------------------------------------------------------------------

# printing fist 10 samples
print(df_final.head(10))
# saving to a CSV file
df_final.to_csv('Merged_data.csv', encoding='utf-8', index=False)	

#-----------------------------------------------------------------------------------------