import api_functions as af
import urllib
import xml.etree.ElementTree  as ET
import xmltodict, json
from firebase import firebase

#af.get_materias_from_list(af.pesquisa_materia({'palavraChave':'abacaxi'}))

firebase = firebase.FirebaseApplication('https://maisbr.firebaseio.com', None)

def get_nomes_codigos_atual():
	# Gets attributes from parlamentares and saves into Firebase 
	# --> still needs to put right below 'senadores URL', now it's using FB id there...

	url = 'http://legis.senado.gov.br/dadosabertos/senador/lista/atual'
	uh = urllib.urlopen(url)
	data = uh.read()
	tree = ET.fromstring(data)
	senadores_tree = tree.findall('.//IdentificacaoParlamentar')
	
	senadores_dict = {}
	for sen in senadores_tree:
		
		codigo = sen.find('CodigoParlamentar').text
		
		# creates object with id 'codigo' and all data nested into that
		senadores_dict[codigo] = {}
		senadores_dict[codigo]['NomeParlamentar'] 			= sen.find('NomeParlamentar').text
		senadores_dict[codigo]['SexoParlamentar'] 			= sen.find('SexoParlamentar').text
		senadores_dict[codigo]['FormaTratamento'] 			= sen.find('FormaTratamento').text
		senadores_dict[codigo]['UrlPaginaParlamentar']		= sen.find('UrlPaginaParlamentar').text
		senadores_dict[codigo]['UrlFotoParlamentar']		= sen.find('UrlFotoParlamentar').text
		senadores_dict[codigo]['EmailParlamentar'] 			= sen.find('EmailParlamentar').text
		senadores_dict[codigo]['SiglaPartidoParlamentar'] 	= sen.find('SiglaPartidoParlamentar').text
		senadores_dict[codigo]['UfParlamentar'] 			= sen.find('UfParlamentar').text

	for codigo, senador in senadores_dict.iteritems():
		print codigo, senador['EmailParlamentar']
		#print '---------'

	result = firebase.post('/senadores', senadores_dict)
	print result
		
