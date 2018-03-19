#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
# ====================================================
# TITLE           : CryptoCurrency Prices
# DESCRIPTION     :
# - 1. Demande à l'utilisateur la crypto dont il veut le prix ou s'il veut
# 	la liste des cryptos disponibles.
# - 2. Cherche la liste des cryptos et les affiches.
# 	Ou cherche le prix via l'API de cryptocompare.com et l'affiche
# - 3. Retour au n°1
# AUTHORS		  : Guillaume HANOTEL
# DATE            : 19/03/2018
# ====================================================


from cryptocompy import coin
from cryptocompy import price
import os
import sys


def get_crypto_full_name(coins):
	list_names = []
	for key, value in coins.items():
		list_names.append(value.get('FullName'))
	return list_names


def get_crypto_name(coins):
	list_names = []
	for key, value in coins.items():
		list_names.append(value.get('CoinName'))
	return list_names


def find_key(d, value):
	for k,v in d.items():
		if isinstance(v, dict):
			p = find_key(v, value)
			if p:
				return [k] + p
		elif v == value:
			return [k]


def print_list(list):
	for row in list:
		print(row)


def clear():
	os.system('cls' if os.name == 'nt' else 'clear')


clear()
print("\t*****************************")
print("\t*\tCRYPTOCURRENCY\t    *")
print("\t*****************************")


cryptocurrencies = coin.get_coin_list(coins='all')
cryptocurrencies_names = get_crypto_name(cryptocurrencies)
cryptocurrencies_acronym = cryptocurrencies.keys()

input_cryptocurrency = ''

while input_cryptocurrency != 'exit':

	print("\n - Enter the name or acronym of the cryptocurrency you want")
	print("   (ex : 'BTC' or 'Bitcoin')")
	print(" - Enter 'list' to list cryptocurrency")
	print(" - Enter 'exit' to exit")

	input_cryptocurrency = input("> ")

	if input_cryptocurrency == 'list':
		cryptocurrencies_fullname = list(get_crypto_full_name(cryptocurrencies))
		print_list(cryptocurrencies_fullname)

	elif input_cryptocurrency == 'exit':
		pass

	else:

		# test si l'input (upper) est dans la liste des acronymes
		# ou si l'input est dans la liste des noms des cryptomonnaies
		if input_cryptocurrency.upper() in cryptocurrencies_acronym or input_cryptocurrency in cryptocurrencies_names:
			# si il a entré le nom complet, on le retransforme en acronyme
			if input_cryptocurrency in cryptocurrencies_names:
				input_cryptocurrency = find_key(cryptocurrencies, input_cryptocurrency)[0]

			# récupération des prix
			prices_crypto = price.get_current_price(input_cryptocurrency, ["EUR", "USD"], e='all', try_conversion=True, full=False, format='raw')

			prix_euro = prices_crypto.get(input_cryptocurrency).get('EUR')
			prix_dollar = prices_crypto.get(input_cryptocurrency).get('USD')

			print('\t1 ' + input_cryptocurrency + ' = ' + str(prix_euro) + '€')
			print('\t1 ' + input_cryptocurrency + ' = ' + str(prix_dollar) + '$')
			print("\n")

		else:
			sys.stderr.write("Error : Undefined CryptoCurrency")
			sys.exit(1)


