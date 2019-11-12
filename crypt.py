from Crypto.Cipher import AES
from Crypto import Random
import struct
import os,random, sys,pkg_resources,hashlib,base64,pickle
from fastecdsa import curve, ecdsa, keys
from hashlib import sha256


def encrypt_file(key, in_filename, out_filename=None, chunksize=64 * 1024):

    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = Random.new().read(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' '*(16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))


file_to_encrypt = 'program.py'
key = Random.get_random_bytes(32)
with open('Key/keyAES', 'wb') as keyAES:
    AESKey = pickle.Pickler(keyAES)
    AESKey.dump(key)
encrypt_file(key, file_to_encrypt, None)

file_data_to_encrypt = 'data.txt'
encrypt_file(key, file_data_to_encrypt , None)

os.remove("program.py")
os.remove("data.txt")

h = hashlib.sha256()

def file_hash(filename):
  with open(filename, 'rb', buffering=0) as f:
    for b in iter(lambda : f.read(128*1024), b''):
      h.update(b)
  return h.hexdigest()
file_to_hash=file_hash('program.py.enc')
file_data_to_hash = file_hash('data.txt.enc')
file_pubKey = "Key/public_key"


private_key = keys.gen_private_key(curve.P256)
public_key = keys.get_public_key(private_key, curve.P256)

with open(file_pubKey, 'wb') as pub:
    publicKey = pickle.Pickler(pub)
    publicKey.dump(public_key)
r, s = ecdsa.sign(file_to_hash, private_key)

with open('Key/rFile', 'wb') as rVariable:
    rPickle = pickle.Pickler(rVariable)
    rPickle.dump(r)

with open('Key/sFile', 'wb') as sVariable:
    sPickle = pickle.Pickler(sVariable)
    sPickle.dump(s)

rData, sData = ecdsa.sign(file_data_to_hash, private_key)

valid = ecdsa.verify((rData, sData), file_data_to_hash, public_key)
with open('Key/rFileData', 'wb') as rDataVariable:
    rDataPickle = pickle.Pickler(rDataVariable)
    rDataPickle.dump(rData)

with open('Key/sFileData', 'wb') as sDataVariable:
    sDataPickle = pickle.Pickler(sDataVariable)
    sDataPickle.dump(sData)
