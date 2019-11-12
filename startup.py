from Crypto.Cipher import AES
from Crypto import Random
import struct
import os,random, sys,pkg_resources,hashlib,base64,pickle
from fastecdsa import curve, ecdsa, keys
from hashlib import sha256

h = hashlib.sha256()
#public_key = '(19555da0fb51dd36edcade3e134170acb7742dd6f856fad8bac00321dc993ab0,4fe2ae5605329d720ee9d0f89408d6d9640b8d6ebf623478d1c262cede18aba9)'
#r = 34816050205070856089875536106622690615783127090386058606998384559303067400962
#s =39027009987109652359683559993977226830867789347105460417532144103192298319409

#=====get the public key=====
my_file_pubKey = "Key/public_key"
with open(my_file_pubKey, 'rb') as pub:
    depickler = pickle.Unpickler(pub)
    public_key = depickler.load()

my_file_r = 'Key/rFile'
with open(my_file_r, 'rb') as rVariable:
    rDepickler = pickle.Unpickler(rVariable)
    r = rDepickler.load()

my_file_s = 'Key/sFile'
with open(my_file_s, 'rb') as sVariable:
    sDepickler = pickle.Unpickler(sVariable)
    s = sDepickler.load()



#=====Function hash with SHA256=====
def file_hash(filename):
  with open(filename, 'rb', buffering=0) as f:
    for b in iter(lambda : f.read(128*1024), b''):
      h.update(b)
  return h.hexdigest()


has_fichier = file_hash('program.py.enc')
#print(has_fichier)


#=====Function validSignature=====
def validSignature(hash):
    valid = ecdsa.verify((r, s), hash, public_key)
    return valid

elliptic_curve = validSignature(has_fichier)



#=====Function decrypt=====
def decrypt_file(key, in_filename, out_filename=None, chunksize=24 * 1024):

    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)



if(elliptic_curve== True):
    file_to_decrypt = 'program.py.enc'
    with open('Key/keyAES', 'rb') as keyAES:
        AESKey_depickler = pickle.Unpickler(keyAES)
        key = AESKey_depickler.load()
    decrypt_file(key,file_to_decrypt)
    print('program.py decrypted')
    os.system("python3 program.py -i ")
    os.remove("program.py")
