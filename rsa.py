"""Codificacion de parejas ASCII y operaciones RSA educativas."""
from algoritmos import es_primo, mcd, inverso_modular, potencia_modular


def entero(valor, nombre):
    if isinstance(valor, bool):
        raise ValueError(f"{nombre} debe ser un entero.")
    texto = str(valor)
    if not texto or texto.strip() != texto or not (texto.isdecimal() or (texto.startswith('-') and texto[1:].isdecimal())) or any(c not in '0123456789-' for c in texto):
        raise ValueError(f"{nombre} debe ser un entero decimal.")
    return int(texto)


def parametros(p, q, e):
    p, q, e = entero(p, 'p'), entero(q, 'q'), entero(e, 'e')
    if not es_primo(p) or not es_primo(q):
        raise ValueError('p y q deben ser numeros primos.')
    if p == q:
        raise ValueError('p y q deben ser distintos.')
    n = p * q
    if not 126126 < n < 1000000:
        raise ValueError('Se requiere 126126 < n < 1000000.')
    phi = (p - 1) * (q - 1)
    if e <= 1 or mcd(e, phi) != 1:
        raise ValueError('e debe ser mayor que 1 y MCD(e, phi) = 1.')
    return {'p':p,'q':q,'e':e,'n':n,'phi':phi,'mcd':mcd(e,phi)}


def encriptar(mensaje, p, q, e):
    datos = parametros(p,q,e)
    if not mensaje:
        raise ValueError('Ingrese un mensaje no vacio.')
    for i, caracter in enumerate(mensaje, 1):
        if not 32 <= ord(caracter) <= 126:
            raise ValueError(f'Caracter no admitido en posicion {i}: {caracter!r}. Solo ASCII 32 a 126.')
    longitud = len(mensaje)
    relleno = longitud % 2 == 1
    preparado = mensaje + (' ' if relleno else '')
    filas = []
    for i in range(0,len(preparado),2):
        pareja = preparado[i:i+2]
        ascii_texto = ''.join(f'{ord(c):03d}' for c in pareja)
        m = int(ascii_texto)
        c = potencia_modular(m,datos['e'],datos['n'])
        filas.append({'pareja':pareja,'ascii':ascii_texto,'m':m,'c':c,'cifrado':f'{c:06d}'})
    return {**datos,'mensaje':mensaje,'preparado':preparado,'L':longitud,'relleno':relleno,'filas':filas,'C':' '.join(f['cifrado'] for f in filas)}


def desencriptar(cifrado, longitud, p, q, e):
    datos = parametros(p,q,e)
    L = entero(longitud,'L')
    if not cifrado or not cifrado.strip():
        raise ValueError('Ingrese el cifrado C.')
    bloques = cifrado.split(' ')
    if any(len(b)!=6 or any(d not in '0123456789' for d in b) for b in bloques):
        raise ValueError('Cada bloque debe tener exactamente seis digitos y separarse por un solo espacio.')
    k = len(bloques)
    if L not in (2*k,2*k-1):
        raise ValueError(f'L debe ser {2*k-1} o {2*k} para {k} bloque(s).')
    d = inverso_modular(datos['e'],datos['phi'])
    filas = []
    caracteres = []
    for bloque in bloques:
        c = int(bloque)
        if c >= datos['n']:
            raise ValueError(f'Bloque {bloque} fuera de rango: debe ser menor que n.')
        m = potencia_modular(c,d,datos['n'])
        ascii_texto = f'{m:06d}'
        codigos = (int(ascii_texto[:3]),int(ascii_texto[3:]))
        if any(not 32 <= codigo <= 126 for codigo in codigos):
            raise ValueError(f'Bloque {bloque} produce codigos ASCII invalidos: {codigos}.')
        pareja = ''.join(chr(codigo) for codigo in codigos)
        caracteres.append(pareja)
        filas.append({'cifrado':bloque,'c':c,'m':m,'ascii':ascii_texto,'pareja':pareja})
    preparado = ''.join(caracteres)
    relleno = L % 2 == 1
    if relleno and preparado[-1] != ' ':
        raise ValueError('Se esperaba un espacio de relleno al final del texto recuperado.')
    mensaje = preparado[:-1] if relleno else preparado
    return {**datos,'d':d,'L':L,'relleno':relleno,'preparado':preparado,'mensaje':mensaje,'C':cifrado,'filas':filas}
