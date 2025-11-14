import matplotlib.pyplot as plt
import csv
import os

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))

# path to csv in "Processed_Data"
csv_survey_a = os.path.join(current_directory, '..', 'Processed_Data', 'survey_values_a.csv')
csv_survey_b = os.path.join(current_directory, '..', 'Processed_Data', 'survey_values_b.csv')


def plot_reactance(input_file_a, input_file_b, output_file_boxplot):

	total_a = []
	total_b = []

	# without intervention
	with open(input_file_a) as csv_file_a:
		csv_reader_a = csv.DictReader(csv_file_a)

		for row in csv_reader_a:

			found = False

			for subject in total_a:
				if row['subjectID'] == subject['subjectID']:
					subject['totalReactance'] += float(row['rschi_value'])
					subject['sureveyCounter'] += 1
					found = True
					break

			if not found:
				total_a.append({
					'subjectID': row['subjectID'],
					'totalReactance': float(row['rschi_value']),
					'sureveyCounter': 1
				})

	# with intervention
	with open(input_file_b) as csv_file_b:
		csv_reader_b = csv.DictReader(csv_file_b)

		for row in csv_reader_b:

			found = False
			for subject in total_b:
				if row['subjectID'] == subject['subjectID']:
					subject['totalReactance'] += float(row['rschi_value'])
					subject['sureveyCounter'] += 1
					found = True
					break

			if not found:
				total_b.append({
					'subjectID': row['subjectID'],
					'totalReactance': float(row['rschi_value']),
					'sureveyCounter': 1
				})

	plot_a = [(subject['totalReactance']/subject['sureveyCounter']) for subject in total_a]
	plot_b = [(subject['totalReactance']/subject['sureveyCounter']) for subject in total_b]


	fig, ax = plt.subplots(figsize=(6, 5))
	fig.subplots_adjust(top=0.85)
	plt.ylim([0, 5.5])

	ax.boxplot(plot_a, positions=[1], labels=['without intervention (A)'])
	ax.boxplot(plot_b, positions=[2], labels=['with intervention (B)'])

	ax.set_ylabel('1 = aceptance - 5 = reactance')
	ax.set_title('(h) Reactance Scale\nfor Human Computer Interaction', fontweight= 'bold', fontsize=14)

	plt.savefig(output_file_boxplot)

	plt.show()

plot_reactance(csv_survey_a, csv_survey_b, 'plot_VI_a_b.png')
