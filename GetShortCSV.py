
DATA_PATH = "D:\\Data Science\\GBIF Data\\0004762-171124123535762\\birbs.csv"
LINE_COUNT = 120000
OUTPUT_PATH = 'birbdata_short.csv'

with open(DATA_PATH) as birbdata:
	# write the first LINE_COUNT lines to another file
	with open(OUTPUT_PATH, 'w') as birbdata_short:
		for x in range(LINE_COUNT):
			try:
				birbdata_short.write(next(birbdata).replace('\t', ','))
			except Exception as ex:
				print('Error while reading line:')
				print(ex)

