import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import ast
import csv
import os

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))

# path to csv in "Processed_Data"
csv_phubbsPerSession_a = os.path.join(current_directory, '..', 'Processed_Data', 'phubbs-per-session-a.csv')
csv_phubbsPerSession_b = os.path.join(current_directory, '..', 'Processed_Data', 'phubbs-per-session-b.csv')


# print boxplot for duration of phubbs total of all subjects (without any relation)
# print boxplot for average duration of phubbs per subject (without any relation)
## comparison between condition a (without intervention) & condition b (with intervention)

## INPUT:	phubbs-per-session-a.csv
## 			phubbs-per-session-b.csv

## OUTPUT:	duration-of-unlocks-per-person-and-condition.csv
##			plot_I_a_b.png

def boxplot_total_duration_of_unlocks_comparison(input_file_a, input_file_b, output_file_boxplot):

	plt.style.use('fast')

	time_format = '%H:%M:%S'

	# data of condition a (without intervention)
	with open(input_file_a) as csv_file_a:
		csv_reader = csv.DictReader(csv_file_a)

		durations_a = []

		for row in csv_reader:

			raw_string = row['phubbs']
			ast_list = ast.literal_eval(raw_string)

			duration_list = [timedelta(hours=int(t.split(':')[0]), minutes=int(t.split(':')[1]), seconds=int(t.split(':')[2])) for t in ast_list]

			for duration in duration_list:
				durations_a.append(duration.total_seconds() / 60)

	# data of condition b (with intervention)
	with open(input_file_b) as csv_file_b:
		csv_reader = csv.DictReader(csv_file_b)

		durations_b = []

		for row in csv_reader:

			raw_string = row['phubbs']
			ast_list = ast.literal_eval(raw_string)

			duration_list = [timedelta(hours=int(t.split(':')[0]), minutes=int(t.split(':')[1]), seconds=int(t.split(':')[2])) for t in ast_list]

			for duration in duration_list:
				durations_b.append(duration.total_seconds() / 60)

	fig, ax = plt.subplots(figsize=(6, 5))
	fig.subplots_adjust(top=0.85)

	ax.boxplot(durations_a, positions=[1], labels=['without intervention (A)'])
	ax.boxplot(durations_b, positions=[2], labels=['with intervention (B)'])

	ax.set_ylabel('duration in minutes')
	ax.set_title('(a) Total Duration of Phone Uses\nwhile Social Interactions', fontweight= 'bold', fontsize=14)

	plt.savefig(output_file_boxplot)

	plt.show()


def boxplot_avg_duration_per_person_of_unlocks_comparison(input_file_a, input_file_b, output_file_boxplot):

	plt.style.use('fast')

	time_format = '%H:%M:%S'

	# data of condition a (without intervention)
	with open(input_file_a) as csv_file_a:
		csv_reader = csv.DictReader(csv_file_a)

		durations_a = []

		for row in csv_reader:

			total_duration_of_subject = 0

			raw_string = row['phubbs']
			ast_list = ast.literal_eval(raw_string)
			duration_list = [timedelta(hours=int(t.split(':')[0]), minutes=int(t.split(':')[1]), seconds=int(t.split(':')[2])) for t in ast_list]

			for duration in duration_list:
				total_duration_of_subject += (duration.total_seconds())

			found = False

			for subject in durations_a:
				if row['subjectID'] == subject['subjectID']:
					subject['numberOfUnlocks'] += int(row['phubbsWhileSession'])
					subject['totaldurations'] += total_duration_of_subject
					found = True
					break

			if not found:
				durations_a.append({
					'subjectID': row['subjectID'],
					'numberOfUnlocks': int(row['phubbsWhileSession']),
					'totaldurations': total_duration_of_subject
				})

	# data of condition b (with intervention)
	with open(input_file_b) as csv_file_b:
		csv_reader = csv.DictReader(csv_file_b)

		durations_b = []

		for row in csv_reader:

			total_duration_of_subject = 0

			raw_string = row['phubbs']
			ast_list = ast.literal_eval(raw_string)
			duration_list = [timedelta(hours=int(t.split(':')[0]), minutes=int(t.split(':')[1]), seconds=int(t.split(':')[2])) for t in ast_list]

			for duration in duration_list:
				total_duration_of_subject += (duration.total_seconds())

			found = False

			for subject in durations_b:
				if row['subjectID'] == subject['subjectID']:
					subject['numberOfUnlocks'] += int(row['phubbsWhileSession'])
					subject['totaldurations'] += total_duration_of_subject
					found = True
					break

			if not found:
				durations_b.append({
					'subjectID': row['subjectID'],
					'numberOfUnlocks': int(row['phubbsWhileSession']),
					'totaldurations': total_duration_of_subject
				})


	avg_durations_a = [round(((subject['totaldurations']/subject['numberOfUnlocks']) / 60), 2) for subject in durations_a if subject['numberOfUnlocks'] != 0]
	avg_durations_b = [round(((subject['totaldurations']/subject['numberOfUnlocks']) / 60), 2) for subject in durations_b if subject['numberOfUnlocks'] != 0]

	#avg_durations_a = [round(((subject['totaldurations']/subject['numberOfUnlocks']) / 60), 2) for subject in durations_a]
	#avg_durations_b = [round(((subject['totaldurations']/subject['numberOfUnlocks']) / 60), 2) for subject in durations_b]

	fig, ax = plt.subplots(figsize=(6, 5))
	fig.subplots_adjust(top=0.85)


	ax.boxplot(avg_durations_a, positions=[1], labels=['without intervention (A)'])
	ax.boxplot(avg_durations_b, positions=[2], labels=['with intervention (B)'])

	ax.set_ylabel('duration in minutes')
	ax.set_title('(b) Average Duration of Phone Uses\nwhile Social Interactions per Person', fontweight= 'bold', fontsize=14)

	plt.savefig(output_file_boxplot)

	plt.show()


# plot average duration per subject
boxplot_avg_duration_per_person_of_unlocks_comparison(csv_phubbsPerSession_a, csv_phubbsPerSession_b, 'plot_I_avg_a_b.png')

# plot total duration of all subjects
boxplot_total_duration_of_unlocks_comparison(csv_phubbsPerSession_a, csv_phubbsPerSession_b, 'plot_I_a_b.png')