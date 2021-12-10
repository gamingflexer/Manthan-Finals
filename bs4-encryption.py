'''
pip install pyarmor
pyarmor obfuscate /path/to/script
python /path/to/script


'''


#import colorama
from base64 import b64decode, b64encode


print('###  LOST MINDS ###')

print
code=input("Enter your code to encode -- > ")

print(code)




def hidecode(code):
    return b64encode(code.encode())

def show(decode):
    return b64decode(code.decode())


#eval (compile(string,''))

print(hidecode(code)) 