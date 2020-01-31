
import random
import string

#gene 26+26 letters and 10 digits
forSelect = string.ascii_letters + string.digits

def generate_code(count, length):
    for x in range(count):
        re = ""
        for y in range(length):
            re += random.choice(forSelect)
        print(re)


if __name__ == '__main__':
    generate_code(200,20)