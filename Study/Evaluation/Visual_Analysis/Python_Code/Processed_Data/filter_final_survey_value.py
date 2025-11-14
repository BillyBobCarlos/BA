import csv
import os

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))

# path to csv in "Raw_Data"
csv_survey_results = os.path.join(current_directory, '..', 'Raw_Data', 'results-final-survey.csv')

# SM := Smartphone Addiction Scale (likert: agree = 5, disagree = 1)
# best: 1

def value_survey_per_person(input_file, output_file):
	try:

		survey_values = []
		counter = 0

		with open(input_file, 'r') as csvfile_input:
			reader = csv.DictReader(csvfile_input)

			# for condition a (without intervention)
			for row in reader:

				subjectID = row['G00001']
				kr = ""

				sm_value = (int(row['SM01[SM1]'])
					+ int(row['SM01[SM2]'])
					+ int(row['SM01[SM3]']) 
					+ int(row['SM01[SM4]']) 
					+ int(row['SM01[SM5]']) 
					+ int(row['SM01[SM6]'])
					+ int(row['SM01[SM7]'])
					+ int(row['SM02[SM8]'])
					+ int(row['SM02[SM9]'])
					+ int(row['SM02[SM10]'])
					+ int(row['SM02[SM11]'])
					+ int(row['SM02[SM12]'])
					+ int(row['SM02[SM13]'])
					+ int(row['SM02[SM14]'])
					+ int(row['SM02[SM15]']))/ 15

				if row['KR[KR1]'] == 'Y':
					kr = "friendship"
				elif row['KR[KR2]'] == 'Y':
					kr = "family relationship"
				elif row['KR[KR3]'] == 'Y':
					kr = "romantic relationship"
				elif row['KR[KR4]'] == 'Y':
					kr = "classmates/fellow students"
				elif row['KR[KR5]'] == 'Y':
					kr = "work colleagues"
				else:
					kr = "other"

				survey_values.append({
					'subjectID': subjectID,
					'sm_value': sm_value
				})


		fields = ['subjectID', 'sm_value', 'kr']
		with open(output_file, 'w', newline='') as csvfile_output:
			writer = csv.DictWriter(csvfile_output, fieldnames=fields)
			writer.writeheader()
			writer.writerows(survey_values)

	except Exception as e:
		print(f"Error cleaning CSV file: {e}")


value_survey_per_person(csv_survey_results, 'final_survey_values.csv')