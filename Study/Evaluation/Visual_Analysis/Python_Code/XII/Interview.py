import matplotlib.pyplot as plt  
import csv

def process_tags(input_file):
	try:
		with open(input_file, 'r') as csvfile:
			reader = csv.DictReader(csvfile)

			tags = []
			tags_sorted = []

			for row in reader:

				tags.append({
					'group': row['Group'],
					'tag': row['ï»¿Title']
					})

			tags_sorted = sorted(tags, key=lambda x: x['group'])

		first = True

		for row in tags_sorted:

			if first:
				group_last = row['group']
				new = []
				first = False

			if row['group'] != group_last:

				csv_name = group_last + '.csv'
				with open(csv_name, 'w', newline='') as csvfile:
					fieldnames = ['tag']
					writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

					writer.writeheader()
					writer.writerows(new)

				group_last = row['group']
				new = []

			new.append({
					'tag': row['tag']
				})

			if row['group'] == group_last:

				csv_name = group_last + '.csv'
				with open(csv_name, 'w', newline='') as csvfile:
					fieldnames = ['tag']
					writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

					writer.writeheader()
					writer.writerows(new)


	except Exception as e:
		print(f"Error cleaning CSV file: {e}")

process_tags('tags.csv')
