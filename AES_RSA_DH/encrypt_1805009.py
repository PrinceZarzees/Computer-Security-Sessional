import numpy
import bitvectordemo_1805009 as bv 
import time
def string_to_hex(string):
    hex_string = ''
    for c in string:
        hex_string += hex(ord(c))[2:].zfill(2)
    return hex_string
def text_to_hex_array(text):
    hexarray=[]
    for i in range(0,len(text)):
        hexarray.append((hex(ord(text[i]))))
    while(len(hexarray)<16):
        hexarray.append('0x00')
    return hexarray
def g(l,round_constant):
    l=numpy.concatenate((l[1:],l[:1]))
    for i in range(len(l)):
        l[i]=hex(bv.Sbox[int(l[i],16)])
    xor_result=numpy.array(l)
    for i in range(0,len(xor_result)):
        xor_result[i]=hex(int(xor_result[i],16)^int(round_constant[i],16))
    return xor_result
def xor(a,b):

    xor_result = numpy.array(a)
    for i in range(0,len(xor_result)):
        xor_result[i]=hex(int(xor_result[i],16)^int(b[i],16))
    return xor_result


def round0(input_text,round_key_matrix):
    int_list = [hex(int(hex_val, 16)) for hex_val in input_text]
    # Reshape the list into a 4x4 column-major array
    state_matrix = numpy.array(int_list).reshape((4, 4), order='F')
    for i in range(0,4):
        for j in range(0,4):
            state_matrix[i][j]=hex(int(state_matrix[i][j],16)^int(round_key_matrix[0][i][j],16))
    return state_matrix
def round(state_matrix,round_number,round_key_matrix):
    #Substitution
    for i in range(0,4):
        for j in range(0,4):
            state_matrix[i][j]=hex(bv.Sbox[int(state_matrix[i][j],16)])
    #Shift Rows
    for i in range(0,4):
        state_matrix[i]=numpy.concatenate((state_matrix[i][i:],state_matrix[i][:i]))
    #Mix Columns
    if (round_number!=10):
        temp=[[0x02,0x03,0x01,0x01],[0x01,0x02,0x03,0x01],[0x01,0x01,0x02,0x03],[0x03,0x01,0x01,0x02]]
        temp_mat=numpy.zeros((4,4),dtype=object)
        for i in range(0,4):
            for j in range(0,4):
                s=0
                for k in range(0,4):
                    AES_modulus = bv.BitVector(bitstring='100011011')
                    bv1 = bv.BitVector(intVal=temp[i][k], size=8)
                    bv2 = bv.BitVector(intVal=int(state_matrix[k][j],16), size=8)
                    bv3 = bv1.gf_multiply_modular(bv2, AES_modulus, 8)
                    s=s^bv3.intValue()
                temp_mat[i][j]=hex(s)
        state_matrix=numpy.copy(temp_mat)
    #Add Round Key
    for i in range(0,4):
        for j in range(0,4):
            state_matrix[i][j]=hex(int(state_matrix[i][j],16)^int(round_key_matrix[round_number][i][j],16))
    return state_matrix


def encrypt(key,input_text):
    global key_scheduleing_time
    start=(time.time())
    w=[]
    for i in range(0,len(key),4):
        w.append(numpy.array(key[i:i+4]))
    for i in range(4,44,4):
        for j in range(0,4):
            if(j==0):
                if (i==4):
                    curr=0x01 
                else:
                    if (prev<0x80):
                        curr=prev*2
                    else:
                        curr=(prev*2)^0x11b
                round_constant = numpy.array([hex(curr), 0x00, 0x00, 0x00])
                prev=curr
                w.append(xor(w[i+j-4],g(w[i+j-1],round_constant)))
            else:
                w.append(xor(w[i+j-1],w[i+j-4]))
    end=time.time()
    key_scheduleing_time=end-start
    # for i in range(0,44,4):
    #     print (w[i:i+4])
    round_key_matrix=[]
    for i in range(0,11):
        w_int = [[hex(int(hex_val, 16)) for hex_val in arr] for arr in w[i*4:i*4+4]]
        round_key_matrix.append(numpy.column_stack(w_int))
    # print(round_key_matrix)
    t=round0(input_text,round_key_matrix)
    for i in range(1,10+1):
        t=round(t,i,round_key_matrix)
    return t
def encrypt_text(key,input_text):
    if (len(key)>16):
        key=key[:16]
    key=text_to_hex_array(key)
    cipher_text=""
    for k in range(0,len(input_text),16):
        temp_text=text_to_hex_array(input_text[k:min(k+16,len(input_text))])
        encrypted=(encrypt(key,temp_text))
        temp=""
        for i in range(0,4):
            for j in range(0,4):
                temp+=chr(int(encrypted[j][i],16))
        cipher_text+=temp
    return cipher_text
# key="BUET CSE18 Batch"
# plain_text="Can They Do This"
# print ("Plain Text: ")
# print ("In ASCII: ",plain_text)
# print ("In HEX: ",string_to_hex(plain_text))
# print ("Key: ")
# print ("In ASCII: ",key)
# print ("In HEX: ",string_to_hex(key))
# start=time.time()
# cipher_text=encrypt_text(key,plain_text)
# end=time.time()
# encryption_time=end-start
# print ("Cipher Text: ")
# print ("In ASCII: ",cipher_text)
# print ("In HEX: ",string_to_hex(cipher_text))
# print ("Deciphered Text: ")
# start=time.time()
# dt=decrypt.decrypt_text(key,cipher_text)
# end=time.time()
# decryption_time=end-start
# print ("In ASCII: ",dt)
# print ("In HEX: ",string_to_hex(dt))
# print ("Execution time details:")
# print ("Key Scheduling : %f seconds" %key_scheduleing_time)
# print ("Encryption Time : %f seconds" %encryption_time)
# print ("Decryption Time : %f seconds" %decryption_time)




