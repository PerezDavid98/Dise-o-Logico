from argparse import ArgumentParser  # importar el módulo ArgumentParser de argparse
from myhdl import Signal, Simulation, intbv, always_comb  # importar las funciones Signal, Simulation, intbv y always_comb de myhdl
from reportlab.lib.pagesizes import letter  # importar el tamaño de página 'letter' del módulo reportlab.lib.pagesizes
from reportlab.lib.units import inch  # importar la unidad de medida 'inch' del módulo reportlab.lib.units
from reportlab.pdfgen import canvas  # importar la función canvas del módulo reportlab.pdfgen

def mult_comb(a, b, result):
    """Función que multiplica dos señales de entrada a y b y almacena el resultado en la señal result."""
    @always_comb
    def logic():
        result.next = a * b
    return logic

if __name__ == '__main__':
    parser = ArgumentParser(description='Programa para multiplicar dos números.')
    parser.add_argument('--bits', type=int, help='Cantidad de bits de los factores a multiplicar')
    parser.add_argument('-a', type=str, help='Valor del primer factor en notación decimal, hexadecimal o binaria', required=True)
    parser.add_argument('-b', type=str, help='Valor del segundo factor en notación decimal, hexadecimal o binaria', required=True)
    args = parser.parse_args()

    # Convertir los factores a intbv
    base = args.a[0]  # obtener la base del primer factor
    if base == 'h':  # si la base es hexadecimal
        num1 = int(args.a[1:], 16)  # convertir el valor a entero
    elif base == 'b':  # si la base es binaria
        num1 = int(args.a[1:], 2)  # convertir el valor a entero
    else:  # de lo contrario, la base es decimal
        num1 = int(args.a)  # convertir el valor a entero
    a = Signal(intbv(num1)[8:])  # crear una señal de 8 bits con el valor convertido

    base = args.b[0]  # obtener la base del segundo factor
    if base == 'h':  # si la base es hexadecimal
        num2 = int(args.b[1:], 16)  # convertir el valor a entero
    elif base == 'b':  # si la base es binaria
        num2 = int(args.b[1:], 2)  # convertir el valor a entero
    else:  # de lo contrario, la base es decimal
        num2 = int(args.b)  # convertir el valor a entero
    b = Signal(intbv(num2)[8:])  # crear una señal de 8 bits con el valor convertido

    # Señal de salida de 16 bits
    result = Signal(intbv(0)[16:])  # crear una señal de 16 bits inicializada en cero

    # Instanciar la función de multiplicación
    mult = mult_comb(a, b, result)  # crear una instancia de la función mult_comb

    # Ejecutar la simulación
    sim = Simulation(mult)  # crear una simulación con la instancia de la función mult_comb
    sim.run()  # ejecutar la simulación

    # Imprimir el resultado en diferentes bases
    decimal = int(result)
    hexadecimal = format(int(result), "x")
    binario = format(int(result), "b")

    # Crear el archivo PDF
    c = canvas.Canvas("multiplicacion.pdf", pagesize=letter)
    c.setFontSize(16)
    c.drawCentredString(4.25 * inch, 10.5 * inch, "Multiplicación de dos números")
    c.setFontSize(14)
    c.drawCentredString(4.25 * inch, 9.5 * inch, f"Primer factor: {args.a}")
    c.drawCentredString(4.25 * inch, 9 * inch, f"Segundo factor: {args.b}")
    c.drawCentredString(4.25 * inch, 8.5 * inch, f"Cantidad de bits: {args.bits}")
    c.setFontSize(12)
    c.drawCentredString(4.25 * inch, 7.5 * inch, f"Resultado en decimal: {decimal}")
    c.drawCentredString(4.25 * inch, 7 * inch, f"Resultado en hexadecimal: {hexadecimal}")
    c.drawCentredString(4.25 * inch, 6.5 * inch, f"Resultado en binario: {binario}")
    c.save()



