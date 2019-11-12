# Group9TP4
Pour le TP4 nous avons décidé d'utilsier Python 3.5.2
nous avons importer plusieur librairies:
  - pycrypto : 
      pour l'installer : pip3 install pycrypto
  - fastecdsa : ( pour elliptic curve)
      pour l'installer : pip3 install fastecdsa
  - websocket : 
      pour l'installer : pip3 install websocket-client
      
Pour executer notre programme il suffit de faire : python3 startup.py
Dans notre dossier nous avons un fichier cyrpt.py qui nous a permis de crypter et hasher nos fichier
Ensuite nous avons un dossier Key dans lequel nous avons notre clé publique de elliptic curve, ainsi que les clé nécesaire
pour valider une signature.
ENfin dans le Dossier File_to_use se sont nos fichier program.py et data.txt de base non encrypter, pour les récuperer en cas de problème
