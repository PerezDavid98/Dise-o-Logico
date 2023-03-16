import os
import argparse
import subprocess


def read_file(filename):
    with open(filename, 'r') as file:
        data = file.readline().split()
    return data


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
def binary_multiply(a, b):
    a = parse_factor(a)
    b = parse_factor(b)

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
        
    return product


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bits', type=int, help='numero de bits')
    parser.add_argument('-a', help='primer operando')
    parser.add_argument('-b', help='segundo operando')
    parser.add_argument('-f', help='archivo de configuracion')
    args = parser.parse_args()

    if args.f:
        data = read_file(args.f)
        args.bits = int(data[1])
        args.a = data[3]
        args.b = data[5]

    result = binary_multiply(args.a, args.b)

        
    # Imprimir el resultado en diferentes bases
    binario = int(result)
    decimal = int(result, 2)
    hexadecimal = hex(int(result))


    # Crear el contenido del documento LaTeX
    latex_content = f"""  
        \\documentclass{{beamer}}
        \\title{{Binary Multiplication}}
        \\author{{Your Name}}
        \\date{{\\today}}
        \\begin{{document}}
        
        \\begin{{frame}}
        \\frametitle{{Entradas}}
        \centering
        Operando a: {args.a}\\\\
        Operando b: {args.b} \\\\
        Numero de bits: {args.bits} \\\\
        Nombre de archivo de texto: {args.f}\\\\
        \\end{{frame}}
        
        \\begin{{frame}}
        \\frametitle{{Multiplicacion Binaria}}
        \centering
        {args.a} $\\times$ {args.b} = {result}\\
        \\end{{frame}}

        \\begin{{frame}}
        \\frametitle{{Resultados}}
        \centering
         Resultado en binario: {binario} \\\\
         Resultado en decimal: {decimal} \\\\
         Resultado en hexadecimal: {hexadecimal} \\\\
        \\end{{frame}}
        
        \\begin{{frame}}
        \centering
        Tecnologico de Costa Rica \\\\
        Integrantes:\\\\
        Bernal Zamora Barrantes\\\\
        Carolina Zuniga Blanco \\\\
        David Perez Calvo\\\\
        Curso: Diseno Logico \\\\
        I Semestre \\\\
        2023
        \\end{{frame}}
        
        \\end{{document}}
    """


      # Almacenar el contenido del documento LaTeX en un archivo
    with open("solucion.tex", "w") as f:
        f.write(latex_content)

    subprocess.run(["pdflatex", "solucion.tex"])

    os.remove('solucion.out')
    os.remove('solucion.aux')
    os.remove('solucion.log')
    os.remove('solucion.nav')
    os.remove('solucion.snm')
    os.remove('solucion.toc')
    os.remove('solucion.tex')




    


