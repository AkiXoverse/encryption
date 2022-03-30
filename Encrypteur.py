#!/usr/bin/python3
from hashlib import sha256
from colorama import Fore, Back, Style
import os
import string
import random
import webbrowser
import os
import time
import json
import ctypes
import os.path

### Primary informations
software_name = "Akii File Encryptor"
version = "1.0"
creator = "Akii"
aki_ascii = """                                                                                                                                                                                                        
               AAA               kkkkkkkk             iiii    iiii  
              A:::A              k::::::k            i::::i  i::::i 
             A:::::A             k::::::k             iiii    iiii  
            A:::::::A            k::::::k                           
           A:::::::::A            k:::::k    kkkkkkkiiiiiii iiiiiii 
          A:::::A:::::A           k:::::k   k:::::k i:::::i i:::::i 
         A:::::A A:::::A          k:::::k  k:::::k   i::::i  i::::i 
        A:::::A   A:::::A         k:::::k k:::::k    i::::i  i::::i 
       A:::::A     A:::::A        k::::::k:::::k     i::::i  i::::i 
      A:::::AAAAAAAAA:::::A       k:::::::::::k      i::::i  i::::i 
     A:::::::::::::::::::::A      k:::::::::::k      i::::i  i::::i 
    A:::::AAAAAAAAAAAAA:::::A     k::::::k:::::k     i::::i  i::::i 
   A:::::A             A:::::A   k::::::k k:::::k   i::::::ii::::::i
  A:::::A               A:::::A  k::::::k  k:::::k  i::::::ii::::::i
 A:::::A                 A:::::A k::::::k   k:::::k i::::::ii::::::i
AAAAAAA                   AAAAAAAkkkkkkkk    kkkkkkkiiiiiiiiiiiiiiii                               
"""
choice_txt = """
1 - Launch the software
2 - Config.json
3 - Credit
4 - Exit
"""

# Config User
def config():
	print(Style.BRIGHT + Fore.BLUE + aki_ascii)
	print(Style.BRIGHT + Fore.BLUE + software_name + " | " + Fore.YELLOW +"Config Editor")
	config_file="config.json"
	if os.path.isfile(config_file):
		os.remove(config_file)
	
	print(Style.BRIGHT + Fore.BLUE + "Quel type d'extension voulez-vous que le logiciel détecte automatiquement ? :")
	extension_config = input(Style.BRIGHT + Fore.BLUE + "$ ")
	print(Style.BRIGHT + Fore.BLUE + "\nVoulez-vous que le logiciel fasse une backup automatique des mots de passe et fichier que vous avez encrypter ? :\n[1] Oui\n[2] Non")
	yesno_config = input(Style.BRIGHT + Fore.BLUE + "$ ")
	if yesno_config == "1":
		backup_choice = True
	if yesno_config == "2":
		backup_choice = False
	config_finale = {
	"extension" : extension_config,
	"backup" : backup_choice
	}

	json_object = json.dumps(config_finale, indent = 2)

	with open(config_file, 'w') as f:
		f.write(json_object)

	print(Style.BRIGHT + Fore.YELLOW + "config.json " + Fore.BLUE + "have been updated !")
	time.sleep(2.5)

# Clear console
def clearconsole():
	command = 'clear'
	if os.name in ('nt', 'dos'):
		command = 'cls'
	os.system(command)

# Actualise Config Data / Create a config
def actualise_data():
	if os.path.isfile('config.json'):
		with open('config.json') as f:
			config = json.load(f)
		global extension
		global backup
		extension = config.get('extension')
		backup = config.get('backup')
	else:
		clearconsole()
		print(Style.BRIGHT + Fore.BLUE + aki_ascii)
		print(Style.BRIGHT + Fore.YELLOW + "[Error] config.json | Un fichier source du logiciel n'a pas pu être chargé.\n[?] Une config prédéfinie sera chargée dans 3 secondes.")
		time.sleep(3)
		with open('config.json', 'w') as f:
			f.write(
        		"""
{
  "extension": "encrypted",
  "backup": true
}

        		""")

# Credit to Akii
def credit():
	print(Style.BRIGHT + Fore.BLUE + aki_ascii)
	print(Style.BRIGHT + Fore.YELLOW + "Le logiciel va ouvrir un lien dans votre navigateur internet, voulez-vous y accéder ?")
	print(Style.BRIGHT + Fore.YELLOW + "1 - Yes\n2 - No")
	yesno = input(Style.BRIGHT + Fore.BLUE + "\n$ ") 

	if yesno == "1":
		webbrowser.open('https://akii.fr')
		main()
	if yesno == "2":
		main()

# Primary part of the program (encryption)
def encryption():
	print(Style.BRIGHT + Fore.BLUE + aki_ascii)
	print(f"{Style.BRIGHT}{Fore.BLUE}Specific Extension used : " + '"' + extension + '"')
	print(f"{Style.BRIGHT}{Fore.BLUE}Backup Auto : {backup}")
	if os.path.exists("Files"):
		pass
	else:
		os.mkdir("Files")


	global entree
	entree = input(f"{Fore.WHITE}--[ Entrez le nom du fichier à encrypter/decrypter\n{Fore.RED}(ATTENTION, le fichier doit être dans le répertoire {Fore.YELLOW}Files{Fore.RED})\n{Fore.WHITE}$ ")
	global key
	key = input(f"\n{Fore.YELLOW}--[ Clé de déchiffrage : ")
	global sortie
	sortie = input(f"\n{Fore.YELLOW}--[ Quel nom voulez-vous attribuer à votre fichier final ? : ")
	print("\n\n")
	keys = sha256(key.encode('utf-8')).digest()

	with open("Files/" + entree,'rb') as f_entree:
		with open(sortie,'wb') as f_sortie:
			i = 0
			while f_entree.peek():
				c = ord(f_entree.read(1))
				j = i % len(keys)
				b = bytes([c^keys[j]])
				f_sortie.write(b)
				i = i + 1
	if backup:

		if os.path.exists("Backup"):
			pass
		else:
			os.mkdir("Backup")

		number = random.randint(1000, 100000)
		now = datetime.now()
		date = now.strftime("%d-%m")
		directory = f"backup/backup-{date}-{number}.txt"
		texte = (f"#############\nAuto data Backup of " + software_name + " :\n\nName of the origine file: " + entree + "\n\nName of the encrypted file: " + sortie + "\nEncryption Key (below):\n\n" + key + "\n#############")
		with open(directory, 'w') as f:
			f.write(texte)		
	
	main()

# Simple Main	
def main():
	actualise_data()
	actualise_data()
	clearconsole()
	if os.name in ('nt', 'dos'):
		ctypes.windll.kernel32.SetConsoleTitleW(f'{software_name} | {version}')
	print(Style.BRIGHT + Fore.BLUE + aki_ascii)
	print(Style.BRIGHT + Fore.BLUE + software_name)
	print(choice_txt)
	choice = input(Style.BRIGHT + Fore.BLUE + "$ ")
	try:
		if choice == "1":
			clearconsole()
			encryption()
		if choice == "2":
			clearconsole()
			config()
		if choice == "3":
			clearconsole()
			credit()
		if choice == "4":
			clearconsole()
			print(aki_ascii)
			print(Fore.RESET + "Merci d'avoir utilisé: " + Style.BRIGHT + Fore.BLUE + software_name + Fore.RESET)
			exit()
		main()
	except Exception as e:
		print(e)
		time.sleep(5)
		print("\n" + "[!] Si vous avez quelconque problème avec le logiciel veuillez contacter le créateur pour avoir de l'aide.")


main()