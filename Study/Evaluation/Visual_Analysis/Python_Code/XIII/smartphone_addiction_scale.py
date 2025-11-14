import matplotlib.pyplot as plt
import csv
import os

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))

# path to csv in "Processed_Data"
csv_survey = os.path.join(current_directory, '..', 'Processed_Data', 'final_survey_values.csv')

# SM := Smartphone Addiction Scale (likert: agree = 5, disagree = 1)
# best: 1 no addiction


def plot_addiction(input_file, output_file_boxplot):

	plot = []

	# without intervention
	with open(input_file) as csv_file:
		csv_reader = csv.DictReader(csv_file)

		for row in csv_reader:

			plot.append(float(row['sm_value']))

	fig, ax = plt.subplots(figsize=(6, 5))
	fig.subplots_adjust(top=0.85)
	plt.ylim([0, 5.5])

	fig.suptitle('(n) Smartphone Addiction Scale', fontweight= 'bold', fontsize=14)
	plt.ylabel('1 = not addicted - 5 = addicted')
	plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
	plt.boxplot(plot)

	plt.savefig(output_file_boxplot)

	plt.show()


plot_addiction(csv_survey, 'plot_XIII.png')