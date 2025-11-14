import csv
import os

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))

# path to csv in "Raw_Data"
csv_survey_results = os.path.join(current_directory, '..', 'Raw_Data', 'results-survey.csv')

# PCI := Perceived Conversation Intimicy (likert: agree = 7, disagree = 1)
# best intimicy: 7
## pci_1,3,4,5,6: 7
## pci_2: 1

# RSCHI := Reactance Scale for Human Computer Interaction
# RSCHI1-5 autonomy -> 1
# RSCHI6-9 anger -> 1
# RSCHI10-13 apathy -> 1

# PDSO := Perceived distraction from self and others (likert: agree = 7, disagree = 1)
# best:
## pdso1,3,5,6: 1
## pdso2,4: 7
# PDSO1-3 self distraction 
# PDSO4-6 other distraction

# PS := Phubbing Scale (likert: agree = 5, disagree = 1)
# best: 1

# IOS := inclusion of self and other (far = 1, close = 7)
# best: 7 but depends on relation

# CSI := context of social interaction


def convert_likert_7(number):
	return (8-number)

def value_survey_per_person(input_file, output_file_a, output_file_b, output_file_no_condition):
	try:

		survey_values_a = []
		survey_values_b = []
		survey_values_no_condition = []
		counter = 0

		with open(input_file, 'r') as csvfile_input:
			reader = csv.DictReader(csvfile_input)

			# for condition a (without intervention)
			for row in reader:

				subjectID = row['G00001']
				condition = row['G00002']
				sessionID = row['G00003']

				pci_value = (int(row['PCI[PCI1]'])
					+ convert_likert_7(int(row['PCI[PCI2]'])) 
					+ int(row['PCI[PCI3]']) 
					+ int(row['PCI[PCI4]']) 
					+ int(row['PCI[PCI5]']) 
					+ int(row['PCI[PCI6]'])) / 6

				rschi_value_autonomy = (int(row['RSHCI01[RSHCI1]']) 
					+ int(row['RSHCI01[RSHCI2]'])
					+ int(row['RSHCI01[RSHCI3]'])
					+ int(row['RSHCI01[RSHCI4]']) 
					+ int(row['RSHCI01[RSHCI5]'])) / 5
				rschi_value_anger = (int(row['RSHCI02[RSHCI6]'])
					+ int(row['RSHCI02[RSHCI7]']) 
					+ int(row['RSHCI02[RSHCI8]'])
					+ int(row['RSHCI02[RSHCI9]'])) / 4
				rschi_value_apathy = (int(row['RSHCI03[RSHCI10]']) 
					+ int(row['RSHCI03[RSHCI11]'])
					+ int(row['RSHCI03[RSHCI12]'])
					+ int(row['RSHCI03[RSHCI13]'])) / 4
				rschi_value = (rschi_value_anger + rschi_value_autonomy + rschi_value_apathy) / 3

				pdso_value_self = (int(row['PDSO01[PDSO1]'])
					+ convert_likert_7(int(row['PDSO01[PDSO2]']))
					+ int(row['PDSO01[PDSO3]'])) / 3
				pdso_value_other = (convert_likert_7(int(row['PDSO02[PDSO4]']))
					+ int(row['PDSO02[PDSO5]'])
					+ int(row['PDSO02[PDSO6]'])) / 3

				ps_value = (int(row['PS[PS1]']) + int(row['PS[PS2]']) + int(row['PS[PS3]']) + int(row['PS[PS4]']) + int(row['PS[PS5]']) 
					+ int(row['PS[PS6]']) + int(row['PS[PS7]']) + int(row['PS[PS8]']) + int(row['PS[PS9]']) + int(row['PS[PS10]'])) / 10

				ios_value = row['IOS']

				csi = row['CSI']


				if condition == 'A':
					survey_values_a.append({
						'subjectID': subjectID,
						'condition': condition,
						'sessionID': sessionID, 
						'pci_value': pci_value,
						'rschi_value': rschi_value,
						'rschi_value_anger': rschi_value_anger,
						'rschi_value_autonomy': rschi_value_autonomy,
						'rschi_value_apathy': rschi_value_apathy,
						'pdso_value_self': pdso_value_self,
						'pdso_value_other': pdso_value_other,
						'ps_value': ps_value,
						'ios_value': ios_value,
						'csi': csi
					})

				elif condition == 'B':
					survey_values_b.append({
						'subjectID': subjectID,
						'condition': condition,
						'sessionID': sessionID, 
						'pci_value': pci_value,
						'rschi_value': rschi_value,
						'rschi_value_anger': rschi_value_anger,
						'rschi_value_autonomy': rschi_value_autonomy,
						'rschi_value_apathy': rschi_value_apathy,
						'pdso_value_self': pdso_value_self,
						'pdso_value_other': pdso_value_other,
						'ps_value': ps_value,
						'ios_value': ios_value,
						'csi': csi
					})

				else:
						survey_values_no_condition.append({
						'subjectID': subjectID,
						'condition': condition,
						'sessionID': sessionID, 
						'pci_value': pci_value,
						'rschi_value': rschi_value,
						'rschi_value_anger': rschi_value_anger,
						'rschi_value_autonomy': rschi_value_autonomy,
						'rschi_value_apathy': rschi_value_apathy,
						'pdso_value_self': pdso_value_self,
						'pdso_value_other': pdso_value_other,
						'ps_value': ps_value,
						'ios_value': ios_value,
						'csi': csi
					})


		fields = ['subjectID', 'condition', 'sessionID', 'pci_value', 
		'rschi_value', 'rschi_value_anger', 'rschi_value_autonomy', 
		'rschi_value_apathy', 'pdso_value_self', 'pdso_value_other', 
		'ps_value', 'ios_value', 'csi']
		with open(output_file_a, 'w', newline='') as csvfile_output:
			writer = csv.DictWriter(csvfile_output, fieldnames=fields)
			writer.writeheader()
			writer.writerows(survey_values_a)

		with open(output_file_b, 'w', newline='') as csvfile_output:
			writer = csv.DictWriter(csvfile_output, fieldnames=fields)
			writer.writeheader()
			writer.writerows(survey_values_b)

		with open(output_file_no_condition, 'w', newline='') as csvfile_output:
			writer = csv.DictWriter(csvfile_output, fieldnames=fields)
			writer.writeheader()
			writer.writerows(survey_values_no_condition)


	except Exception as e:
		print(f"Error cleaning CSV file: {e}")


value_survey_per_person(csv_survey_results, 'survey_values_a.csv', 'survey_values_b.csv', 'survey_values_no_condition.csv')