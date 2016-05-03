import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random

def genkey():
	random_gen = Random.new().read
	private = RSA.generate(1024, random_gen)
	pub = key.publickey()
	print 'public key:', pub
	print "private key:",key.privatekey()
	data = "I will encrypt this string"
	print data
	encrypted = pub.encrypt(data,32)[0]
	print "encrypted string:", encrypted
	print key.decrypt(encrypted)

def main():
	genkey()



if __name__ == '__main__':
	main()