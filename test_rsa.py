import unittest
from unittest.mock import Mock, patch
from types import SimpleNamespace
from main import Aplicacion
from rsa import encriptar, desencriptar
from algoritmos import mcd, inverso_modular, potencia_modular, es_primo

P,Q,E=367,373,17

class CampoFalso:
    def __init__(self,value=''):
        self.value=value

    def delete(self,*args):
        del args
        self.value=''

    def insert(self,index,value):
        del index
        self.value=value

    def get(self,*args):
        del args
        return self.value

    def configure(self,**kwargs):
        del kwargs

class TablaFalsa:
    def __init__(self):
        self.filas=['resultado anterior']

    def get_children(self):
        return self.filas

    def delete(self,*items):
        del items
        self.filas=[]

    def insert(self,parent,index,values):
        del parent,index
        self.filas.append(values)

class PruebasRSA(unittest.TestCase):
    def test_referencia(self):
        a=encriptar('RSA',P,Q,E)
        self.assertEqual((a['n'],a['phi'],a['L'],a['C']),(136891,136152,3,'026054 123875'))
        b=desencriptar(a['C'],a['L'],P,Q,E)
        self.assertEqual((b['d'],b['mensaje']),(8009,'RSA'))

    def test_transferir_solo_copia_datos_y_limpia_resultados(self):
        cifrado=encriptar('RSA',P,Q,E)
        entradas={
            ('dec','p'):CampoFalso('11'),
            ('dec','q'):CampoFalso('13'),
            ('dec','e'):CampoFalso('7'),
            ('dec','C'):CampoFalso('cifrado anterior'),
            ('dec','L'):CampoFalso('4'),
            ('dec','resultado'):CampoFalso('resultado anterior con d'),
            ('dec','tabla'):TablaFalsa(),
        }
        pestañas=SimpleNamespace(select=Mock())
        app=Aplicacion.__new__(Aplicacion)
        app.ultimo=cifrado
        app.entradas=entradas
        app.tabs=pestañas
        app.ejecutar=Mock()

        with patch('main.messagebox.showinfo') as mostrar_info:
            app.transferir()

        self.assertEqual([entradas['dec',clave].get() for clave in ('p','q','e')],['367','373','17'])
        self.assertEqual(entradas['dec','C'].get(), '026054 123875')
        self.assertEqual(entradas['dec','L'].get(), '3')
        self.assertEqual(entradas['dec','resultado'].get(), '')
        self.assertEqual(entradas['dec','tabla'].filas, [])
        pestañas.select.assert_called_once_with(1)
        app.ejecutar.assert_not_called()
        mostrar_info.assert_called_once_with(
            'Cifrado recibido',
            'Cifrado recibido correctamente. Presiona DESENCRIPTAR para recuperar el mensaje original',
        )

    def test_desencriptar_se_ejecuta_al_presionar_su_boton(self):
        entradas={
            ('dec','p'):CampoFalso('367'),
            ('dec','q'):CampoFalso('373'),
            ('dec','e'):CampoFalso('17'),
            ('dec','C'):CampoFalso('026054 123875'),
            ('dec','L'):CampoFalso('3'),
            ('dec','resultado'):CampoFalso('resultado anterior'),
            ('dec','tabla'):TablaFalsa(),
        }
        app=Aplicacion.__new__(Aplicacion)
        app.entradas=entradas

        with patch('main.messagebox.showerror') as mostrar_error:
            app.ejecutar('dec')

        self.assertIn('LLAVE PRIVADA (d, n): (8009, 136891)', entradas['dec','resultado'].get())
        self.assertIn("MENSAJE RECUPERADO = 'RSA'", entradas['dec','resultado'].get())
        self.assertEqual(len(entradas['dec','tabla'].filas),2)
        mostrar_error.assert_not_called()

    def test_encriptacion_invalida_limpia_y_no_transfiere_cifrado_anterior(self):
        entradas={
            ('enc','p'):CampoFalso('367'),
            ('enc','q'):CampoFalso('373'),
            ('enc','e'):CampoFalso('17'),
            ('enc','mensaje'):CampoFalso('JOSE'),
            ('enc','resultado'):CampoFalso(),
            ('enc','tabla'):TablaFalsa(),
            ('dec','p'):CampoFalso(),
            ('dec','q'):CampoFalso(),
            ('dec','e'):CampoFalso(),
            ('dec','C'):CampoFalso(),
            ('dec','L'):CampoFalso(),
            ('dec','resultado'):CampoFalso(),
            ('dec','tabla'):TablaFalsa(),
        }
        app=Aplicacion.__new__(Aplicacion)
        app.entradas=entradas
        app.tabs=SimpleNamespace(select=Mock())
        app.ultimo=None

        with patch('main.messagebox.showerror') as mostrar_error, \
             patch('main.messagebox.showinfo') as mostrar_info:
            app.ejecutar('enc')
            cifrado_anterior=app.ultimo['C']
            self.assertTrue(cifrado_anterior)
            self.assertIn(cifrado_anterior,entradas['enc','resultado'].get())
            self.assertTrue(entradas['enc','tabla'].filas)

            entradas['enc','mensaje'].value='JOSÉ'
            app.ejecutar('enc')

            self.assertIsNone(app.ultimo)
            self.assertEqual(entradas['enc','resultado'].get(),'')
            self.assertEqual(entradas['enc','tabla'].filas,[])
            mostrar_error.assert_called_once()
            self.assertIn('Caracter no admitido',mostrar_error.call_args.args[1])

            app.transferir()

        self.assertEqual(entradas['dec','C'].get(),'')
        self.assertEqual(entradas['dec','L'].get(),'')
        self.assertEqual(entradas['dec','resultado'].get(),'')
        mostrar_info.assert_called_once_with('Aviso','Primero encripte un mensaje.')

        entradas['enc','mensaje'].value='RSA'
        with patch('main.messagebox.showerror') as mostrar_error:
            app.ejecutar('enc')

        self.assertEqual(app.ultimo['C'],'026054 123875')
        self.assertIn('CIFRADO C = 026054 123875',entradas['enc','resultado'].get())
        self.assertEqual(len(entradas['enc','tabla'].filas),2)
        mostrar_error.assert_not_called()

    def test_desencriptacion_invalida_limpia_resultados_anteriores(self):
        entradas={
            ('dec','p'):CampoFalso('367'),
            ('dec','q'):CampoFalso('373'),
            ('dec','e'):CampoFalso('17'),
            ('dec','C'):CampoFalso('12345'),
            ('dec','L'):CampoFalso('2'),
            ('dec','resultado'):CampoFalso('mensaje anterior y llave privada'),
            ('dec','tabla'):TablaFalsa(),
        }
        app=Aplicacion.__new__(Aplicacion)
        app.entradas=entradas

        with patch('main.messagebox.showerror') as mostrar_error:
            app.ejecutar('dec')

        self.assertEqual(entradas['dec','resultado'].get(),'')
        self.assertEqual(entradas['dec','tabla'].filas,[])
        mostrar_error.assert_called_once()

    def test_mensajes(self):
        for texto in ['AB','A','aBcD','123!?','  Hola 123!?  ','A  B',' A ','AB  ','  ',' ']:
            with self.subTest(texto=repr(texto)):
                a=encriptar(texto,P,Q,E)
                self.assertEqual(desencriptar(a['C'],a['L'],P,Q,E)['mensaje'],texto)

    def test_algoritmos(self):
        self.assertTrue(es_primo(367))
        self.assertFalse(es_primo(1))
        self.assertEqual(mcd(17,136152),1)
        self.assertEqual(inverso_modular(17,136152),8009)
        self.assertEqual(potencia_modular(82083,17,136891),26054)

    def test_parametros_invalidos(self):
        for p,q,e in [(4,Q,E),(P,P,E),(2,3,E),(P,Q,2),(P,Q,1),('x',Q,E)]:
            with self.subTest(p=p,q=q,e=e),self.assertRaises(ValueError):
                encriptar('AB',p,q,e)

    def test_texto_invalido(self):
        for texto in ['','ñ','á','A\nB','A\tB']:
            with self.subTest(texto=repr(texto)),self.assertRaises(ValueError):
                encriptar(texto,P,Q,E)

    def test_cifrado_invalido(self):
        for c,L in [('12345',2),('1234567',2),('12x456',2),('000001  000002',4),('136891',2),('000001',4),('000001',0),('',1)]:
            with self.subTest(c=c,L=L),self.assertRaises(ValueError):
                desencriptar(c,L,P,Q,E)

    def test_ascii_recuperado_invalido(self):
        with self.assertRaises(ValueError):
            desencriptar('000000',2,P,Q,E)

    def test_relleno_invalido(self):
        a=encriptar('AB',P,Q,E)
        with self.assertRaises(ValueError):
            desencriptar(a['C'],1,P,Q,E)

if __name__=='__main__':
    unittest.main()
