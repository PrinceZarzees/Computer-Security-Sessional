import encrypt_1805009
import decrypt_1805009
import time
key="BUET"
plain_text="Can They Do This?????***&&&&"
print ("Plain Text: ")
print ("In ASCII: ",plain_text)
print ("In HEX: ",encrypt_1805009.string_to_hex(plain_text))
print ("Key: ")
print ("In ASCII: ",key)
print ("In HEX: ",encrypt_1805009.string_to_hex(key))
start=time.time()
cipher_text=encrypt_1805009.encrypt_text(key,plain_text)
end=time.time()
encryption_time=end-start
print ("Cipher Text: ")
print ("In ASCII: ",cipher_text)
print ("In HEX: ",encrypt_1805009.string_to_hex(cipher_text))
print ("Deciphered Text: ")
start=time.time()
dt=decrypt_1805009.decrypt_text(key,cipher_text)
end=time.time()
decryption_time=end-start
print ("In ASCII: ",dt)
print ("In HEX: ",encrypt_1805009.string_to_hex(dt))
print ("Execution time details:")
print ("Key Scheduling : %f seconds" %encrypt_1805009.key_scheduleing_time)
print ("Encryption Time : %f seconds" %encryption_time)
print ("Decryption Time : %f seconds" %decryption_time)