import argparse


# Files
def read_file(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    for line in lines:
        print(line.strip())


# Number Equivalences
def hex_to_bin(number):
    return bin(int(number, 16))[2:]


def dec_to_bin(number):
    return bin(int(number))[2:]


# Main Program utils
def parse_factor(factor):
    if "d" in factor[0]:
        return dec_to_bin(factor[1:])
    elif "h" in factor[0]:
        return hex_to_bin(factor[1:])
    elif "b" in factor[0]:
        return factor
    else:
        return dec_to_bin(factor)


def binary_addition(a, b):
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    b = b.zfill(max_len)

    addition = ''
    temp = 0

    for i in range(max_len - 1, -1, -1):
        num = int(a[i]) + int(b[i]) + temp
        if num % 2 == 0:
            addition = '0' + addition
        else:
            addition = '1' + addition

        if num == 2:
            temp = 1
        else:
            temp = 0

    if temp != 0:
        addition = '01' + addition

    if int(addition) == 0:
        addition = '0'

    return addition


# Main program
def binary_multiplication(a, b):
    a = parse_factor(a)
    b = parse_factor(b)

    print(a, b)

    max_len = max(len(a), len(b))
    min_len = min(len(a), len(b))

    product = ''
    aux = ''

    temp = []
    zeroes = 0
    temp_index = 0

    for j in range(min_len - 1, -1, -1):
        aux = ''
        for i in range(max_len - 1, -1, -1):
            sum_result = int(a[i]) * int(b[j])
            if sum_result == 0:
                aux = '0' + aux
            elif sum_result == 1:
                aux = '1' + aux
        aux = aux + ('0' * zeroes)
        zeroes += 1
        temp.append(aux)

        if len(temp) == 2:
            product = binary_addition(str(temp[0]), str(temp[1]))
        elif len(temp) > 2:
            temp_index = len(temp)
            temp_index += 1
            product = binary_addition(str(product), str(temp[temp_index - 2]))
        else:
            pass

    print(product)


def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bits", help="Cantidad de bits de los numeros")
    parser.add_argument("-a", help="Factor 'A' a multiplicar")
    parser.add_argument("-b", help="Factor 'B' a multiplicar")
    parser.add_argument("-f", help="Nombre del archivo")

    args = parser.parse_args()

    if args.f:
        read_file()

    binary_multiplication(args.a, args.b)


init()