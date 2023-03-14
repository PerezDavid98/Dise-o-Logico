import argparse
import mult
from argparse import ArgumentParser  # importar el módulo ArgumentParser de argparse
from myhdl import Signal, Simulation, intbv, always_comb  # importar las funciones Signal, Simulation, intbv y always_comb de myhdl
from reportlab.lib.units import inch  # importar la unidad de medida 'inch' del módulo reportlab.lib.units
from reportlab.pdfgen import canvas  # importar la función canvas del módulo reportlab.pdfgen
from reportlab.lib.pagesizes import letter, landscape

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
    parser = argparse.ArgumentParser(description='Perform multiplication operation.')
    #parser.add_argument('--bits', type=int, help='Number of bits for precision.')
    parser.add_argument('-a', help='First argument for multiplication.')
    parser.add_argument('-b', help='Second argument for multiplication.')
    args = parser.parse_args()

    #if args.f:
        #read_file()

    result = binary_multiplication(args.a, args.b)

    # Imprimir el resultado en diferentes bases

    
    decimal = int(result, 2)
    hexadecimal = format(int(result), "x")
    binario = int(result)


    # Crear el archivo PDF
    c = canvas.Canvas("Multiplicación.pdf", pagesize=landscape(letter))

    #Primera diapositiva
    c.setFontSize(24)
    c.drawCentredString(5.5 * inch, 6.5 * inch, "Información obtenida")
    c.drawCentredString(5.5 * inch, 4.5 * inch, f"Primer número: {args.a}")
    c.drawCentredString(5.5 * inch, 3.5 * inch, f"Segundo número: {args.b}")
    #c.drawCentredString(4.25 * inch, 7.5 * inch, f"Cantidad de bits: {args.bits}")
    c.showPage()

    #Segunda diapositiva
    c.setFontSize(24)
    c.drawCentredString(5.5 * inch, 7 * inch, "Multiplicación binaria")
    c.drawCentredString(5.5 * inch, 5.5 * inch, f"Resultado en decimal: {decimal}")
    c.drawCentredString(5.5 * inch, 4.5 * inch, f"Resultado en hexadecimal: {hexadecimal}")
    c.drawCentredString(5.5 * inch, 3.5 * inch, f"Resultado en binario: {binario}")
    c.showPage()

    #Tercera diapositiva
    c.setFontSize(20)
    c.drawCentredString(5.5 * inch, 7.25 * inch, "Instituto Tecnológico de Costa Rica")
    c.drawCentredString(5.5 * inch, 6.25 * inch, f"Integrantes:")
    c.drawCentredString(5.5 * inch, 5.5 * inch, f"Bernal Zamora Barrantes")
    c.drawCentredString(5.5 * inch, 5 * inch, f"David Pérez Calvo")
    c.drawCentredString(5.5 * inch, 4.5 * inch, f"Carolina Zúñiga Blanco")
    c.drawCentredString(5.5 * inch, 3.5 * inch, f"Curso: Diseño Lógico")
    c.drawCentredString(5.5 * inch, 2.5 * inch, f"Curso: Grupo 3")
    c.drawCentredString(5.5 * inch, 1.5 * inch, f"I Semestre")
    c.drawCentredString(5.5 * inch, 0.5 * inch, f"2023")
    c.showPage()

    c.save()


