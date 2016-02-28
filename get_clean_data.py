# coding=utf8

import api_functions as af
import urllib
import xml.etree.ElementTree  as ET
import xmltodict, json
#from firebase import firebase
from firebase import Firebase #https://github.com/mikexstudios/python-firebase

#af.get_materias_from_list(af.pesquisa_materia({'palavraChave':'abacaxi'}))

#firebase = firebase.FirebaseApplication('https://maisbr.firebaseio.com', None)
#f = Firebase('https://maisbr.firebaseio.com/')

def get_nomes_metadata_atual():
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

	#firebase.post('/senadores', senadores_dict) # Substituir posteriormente por método genérico para salvar os dados

def get_votacoes_senador(codigo):
	# Salva votações do senador no banco de dados
	tree = af.votacoes_senador(codigo, {'ano':'2015	', 'sigla':'PEC'})
	votacoes_tree = tree.findall('.//Votacao')

	votos_dict = {}
	for vot in votacoes_tree:
		cod_materia = vot.find('.//CodigoMateria').text

		votos_dict[cod_materia] = {}
		votos_dict[cod_materia]['DescricaoVoto'] 		= vot.find('.//DescricaoVoto').text
		votos_dict[cod_materia]['DescricaoVotacao'] 	= vot.find('.//DescricaoVotacao').text
		votos_dict[cod_materia]['DescricaoResultado'] 	= vot.find('.//DescricaoResultado').text
		votos_dict[cod_materia]['AnoMateria'] 			= vot.find('.//AnoMateria').text
		votos_dict[cod_materia]['SiglaSubtipoMateria'] 	= vot.find('.//SiglaSubtipoMateria').text
	
	# Salva no Firebase
	url = '/senadores/-KBQF2qbolbf1W7N_6I8/' + codigo + '/votos/'
	f = Firebase('https://maisbr.firebaseio.com' + url)
	f.put(votos_dict)

	#firebase.post('/senadores', senadores_dict)

def get_materias_metadata_atual():
	# Definir quão atuais são as matérias (fetch by date, maybe? By number intrinsically is by date?)
	pass

def test_firebase():
	test_data = {'name':'cleibzon', 'materias':['a','b','c']}
	firebase.post('/test', test_data)





