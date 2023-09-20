import random
def string_to_number(message):
    return int.from_bytes(message.encode(), 'big')


def number_to_string(number):
    return number.to_bytes((number.bit_length() + 7) // 8, 'big').decode()
def power(a,d,n):
    if (d==0):
        return 1
    if (d%2==0):
        t=power(a,d//2,n)
        return (t*t)%n
    else:
        t=power(a,d//2,n)
        return ((t*a)%n*t)%n
def miller_rabin(n,k):
    if (n%2==0):
        return False
    d=n-1
    s=0
    while(d%2==0):
        s+=1
        d=d//2
    for i in range(k):
        a=random.randrange(2,n-1)
        x=power(a,d,n)
        for j in range(s):
            y=power(x,2,n)
            if(y==1 and x!=1 and x!=n-1):
                return False
            x=y
        if (y!=1):
            return False
    return True
def generate_prime(k):
    while(True):
        n=random.randrange(2**(k-1),2**(k))
        if(miller_rabin(n,5)):
            return n
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a)*x, x
def generate_keypair(bits):
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    n = p * q
    l=((p-1)*(q-1))//gcd(p-1,q-1)

    while True:
        e = random.randrange(3, l)
        if gcd(e, l) == 1:
            break
    _, d,_ = extended_gcd(e,l)
    d = d % l
    return (e, n), (d, n)


def encrypt(message, public_key):
    e, n = public_key
    return power(message, e, n)


def decrypt(ciphertext, private_key):
    d, n = private_key
    return power(ciphertext, d, n)


#Example usage
# message = "BUET CSE18 Batch"
# temp=255
# bits=8
# public_key, private_key = generate_keypair(bits)
# print ("Public key: ", public_key)
# print ("Private key: ", private_key)
# encrypted_message = encrypt(temp, public_key)
# decrypted_message = decrypt(encrypted_message, private_key)
# print (decrypted_message)
# print("Decrypted:", number_to_string(decrypted_message))

