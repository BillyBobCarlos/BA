import matplotlib.pyplot as plt  
import csv
from datetime import datetime
import os

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))

# path to csv in "Raw_Data"
csv_phone_use = os.path.join(current_directory, '..', 'Raw_Data', 'phone-use.csv')
csv_phone_use_a = os.path.join(current_directory, '..', 'Raw_Data', 'phone-use-a.csv')
csv_phone_use_b = os.path.join(current_directory, '..', 'Raw_Data', 'phone-use-b.csv')

# number of unlocks during one social interaction per Person
# no relation

# csv/-filter:
## phoneUse: showedIntervention = false/true
## socialInteraction

def isFirstTimeBeforeSecondTime(first_time, second_time):
	if datetime.strptime(first_time, '%H:%M:%S') <= datetime.strptime(second_time, '%H:%M:%S'):
		return True
	return False

def isFirstTimeAfterSecondTime(first_time, second_time):
	if datetime.strptime(first_time, '%H:%M:%S') >= datetime.strptime(second_time, '%H:%M:%S'):
		return True
	return False

def process_data(input_file_sessions, input_file_phone_use, output_file):
	try:
		matched_data = []

		with open(input_file_sessions, 'r') as csvfile_interaction, open(input_file_phone_use, 'r') as csvfile_phoneUse:
			reader1 = csv.DictReader(csvfile_interaction)
			reader2 = csv.DictReader(csvfile_phoneUse)

			for row1 in reader1:
				csvfile_phoneUse.seek(0) # reset file reader to beginning of phoneUse
				count_matches = 0 # counter for the number of phoneUses per interaction
				phubbs = []
				conditions = []
				common_char = ''

				for row2 in reader2:
					# compare each social interaction with phoneUse-logs
					if row1['subjectID'] == row2['subjectID'] and row1['dateStartOfInteraction'] == row2['date']:
						if isFirstTimeBeforeSecondTime(row1['startOfInteraction'], row2['startOfPhoneUse']):
							if isFirstTimeAfterSecondTime(row1['endOfInteraction'], row2['endOfPhoneUse']):
							# current phoneUse is during current socialInteraction
								phubbDuration = (datetime.strptime(row2['endOfPhoneUse'], '%H:%M:%S') - datetime.strptime(row2['startOfPhoneUse'], '%H:%M:%S'))
								if not "-1 day" in str(phubbDuration):
									phubbs.append(str(phubbDuration))
									count_matches += 1

				sessionDuration = (datetime.strptime(row1['endOfInteraction'], '%H:%M:%S') - datetime.strptime(row1['startOfInteraction'], '%H:%M:%S'))
				if "-1 day" in str(sessionDuration):
					sessionDuration = str(sessionDuration).replace('-1 day, ', '')

				matched_data.append({
					'subjectID': row1['subjectID'],
					'sessionID': row1['ID'],
					'sessionDate': row1['dateStartOfInteraction'],
					'sessionStart': row1['startOfInteraction'],
					'sessionEnd': row1['endOfInteraction'],
					'sessionDuration': sessionDuration,
					'phubbsWhileSession': count_matches,
					'phubbs': phubbs
				})

		fields = ['subjectID', 'sessionID', 'sessionDate', 'sessionStart', 'sessionEnd', 'sessionDuration', 'phubbsWhileSession', 'phubbs']
		with open(output_file, 'w', newline='') as csvfile_output:
			writer = csv.DictWriter(csvfile_output, fieldnames=fields)
			writer.writeheader()
			writer.writerows(matched_data)

	except Exception as e:
		print(f"Error cleaning CSV file: {e}")


process_data('social-sessions.csv', csv_phone_use, 'phubbs-per-session.csv')
process_data('social-sessions.csv', csv_phone_use_a, 'phubbs-per-session-a.csv')
process_data('social-sessions.csv', csv_phone_use_b, 'phubbs-per-session-b.csv')