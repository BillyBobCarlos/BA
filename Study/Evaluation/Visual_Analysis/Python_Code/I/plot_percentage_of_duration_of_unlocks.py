import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
import ast
import csv
import os

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))

# path to csv in "Processed_Data"
csv_phubbsPerSession_a = os.path.join(current_directory, '..', 'Processed_Data', 'phubbs-per-session-a.csv')
csv_phubbsPerSession_b = os.path.join(current_directory, '..', 'Processed_Data', 'phubbs-per-session-b.csv')

def boxplot_unlocks_comparison(input_file_a, input_file_b, output_file_duration, output_csv_a, output_csv_b):

	plt.style.use('fast')

	time_format = '%H:%M:%S'

	# data of condition a (without intervention)
	with open(input_file_a) as csv_file_a:
		csv_reader = csv.DictReader(csv_file_a)

		durations_a = []
		number_of_phubbs_while_studymode_a = 0

		for row in csv_reader:

			raw_string = row['phubbs']
			ast_list = ast.literal_eval(raw_string)

			duration_list = [timedelta(hours=int(t.split(':')[0]), minutes=int(t.split(':')[1]), seconds=int(t.split(':')[2])) for t in ast_list]

			for duration in duration_list:
				#durations_a.append(round((duration.total_seconds() / 60), 2))
				durations_a.append(duration.total_seconds())

		number_of_phubbs_while_studymode_a = len(durations_a)

	# 0-15 sec -> I
	# 15-30 sec -> II
	# 30-60 sec -> III
	# 1-5 min -> IV
	# > 5 min -> V
	durations_I = []
	durations_II = []
	durations_III = []
	durations_IV = []
	durations_V = []

	for duration in durations_a:
		if duration <= 15:
			durations_I.append(duration)
		elif duration <= 30:
			durations_II.append(duration)
		elif duration <= 60:
			durations_III.append(duration)
		elif duration <= 300:
			durations_IV.append(duration)
		else:
			durations_V.append(duration)

	std_I = np.std(durations_I)
	m_I = np.mean(np.array(durations_I))
	std_II = np.std(durations_II)
	m_II = np.mean(np.array(durations_II))
	std_III = np.std(durations_III)
	m_III = np.mean(np.array(durations_III))
	std_IV = np.std(durations_IV)
	m_IV = np.mean(np.array(durations_IV))
	std_V = np.std(durations_V)
	m_V = np.mean(np.array(durations_V))
	print("a I:   " + str(std_I) + " " + str(m_I))
	print("a II:  " + str(std_II) + " " + str(m_II))
	print("a III: " + str(std_III) + " " + str(m_III))
	print("a IV:  " + str(std_IV) + " " + str(m_IV))
	print("a V:   " + str(std_V) + " " + str(m_V))

	percent_usage_I_a = ((len(durations_I)*100)/number_of_phubbs_while_studymode_a)
	percent_usage_II_a = ((len(durations_II)*100)/number_of_phubbs_while_studymode_a)
	percent_usage_III_a = ((len(durations_III)*100)/number_of_phubbs_while_studymode_a)
	percent_usage_IV_a = ((len(durations_IV)*100)/number_of_phubbs_while_studymode_a)
	percent_usage_V_a = ((len(durations_V)*100)/number_of_phubbs_while_studymode_a)

	# data of condition b (with intervention)
	with open(input_file_b) as csv_file_b:
		csv_reader = csv.DictReader(csv_file_b)

		durations_b = []
		number_of_phubbs_while_studymode_b = 0

		for row in csv_reader:

			raw_string = row['phubbs']
			ast_list = ast.literal_eval(raw_string)

			duration_list = [timedelta(hours=int(t.split(':')[0]), minutes=int(t.split(':')[1]), seconds=int(t.split(':')[2])) for t in ast_list]

			for duration in duration_list:
				durations_b.append(duration.total_seconds())

		number_of_phubbs_while_studymode_b = len(durations_b)

	# 0-15 sec -> I
	# 15-30 sec -> II
	# 30-60 sec -> III
	# 1-5 min -> IV
	# > 5 min -> V
	durations_I = []
	durations_II = []
	durations_III = []
	durations_IV = []
	durations_V = []

	for duration in durations_b:
		if duration <= 15:
			durations_I.append(duration)
		elif duration <= 30:
			durations_II.append(duration)
		elif duration <= 60:
			durations_III.append(duration)
		elif duration <= 300:
			durations_IV.append(duration)
		else:
			durations_V.append(duration)

	std_I = np.std(durations_I)
	m_I = np.mean(np.array(durations_I))
	std_II = np.std(durations_II)
	m_III = np.mean(np.array(durations_II))
	std_III = np.std(durations_III)
	m_III = np.mean(np.array(durations_III))
	std_IV = np.std(durations_IV)
	m_IV = np.mean(np.array(durations_IV))
	std_V = np.std(durations_V)
	m_V = np.mean(np.array(durations_V))
	print("b I:   " + str(std_I) + " " + str(m_I))
	print("b II:  " + str(std_II) + " " + str(m_II))
	print("b III: " + str(std_III) + " " + str(m_III))
	print("b IV:  " + str(std_IV) + " " + str(m_IV))
	print("b V:   " + str(std_V) + " " + str(m_V))

	percent_usage_I_b = ((len(durations_I)*100)/number_of_phubbs_while_studymode_b)
	percent_usage_II_b = ((len(durations_II)*100)/number_of_phubbs_while_studymode_b)
	percent_usage_III_b = ((len(durations_III)*100)/number_of_phubbs_while_studymode_b)
	percent_usage_IV_b = ((len(durations_IV)*100)/number_of_phubbs_while_studymode_b)
	percent_usage_V_b = ((len(durations_V)*100)/number_of_phubbs_while_studymode_b)


	percents_of_durations_a = []
	percents_of_durations_a.append(percent_usage_I_a)
	percents_of_durations_a.append(percent_usage_II_a)
	percents_of_durations_a.append(percent_usage_III_a)
	percents_of_durations_a.append(percent_usage_IV_a)
	percents_of_durations_a.append(percent_usage_V_a)

	percents_of_durations_b = []
	percents_of_durations_b.append(percent_usage_I_b)
	percents_of_durations_b.append(percent_usage_II_b)
	percents_of_durations_b.append(percent_usage_III_b)
	percents_of_durations_b.append(percent_usage_IV_b)
	percents_of_durations_b.append(percent_usage_V_b)

	with open(output_csv_a, mode='w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(['Duration Range', 'Group A (%)'])
		for i, duration in enumerate(['0-15 sec', '15-30 sec', '30-60 sec', '1-5 min', '5+ min']):
			writer.writerow([duration, percents_of_durations_a[i]])

	with open(output_csv_b, mode='w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(['Duration Range', 'Group B (%)'])
		for i, duration in enumerate(['0-15 sec', '15-30 sec', '30-60 sec', '1-5 min', '5+ min']):
			writer.writerow([duration, percents_of_durations_b[i]])

	fig, ax = plt.subplots(1, 2, figsize=(10, 5)) 
	fig.subplots_adjust(top=0.8)
	fig.subplots_adjust(bottom=0.2)

	percents = ['0-15\nsec', '15-30\nsec', '30-60\nsec', '1-5\nmin', '5+\nmin']
	x = np.arange(len(percents))  # Positions for bars
	width = 0.5  # Width of each bar

	ax[0].bar(x, percents_of_durations_a, width, label='Group A')
	ax[0].set_ylabel('percentage of the number of unlocks in each study mode')
	ax[0].set_title('without interventions (A)')
	ax[0].set_xticks(x)
	ax[0].set_xticklabels(percents)
	ax[0].set_ylim([0, 100])

	ax[1].bar(x, percents_of_durations_b, width, label='Group B')
	ax[1].set_title('with interventions (B)')
	ax[1].set_xticks(x)
	ax[1].set_xticklabels(percents)
	ax[1].set_ylim([0, 100])

	ax[0].text(0, 80, f'total number of unlocks\nin study mode a: {number_of_phubbs_while_studymode_a}', fontsize=10, color='gray')
	ax[1].text(0, 80, f'total number of unlocks\nin study mode b: {number_of_phubbs_while_studymode_b}', fontsize=10, color='gray')

	fig.suptitle("(e) Percentage Duration of Phone Uses\nwhile Social Interactions", fontweight= 'bold', fontsize=14)

	plt.savefig(output_file_duration)

	plt.show()



boxplot_unlocks_comparison(csv_phubbsPerSession_a, csv_phubbsPerSession_b, 'plot_0_a_b.png', 'average_duration_a.csv', 'average_duration_b.csv')