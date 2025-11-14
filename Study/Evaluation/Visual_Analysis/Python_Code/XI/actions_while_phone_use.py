import csv
from matplotlib import pyplot as plt
import os

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))

# path to csv in "Raw_Data"
csv_survey_results = os.path.join(current_directory, '..', 'Raw_Data', 'results-survey.csv')

def csi_values_list(input_file, output_file_csi):
	try:

		survey_values_csi = []

		with open(input_file, 'r') as csvfile_input:
			reader = csv.DictReader(csvfile_input)

			for row in reader:
				subjectID = row['G00001']
				condition = row['G00002']
				sessionID = row['G00003']
				csi = row['CSI']

				survey_values_csi.append({
					'subjectID': subjectID,
					'condition': condition,
					'sessionID': sessionID, 
					'csi': csi
				})

		fields = ['subjectID', 'condition', 'sessionID', 'csi']
		with open(output_file_csi, 'w', newline='') as csvfile_output:
			writer = csv.DictWriter(csvfile_output, fieldnames=fields)
			writer.writeheader()
			writer.writerows(survey_values_csi)

	except Exception as e:
		print(f"Error cleaning CSV file: {e}")

def process_context_of_use(input_file, output_file):
	try:
		processed = []
		delete = False

		# check for substrings and replace
		substr_eating = ['breakfast', 'Breakfast', 'dinner', 'Dinner', 'lunch', 'Lunch', 'Mittagessen', 'Essen', 'Coffee', 'Breakfasr', 'Eat', 'eating']
		substr_activity = ['Game night', 'Movie night', 'Party', 'going out', 'Cooking', 'kitchen', 'Shopping', 'recipe']
		substr_chill = ['chill', 'Chill', 'Sitting']
		substr_talking = ['talk', 'meet', 'speak', 'chatting', 'Planing', 'Talking', 'chat']
		substr_work = ['work', 'Work', 'learn', 'Learn', 'Study', 'Private office']

		substr_delete = ['Jj']


		with open(input_file, 'r') as csvfile_input:
			reader = csv.DictReader(csvfile_input)

			for row in reader:
				context = row['csi']
				context_conret = context

				# eating
				for substr in substr_eating:
					if substr in context:
						context = 'eating or coffeeing\ntogether'
				# chilling
				for substr in substr_chill:
					if substr in context:
						context = 'chilling\ntogether'
				# activities
				for substr in substr_activity:
					if substr in context:
						context = 'doing activities\ntogether'
				# talking
				for substr in substr_talking:
					if substr in context:
						context = 'talk to\neach other'
				# working
				for substr in substr_work:
					if substr in context:
						context = 'working or studying\ntogether'


				# delete
				for substr in substr_delete:
					if substr in context:
						delete = True

				found = False
				if not delete:
					for csi_name in processed:
						if csi_name['csi_name'] == context:
							csi_name['frequency'] += 1
							csi_name['contents'].append(context_conret)
							found = True
							break

					if not found:
						processed.append({
							'csi_name': context,
							'frequency': 1,
							'contents': [context_conret]
						})

				delete = False

		sorted_processed = sorted(processed, key=lambda x: x['frequency'], reverse=True)

		fields = ['csi_name', 'frequency', 'contents']
		with open(output_file, 'w', newline='') as csvfile_output:
			writer = csv.DictWriter(csvfile_output, fieldnames=fields)
			writer.writeheader()
			writer.writerows(sorted_processed)

	except Exception as e:
		print(f"Error cleaning CSV file: {e}")

def print_chart(input_file, output_file, title, output_csv):

	# style of plot
	plt.style.use('fast')

	context_names = []
	frequencies = []
	proportion = []
	proportion_round = []
	total = 0

	with open(input_file) as csv_file:
		csv_reader = csv.DictReader(csv_file)

		for row in csv_reader:
			csi = row['csi_name']
			frequency = int(row['frequency'])
			total += frequency
			context_names.append(csi)
			frequencies.append(frequency)

		for fre in frequencies:
			proportion.append((fre*100)/total)
			proportion_round.append(int((fre*100)/total))

	fig, ax = plt.subplots(figsize=(6, 5))
	fig.subplots_adjust(top=0.85)
	fig.subplots_adjust(bottom=0.25)

	bars = ax.bar(context_names, proportion, color='skyblue')
	# Annotate the average values on the bars
	for i, perc in enumerate(proportion_round):
		ax.text(i, proportion_round[i], f'{perc}%', ha='center', va='bottom', color='black')

	plt.bar(context_names, proportion)
	plt.xticks(rotation=45, ha="right")	
	plt.ylabel('frequency of activities')
	plt.ylim([0, 100])

	fig.suptitle(title, fontweight= 'bold', fontsize=14)

	# save plot
	plt.savefig(output_file)

	plt.show()

	with open(output_csv, mode='w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(['activity', 'frequency'])
		for i, context_name in enumerate(context_names):
			writer.writerow([context_name, proportion[i]])



csi_values_list(csv_survey_results, 'survey_values_csi.csv')
process_context_of_use('survey_values_csi.csv', 'csi.csv')
print_chart('csi.csv', 'plot_XI.png', '(g) Frequency of the Types of\nSocial Interactions (Activities)\nwhile Using Phone', 'plot_XI_percents.csv')
