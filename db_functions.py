# coding=utf8

#from firebase import firebase
from firebase import Firebase #https://github.com/mikexstudios/python-firebase
import requests


FBURL = 'https://maisbr.firebaseio.com';

def get_senadores_list():
	# Equivalente ao 'curl' para usar a opção shallow e só pegar as keys dos senadores
	r = requests.get('https://maisbr.firebaseio.com/senadores.json?shallow=True')
	senadores_dict = r.json()

	list = []
	for key, val in senadores_dict.iteritems():
		print 'Salvo senador:', key
		list.append(key)

	return sorted(list)
