import csv


## never used this

def connect_session_and_survey_values(input_file_sessions, input_file_surveys, output_file):
	try:

		connected_session_survey = []

		with open(input_file_surveys, 'r') as csvfile_surveys, open(input_file_sessions, 'r') as csvfile_sessions:
			reader1 = csv.DictReader(csvfile_surveys)
			reader2 = csv.DictReader(csvfile_sessions)

			for row1 in reader1:
				csvfile_sessions.seek(0)
				sessionID = row1['sessionID']
				phubbs = -1

				for row2 in reader2:
					if row2['sessionID'] == sessionID:
						phubbs = row2['phubbsWhileSession']

				connected_session_survey.append({
						'subjectID': row1['subjectID'], 
						'condition': row1['condition'],
						'sessionID': row1['sessionID'],
						'phubbsWhileSession': phubbs, 
						'pci_value': row1['pci_value'],
						'rschi_value': row1['rschi_value'],
						'rschi_value_anger': row1['rschi_value_anger'],
						'rschi_value_autonomy': row1['rschi_value_autonomy'],
						'rschi_value_apathy': row1['rschi_value_apathy'],
						'pdso_value_self': row1['pdso_value_self'],
						'pdso_value_other': row1['pdso_value_other'],
						'ps_value': row1['ps_value'],
						'ios_value': row1['ios_value'],
						'csi': row1['csi']
					})

		
		fields = ['subjectID', 'condition', 'sessionID', 'phubbsWhileSession', 'pci_value', 
		'rschi_value', 'rschi_value_anger', 'rschi_value_autonomy', 
		'rschi_value_apathy', 'pdso_value_self', 'pdso_value_other', 
		'ps_value', 'ios_value', 'csi']
		with open(output_file, 'w', newline='') as csvfile_output:
			writer = csv.DictWriter(csvfile_output, fieldnames=fields)
			writer.writeheader()
			writer.writerows(connected_session_survey)

	except Exception as e:
		print(f"Error cleaning CSV file: {e}")

connect_session_and_survey_values('phubbs-per-session-a.csv', 'survey_values_a.csv', 'survey-values-phubbs-a.csv')
connect_session_and_survey_values('phubbs-per-session-b.csv', 'survey_values_b.csv', 'survey-values-phubbs-b.csv')