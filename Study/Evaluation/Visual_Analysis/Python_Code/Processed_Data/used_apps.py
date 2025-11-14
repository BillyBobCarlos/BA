import csv
import os

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))

# path to csv in "Raw_Data"
csv_phone_use = os.path.join(current_directory, '..', 'Raw_Data', 'phone-use.csv')
csv_phone_use_a = os.path.join(current_directory, '..', 'Raw_Data', 'phone-use-a.csv')
csv_phone_use_b = os.path.join(current_directory, '..', 'Raw_Data', 'phone-use-b.csv')

# listed apps that where used while phone-use in social interaction
# ranked by frequency

# csv/-filter:
## condition a: phone-use-a.csv
## condition b: phone-use-b.csv
## both: phone-use

def save_appnames_with_frequency(input_file, output_file):
	try:
		counted_apps = []
		subjects_with_accessibility_service = ['uj20', 'Ss26', 'HJ42', 'LJ16', 'Mu06', 'Mv18', 'sm07', 'ej15']

		with open(input_file, 'r') as csvfile_interaction:
			reader = csv.DictReader(csvfile_interaction)

			for row in reader:
				if row['subjectID'] in subjects_with_accessibility_service:
					apps_used_str = row['appsUsed']

					cleaned_list = apps_used_str[1:-1].split(', ')

					for item in cleaned_list:
						if item == '':
							item = 'null'
						found = False

						for app in counted_apps:
							if app['appID'] == item:
								app['frequency'] += 1
								found = True
								break

						if not found:
							counted_apps.append({
								'appID': item,
								'frequency': 1
							})

		sorted_counted_apps = sorted(counted_apps, key=lambda x: x['frequency'], reverse=True)
		
		fields = ['appID', 'frequency']
		with open(output_file, 'w', newline='') as csvfile_output:
			writer = csv.DictWriter(csvfile_output, fieldnames=fields)
			writer.writeheader()
			writer.writerows(sorted_counted_apps)

	except Exception as e:
		print(f"Error cleaning CSV file: {e}")


def process_appnames(input_file, output_file):
	try:
		processed = []
		delete = False

		# check for substrings and replace
		substr_messenger = ['whatsapp', 'messaging', 'telegramm', 'signal', 'securesms', 'Slack', 'mail', 'messenger']
		substr_socialmedia = ['insta', 'twitter', 'reddit', 'facebook']
		substr_entertainment = ['youtube', 'quizduel', 'com.onemt.and.kc', 'chess', 'skatpalast']
		substr_browser = ['search', 'ecosia', 'chrome']
		#substr_input = ['inputmethod', 'lge.ime', 'honeyboard', 'swiftkey', 'intelligent']
		substr_calls = ['dialer', 'contact']
		substr_music = ['spotify', 'swr1bwradio']
		substr_pay = ['paypal', 'banking']
		substr_organization = ['pixelhouse', 'ebay', 'cineplex', 'calendar', 'reminder', 'de.hafas.android.db', 'VVSMobil', 'DINGCompanion', 'bring', 'spond']
		substr_tools = ['gallery', 'camera', 'maps', 'calculator', 'setting', 'vending', 'clockpackage', 'photos', 
		'docs', 'screenshot', 'android.video', 'android.apps.nbu.files', 'galaxyfinder', 'myfiles']
		substr_health = ['freestylelibre3']
		substr_sport = ['hudl', 'komoot']

		substr_delete = ['incallui', 'permissioncontroller', 'smartcapture', 'aodservice', 'lool', 'ledcover', 'services', 'com.android.phone', 'daemonapp', 'qmemoplus',
		'inputmethod', 'lge.ime', 'honeyboard', 'swiftkey', 'intelligent']
		substr_null = ['null']


		with open(input_file, 'r') as csvfile_appnames:
			reader = csv.DictReader(csvfile_appnames)

			for row in reader:
				app_name = row['appID']

				# messengers
				for substr in substr_messenger:
					if substr in app_name:
						app_name = 'messengers'
				# social media
				for substr in substr_socialmedia:
					if substr in app_name:
						app_name = 'social\nmedia'
				# entertainment
				for substr in substr_entertainment:
					if substr in app_name:
						app_name = 'entertainment'
				# internet explorers
				for substr in substr_browser:
					if substr in app_name:
						app_name = 'internet explorer'
				# calls
				for substr in substr_calls:
					if substr in app_name:
						app_name = 'calls'
				# input
				#for substr in substr_input:
				#	if substr in app_name:
				#		app_name = 'keyboard\ninput'
				# music
				for substr in substr_music:
					if substr in app_name:
						app_name = 'music'
				# payment
				for substr in substr_pay:
					if substr in app_name:
						app_name = 'payment'
				# smartphone tools
				for substr in substr_tools:
					if substr in app_name:
						app_name = 'smartphone\ntools'
				# organization tools
				for substr in substr_organization:
					if substr in app_name:
						app_name = 'organization\ntools'
				# health
				for substr in substr_health:
					if substr in app_name:
						app_name = 'health'
				# sports
				for substr in substr_sport:
					if substr in app_name:
						app_name = 'sports'
				# only unlocked
				for substr in substr_null:
					if substr in app_name:
						app_name = 'only\nunlocked'


				# delete
				for substr in substr_delete:
					if substr in app_name:
						delete = True


				if not delete:
					found = False
					for app in processed:
						if app['appname'] == app_name:
							app['frequency'] += int(row['frequency'])
							found = True
							break

					if not found:
						processed.append({
							'appname': app_name,
							'frequency': int(row['frequency'])
						})

				delete = False
				found = False

		sorted_processed = sorted(processed, key=lambda x: x['frequency'], reverse=True)

		fields = ['appname', 'frequency']
		with open(output_file, 'w', newline='') as csvfile_output:
			writer = csv.DictWriter(csvfile_output, fieldnames=fields)
			writer.writeheader()
			writer.writerows(sorted_processed)

	except Exception as e:
		print(f"Error cleaning CSV file: {e}")


# first sort by frequency and id
#save_appnames_with_frequency(csv_phone_use, 'used-apps-frequency.csv')
#save_appnames_with_frequency(csv_phone_use_a, 'used-apps-frequency-a.csv')
#save_appnames_with_frequency(csv_phone_use_b, 'used-apps-frequency-b.csv')
# then sort by category and frequency
process_appnames('used-apps-frequency.csv', 'processed-app-frequency.csv')
process_appnames('used-apps-frequency-a.csv', 'processed-app-frequency-a.csv')
process_appnames('used-apps-frequency-b.csv', 'processed-app-frequency-b.csv')