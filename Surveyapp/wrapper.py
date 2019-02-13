from .errors import  *

count =1

while count <=5:
    try:
        password = input('Enter password')
        message ='User has given the wrong password ,Please provide the correct password'
        raise InvaliPassword(message)
    except InvaliPassword as P:
        print(P.msg)
        count +=1

