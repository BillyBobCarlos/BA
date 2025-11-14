import csv
from matplotlib import pyplot as plt
import os
import numpy as np


# Get the current directory
current_directory = os.path.dirname(os.path.realpath(__file__))

# Path to the CSV file in directory "Processed_Data"
csv_processed_app_frequency = os.path.join(current_directory, '..', 'Processed_Data', 'processed-app-frequency.csv')
csv_processed_app_frequency_a = os.path.join(current_directory, '..', 'Processed_Data', 'processed-app-frequency-a.csv')
csv_processed_app_frequency_b = os.path.join(current_directory, '..', 'Processed_Data', 'processed-app-frequency-b.csv')


def print_chart(input_file_a, input_file_b, output_file):

	# style of plot
	plt.style.use('fast')

	apps_a = []
	app_names_a = []
	proportion_a = []
	total_a = 0

	apps_b = []
	app_names_b = []
	proportion_b = []
	total_b = 0

	with open(input_file_a) as csv_file:
		csv_reader = csv.DictReader(csv_file)

		for row in csv_reader:
			total_a += int(row['frequency'])
			apps_a.append({
				'app_name': row['appname'],
				'frequency': int(row['frequency'])
				})

		for app in apps_a:
			if int((app['frequency']*100)/total_a) > 0:
				proportion_a.append(int((app['frequency']*100)/total_a))
				app_names_a.append(app['app_name'])

	with open(input_file_b) as csv_file:
		csv_reader = csv.DictReader(csv_file)

		for row in csv_reader:
			total_b += int(row['frequency'])
			apps_b.append({
				'app_name': row['appname'],
				'frequency': int(row['frequency'])
				})

		for app in apps_b:
			if int((app['frequency']*100)/total_b) > 0:
				proportion_b.append(int((app['frequency']*100)/total_b))
				app_names_b.append(app['app_name'])

	fig, ax = plt.subplots(1, 2, figsize=(10, 5))

	x_a = np.arange(len(app_names_a)) 
	x_b = np.arange(len(app_names_b)) 
	width = 0.8

	for i, perc in enumerate(proportion_a):
		ax[0].text(i, proportion_a[i], f'{perc}%', ha='center', va='bottom', color='black')

	for i, perc in enumerate(proportion_b):
		ax[1].text(i, proportion_b[i], f'{perc}%', ha='center', va='bottom', color='black')

	ax[0].bar(x_a, proportion_a, width)
	ax[0].set_xticks(x_a)
	ax[0].set_xticklabels(app_names_a, rotation=45, ha="right")
	ax[0].set_ylabel('frequency of apps used')
	ax[0].set_title('without interventions (A)', style='normal')
	ax[0].set_ylim([0, 100])

	ax[1].bar(x_b, proportion_b, width)
	ax[1].set_xticks(x_b)
	ax[1].set_xticklabels(app_names_b, rotation=45, ha="right")
	ax[1].set_title('with interventions (B)', style='normal')
	ax[1].set_ylim([0, 100])

	ax[0].text(0, 80, f'total number of used apps\nin study mode a: {total_a}', fontsize=10, color='gray')
	ax[1].text(0, 80, f'total number of used apps\nin study mode b: {total_b}', fontsize=10, color='gray')

	fig.suptitle("(f) Frequency of Apps Used while Social Interactions", fontweight= 'bold', fontsize=14)

	fig.subplots_adjust(top=0.85)
	fig.subplots_adjust(bottom=0.25)

	plt.savefig(output_file)

	plt.show()


print_chart(csv_processed_app_frequency_a, csv_processed_app_frequency_b, 'plot_V_a_b.png')