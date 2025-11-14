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

# print boxplot for number of phubbs (without any relation)
## comparison between condition a (without intervention) & condition b (with intervention)

## INPUT:	phubbs-per-session-a.csv
## 			phubbs-per-session-b.csv

## OUTPUT:	number-of-unlocks-per-person-and-condition.csv
##			plot_II_a_b.png

def boxplot_number_of_unlocks_per_person_comparison(input_file_a, input_file_b, output_file_csv, output_file_boxplot):

	plt.style.use('fast')

	# data of condition a (without intervention)
	with open(input_file_a) as csv_file_a:
		csv_reader = csv.DictReader(csv_file_a)

		total_a = []
		total_number_a = 0

		for row in csv_reader:

			found = False

			for subject in total_a:
				if row['subjectID'] == subject['subjectID']:
					total_number_a += int(row['phubbsWhileSession'])
					subject['numberOfUnlocks'] += int(row['phubbsWhileSession'])
					found = True
					break

			if not found:
				total_number_a += int(row['phubbsWhileSession'])
				total_a.append({
					'subjectID': row['subjectID'],
					'condition': 'A',
					'numberOfUnlocks': int(row['phubbsWhileSession'])
				})

	# data of condition b (with intervention)
	with open(input_file_b) as csv_file_b:
		csv_reader = csv.DictReader(csv_file_b)

		total_b = []
		total_number_b = 0

		for row in csv_reader:

			found = False

			for subject in total_b:
				if row['subjectID'] == subject['subjectID']:
					total_number_b += int(row['phubbsWhileSession'])
					subject['numberOfUnlocks'] += int(row['phubbsWhileSession'])
					found = True
					break

			if not found:
				total_number_b += int(row['phubbsWhileSession'])
				total_b.append({
					'subjectID': row['subjectID'],
					'condition': 'B',
					'numberOfUnlocks': int(row['phubbsWhileSession'])
				})

	# save number of unlocks per person in extra csv file
	with open(output_file_csv, 'w', newline='') as csv_file_output:
		fieldnames = ['subjectID', 'condition', 'numberOfUnlocks']
		writer = csv.DictWriter(csv_file_output, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(total_a)
		writer.writerows(total_b)

	# extract only number of unlocks from both conditions to plot
	num_of_unlocks_a = [subject['numberOfUnlocks'] for subject in total_a]
	num_of_unlocks_b = [subject['numberOfUnlocks'] for subject in total_b]

	fig, ax = plt.subplots()

	ax.boxplot(num_of_unlocks_a, positions=[1], labels=[f'without intervention\ntotal: {total_number_a}'])
	ax.boxplot(num_of_unlocks_b, positions=[2], labels=[f'with intervention\ntotal: {total_number_b}'])

	ax.set_ylabel('number of unlocks')
	ax.set_title('total number of unlocks per person')

	plt.savefig(output_file_boxplot)

	plt.show()


boxplot_number_of_unlocks_per_person_comparison(csv_phubbsPerSession_a, csv_phubbsPerSession_b, 'number-of-unlocks-per-person-and-condition.csv', 'plot_II_a_b.png')