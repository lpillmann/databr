import get_clean_data as cd

siglas = [	'PEC', 
			'PLS', 
			'PLC', 
			'PLN',
			'PLV', 
			'MPV', 
			'PRC', 
			'PRS', 
			'PDS'
		]

anos = ['2011', 
		'2012', 
		'2013', 
		'2014', 
		'2015', 
		'2016']

for s in siglas:
	for a in anos:
		cd.get_votos_senadores({'ano':a, 'sigla':s})