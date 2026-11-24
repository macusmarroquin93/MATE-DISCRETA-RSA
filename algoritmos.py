"""Algoritmos matematicos implementados sin atajos criptograficos."""

def es_primo(numero):
    if numero < 2:
        return False
    if numero == 2:
        return True
    if numero % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= numero:
        if numero % divisor == 0:
            return False
        divisor += 2
    return True


def mcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def inverso_modular(a, modulo):
    anterior, actual = modulo, a % modulo
    x_anterior, x_actual = 0, 1
    while actual:
        cociente = anterior // actual
        anterior, actual = actual, anterior - cociente * actual
        x_anterior, x_actual = x_actual, x_anterior - cociente * x_actual
    if anterior != 1:
        raise ValueError("El exponente no tiene inverso modular.")
    return x_anterior % modulo


def potencia_modular(base, exponente, modulo):
    if exponente < 0 or modulo <= 0:
        raise ValueError("Exponente o modulo invalido.")
    resultado = 1 % modulo
    base %= modulo
    while exponente > 0:
        if exponente % 2:
            resultado = (resultado * base) % modulo
        base = (base * base) % modulo
        exponente //= 2
    return resultado
