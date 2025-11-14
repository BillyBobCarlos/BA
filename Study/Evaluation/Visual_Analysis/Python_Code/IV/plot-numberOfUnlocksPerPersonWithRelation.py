import matplotlib.pyplot as plt
from datetime import datetime
import csv
import os

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))

# path to csv in "Processed_Data"
csv_phubbsPerSession = os.path.join(current_directory, '..', 'Processed_Data', 'phubbs-per-session.csv')
csv_phubbsPerSession_a = os.path.join(current_directory, '..', 'Processed_Data', 'phubbs-per-session-a.csv')
csv_phubbsPerSession_b = os.path.join(current_directory, '..', 'Processed_Data', 'phubbs-per-session-b.csv')

# cast durationstrings to seconds
def cast_sessionduration_in_seconds(input_str):
	duration_obj = datetime.strptime(input_str, "%H:%M:%S")
	duration_in_seconds = duration_obj.hour * 3600 + duration_obj.minute * 60 + duration_obj.second
	return duration_in_seconds

# calculation of relation between number of unlocks and session duration (number/duration)
# round to int with no comma-part
def calculate_relation_between_sessionduration_and_number_of_phubbs(input_str_duration, input_number):
	relation_seconds = input_number/cast_sessionduration_in_seconds(input_str_duration)
	relation_clean = relation_seconds * (10 ** 4)
	relation_round = round(relation_clean, 0) # no part after comma -> int
	return relation_round


# print boxplot for number of phubbs in relation to sessionduration
## comparison between condition a (without intervention) & condition b (with intervention)

## INPUT:	phubbs-per-session-a.csv
## 			phubbs-per-session-b.csv

## OUTPUT:	number-of-unlocks-per-person-and-condition-relation.csv
##			plot_IV_a_b.png

def boxplot_number_of_unlocks_per_person_comparison(input_file_a, input_file_b, output_file_csv, output_file_boxplot):

	plt.style.use('fast')

	# data of condition a (without intervention)
	with open(input_file_a) as csv_file_a:
		csv_reader = csv.DictReader(csv_file_a)

		total_a = []

		for row in csv_reader:

			found = False

			for subject in total_a:
				if row['subjectID'] == subject['subjectID']:
					subject['numberOfUnlocks'] += int(row['phubbsWhileSession'])
					subject['numberOfUnlocksInRelation'] += calculate_relation_between_sessionduration_and_number_of_phubbs(row['sessionDuration'], int(row['phubbsWhileSession']))
					found = True
					break

			if not found:
				total_a.append({
					'subjectID': row['subjectID'],
					'condition': 'A',
					'numberOfUnlocks': int(row['phubbsWhileSession']),
					'numberOfUnlocksInRelation': calculate_relation_between_sessionduration_and_number_of_phubbs(row['sessionDuration'], int(row['phubbsWhileSession']))
				})

	# data of condition b (with intervention)
	with open(input_file_b) as csv_file_b:
		csv_reader = csv.DictReader(csv_file_b)

		total_b = []

		for row in csv_reader:

			found = False

			for subject in total_b:
				if row['subjectID'] == subject['subjectID']:
					subject['numberOfUnlocks'] += int(row['phubbsWhileSession'])
					subject['numberOfUnlocksInRelation'] += calculate_relation_between_sessionduration_and_number_of_phubbs(row['sessionDuration'], int(row['phubbsWhileSession']))
					found = True
					break

			if not found:
				total_b.append({
					'subjectID': row['subjectID'],
					'condition': 'B',
					'numberOfUnlocks': int(row['phubbsWhileSession']),
					'numberOfUnlocksInRelation': calculate_relation_between_sessionduration_and_number_of_phubbs(row['sessionDuration'], int(row['phubbsWhileSession']))
				})

	# save number of unlocks per person in extra csv file
	with open(output_file_csv, 'w', newline='') as csv_file_output:
		fieldnames = ['subjectID', 'condition', 'numberOfUnlocks', 'numberOfUnlocksInRelation']
		writer = csv.DictWriter(csv_file_output, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(total_a)
		writer.writerows(total_b)

	# extract only number of unlocks from both conditions to plot
	num_of_unlocks_relation_a = [subject['numberOfUnlocksInRelation'] for subject in total_a]
	num_of_unlocks_relation_b = [subject['numberOfUnlocksInRelation'] for subject in total_b]

	fig, ax = plt.subplots()

	ax.boxplot(num_of_unlocks_relation_a, positions=[1], labels=['without intervention'])
	ax.boxplot(num_of_unlocks_relation_b, positions=[2], labels=['with intervention'])

	ax.set_ylabel('number of unlocks / session duration (*10^4)')
	ax.set_title('total number of unlocks per person in relation to session durations')

	plt.savefig(output_file_boxplot)

	plt.show()


boxplot_number_of_unlocks_per_person_comparison(csv_phubbsPerSession_a, csv_phubbsPerSession_b, 'number-of-unlocks-per-person-and-condition-relation.csv', 'plot_IV_a_b.png')