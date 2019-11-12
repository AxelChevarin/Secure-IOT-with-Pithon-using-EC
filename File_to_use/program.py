from Crypto.Cipher import AES
from Crypto import Random
import os,random, sys,pkg_resources,hashlib,base64,pickle,time
from fastecdsa import curve, ecdsa, keys
from hashlib import sha256
from websocket import create_connection

ws = create_connection("ws://echo.websocket.org/")
h = hashlib.sha256()

#=====get the public key=====
my_file_pubKey = "Key/public_key"
with open(my_file_pubKey, 'rb') as pub:
    depickler = pickle.Unpickler(pub)
    public_key = depickler.load()

my_file_r = 'Key/rFileData'
with open(my_file_r, 'rb') as rVariable:
    rDepickler = pickle.Unpickler(rVariable)
    r = rDepickler.load()

my_file_s = 'Key/sFileData'
with open(my_file_s, 'rb') as sVariable:
    sDepickler = pickle.Unpickler(sVariable)
    s = sDepickler.load()


#=====Function hash with SHA256=====
def file_hash(filename):
  with open(filename, 'rb', buffering=0) as f:
    for b in iter(lambda : f.read(128*1024), b''):
      h.update(b)
  return h.hexdigest()

hash_Data_file = file_hash('data.txt.enc')


#=====Function validSignature=====

def validSignature(hash):
    valid = ecdsa.verify((r, s), hash, public_key)
    return valid

elliptic_curve = validSignature(hash_Data_file)
print(elliptic_curve)


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
    file_to_decrypt = 'data.txt.enc'
    with open('Key/keyAES', 'rb') as keyAES:
        AESKey_depickler = pickle.Unpickler(keyAES)
        key = AESKey_depickler.load()
    decrypt_file(key,file_to_decrypt)
    with open('data.txt', 'rb') as my_data:
        data_from_file = my_data.read()
    data= data_from_file
    os.remove('data.txt')
    while True:
        print("Sending data ....")
        ws.send(data)
        print("Sent")
        print("Receiving...")
        result =  ws.recv()
        print("Received '%s'" % result)
        time.sleep(1)
    ws.close()
    os.remove('data.txt')
else:
    data_to_write = 'bonjour toto'
    with open('data.txt', 'w') as my_data:
        my_data.write(data_to_write)

    with open('data.txt', 'r') as my_data:
        data_from_file = my_data.read()
    data= data_from_file
    os.remove('data.txt')
    while True:
        print("Sending data ....")
        ws.send(data)
        print("Sent")
        print("Receiving...")
        result =  ws.recv()
        print("Received '%s'" % result)
        time.sleep(1)
    ws.close()
