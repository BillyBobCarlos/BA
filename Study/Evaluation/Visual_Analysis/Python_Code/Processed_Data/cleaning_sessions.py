import matplotlib.pyplot as plt  
import csv
from datetime import datetime, timedelta
import os

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))

# path to csv in "Raw_Data"
csv_social_interactions = os.path.join(current_directory, '..', 'Raw_Data', 'social-interactions.csv')


# processing data
# first clean data by delete double starttime
# then merge sessions which are < 3 apart
# save output data as 'socialsessions.csv'

def merge_social_sessions(input_file, output_file, number):
	try:
		with open(input_file, 'r') as csvfile:
			reader = csv.DictReader(csvfile)

			# Get the first row
			previous_row = next(reader, None)

			# Cleaned rows
			merged_rows = []
			merge_rows = False

			for current_row in reader:
				if previous_row['subjectID'] == current_row['subjectID'] and previous_row['dateStartOfInteraction'] == current_row['dateStartOfInteraction']:
					if (datetime.strptime(current_row['startOfInteraction'], '%H:%M:%S') - datetime.strptime(previous_row['endOfInteraction'], '%H:%M:%S')) <= timedelta(minutes=number):
						diff = (datetime.strptime(current_row['startOfInteraction'], '%H:%M:%S') - datetime.strptime(previous_row['endOfInteraction'], '%H:%M:%S'))
						current_row['startOfInteraction'] = previous_row['startOfInteraction']
						merge_rows = True

				if not merge_rows:
					merged_rows.append(previous_row)

				previous_row = current_row
				merge_rows = False

			merged_rows.append(previous_row)

		with open(output_file, 'w', newline='') as csvfile:
			fieldnames = reader.fieldnames
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

			writer.writeheader()
			writer.writerows(merged_rows)



	except Exception as e:
		print(f"Error cleaning CSV file: {e}")


def cleaning_social_sessions(input_file, output_file):
	try:
		with open(input_file, 'r') as csvfile:
			reader = csv.DictReader(csvfile)

			# Get the first row
			previous_row = next(reader, None)

			# Cleaned rows
			cleaned_rows = []
			delete_row = False

			for current_row in reader:
				if previous_row['subjectID'] == current_row['subjectID'] and previous_row['dateStartOfInteraction'] == current_row['dateStartOfInteraction']:
					if previous_row['startOfInteraction'] == current_row['startOfInteraction']:
						delete_row = True

				if not delete_row:
					cleaned_rows.append(previous_row)

				previous_row = current_row
				delete_row = False

			cleaned_rows.append(previous_row)

		with open(output_file, 'w', newline='') as csvfile:
			fieldnames = reader.fieldnames
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

			writer.writeheader()
			writer.writerows(cleaned_rows)


	except Exception as e:
		print(f"Error cleaning CSV file: {e}")


#cleaning_social_sessions(csv_social_interactions, 'cleaned-social-interactions.csv')
#merge_social_sessions('cleaned-social-interactions.csv', 'social-sessions.csv', 3)
