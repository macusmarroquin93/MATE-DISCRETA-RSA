"""Interfaz grafica de laboratorio RSA. Solo biblioteca estandar."""
import tkinter as tk
from tkinter import ttk, messagebox
from rsa import encriptar, desencriptar

BG='#0b1220'; PANEL='#162235'; TEXT='#e7edf8'; MUTED='#a9bad0'; ACCENT='#3bd5c3'

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('RSA LAB | Matematica Discreta I')
        self.geometry('1120x790')
        self.minsize(850,650)
        self.configure(bg=BG)
        style=ttk.Style(self)
        style.theme_use('clam')
        style.configure('TNotebook',background=BG,borderwidth=0)
        style.configure('TNotebook.Tab',padding=(20,12),font=('Segoe UI',11,'bold'))
        style.configure('Treeview',background=PANEL,foreground=TEXT,fieldbackground=PANEL,rowheight=29,font=('Consolas',10))
        style.configure('Treeview.Heading',background='#263850',foreground=TEXT,font=('Segoe UI',10,'bold'))
        style.map('Treeview',background=[('selected','#146f77')])
        tk.Label(self,text='RSA  /  LABORATORIO DE CRIPTOGRAFÍA',bg=BG,fg=ACCENT,font=('Segoe UI',12,'bold')).pack(anchor='w',padx=30,pady=(24,2))
        tk.Label(self,text='Matemática discreta',bg=BG,fg=TEXT,font=('Segoe UI',24,'bold')).pack(anchor='w',padx=30,pady=(0,2))
        tk.Label(self,text='Hecho por Raúl Godínez y María Marroquín',bg=BG,fg=MUTED,font=('Segoe UI',10)).pack(anchor='w',padx=30,pady=(0,12))
        self.tabs=ttk.Notebook(self)
        self.tabs.pack(fill='both',expand=True,padx=25,pady=(0,22))
        self.enc=self.crear_pestana('01  ENCRIPTAR')
        self.dec=self.crear_pestana('02  DESENCRIPTAR')
        self.entradas={}
        for modo,contenedor in [('enc',self.enc),('dec',self.dec)]:
            self.crear_formulario(modo,contenedor)

    def crear_pestana(self,nombre):
        frame=tk.Frame(self.tabs,bg=BG)
        self.tabs.add(frame,text=nombre)
        return frame

    def etiqueta(self,padre,texto):
        return tk.Label(padre,text=texto,bg=BG,fg=MUTED,font=('Segoe UI',10,'bold'))

    def crear_formulario(self,modo,padre):
        zona=tk.Frame(padre,bg=BG)
        zona.pack(fill='x',padx=12,pady=14)
        for columna,(clave,valor) in enumerate([('p','367'),('q','373'),('e','17')]):
            sub=tk.Frame(zona,bg=BG)
            sub.grid(row=0,column=columna,sticky='ew',padx=(0,12))
            self.etiqueta(sub,clave.upper()+'  ·  '+('PRIMO' if clave!='e' else 'EXPONENTE')).pack(anchor='w')
            entrada=tk.Entry(sub,font=('Consolas',13),bg=PANEL,fg=TEXT,insertbackground=TEXT,relief='flat',bd=0)
            entrada.insert(0,valor)
            entrada.pack(fill='x',ipady=9,pady=6)
            self.entradas[modo,clave]=entrada
            zona.columnconfigure(columna,weight=1)
        cuerpo=tk.Frame(padre,bg=BG)
        cuerpo.pack(fill='x',padx=12)
        if modo=='enc':
            self.etiqueta(cuerpo,'MENSAJE ORIGINAL · ASCII IMPRIMIBLE').pack(anchor='w')
            campo=tk.Text(cuerpo,height=3,font=('Consolas',12),bg=PANEL,fg=TEXT,insertbackground=TEXT,relief='flat',wrap='char')
            campo.insert('1.0','RSA')
            campo.pack(fill='x',pady=(6,10))
            self.entradas[modo,'mensaje']=campo
        else:
            self.etiqueta(cuerpo,'CIFRADO C · BLOQUES DE SEIS DÍGITOS').pack(anchor='w')
            campo=tk.Text(cuerpo,height=3,font=('Consolas',12),bg=PANEL,fg=TEXT,insertbackground=TEXT,relief='flat',wrap='char')
            campo.insert('1.0','026054 123875')
            campo.pack(fill='x',pady=(6,8))
            self.entradas[modo,'C']=campo
            self.etiqueta(cuerpo,'LONGITUD ORIGINAL L').pack(anchor='w')
            largo=tk.Entry(cuerpo,font=('Consolas',12),bg=PANEL,fg=TEXT,insertbackground=TEXT,relief='flat')
            largo.insert(0,'3')
            largo.pack(fill='x',ipady=7,pady=(5,9))
            self.entradas[modo,'L']=largo
        botones=tk.Frame(padre,bg=BG)
        botones.pack(fill='x',padx=12,pady=(0,10))
        tk.Button(botones,text='▶  '+('ENCRIPTAR MENSAJE' if modo=='enc' else 'DESENCRIPTAR MENSAJE'),command=lambda m=modo:self.ejecutar(m),bg=ACCENT,fg='#06212a',activebackground='#79e5da',font=('Segoe UI',11,'bold'),relief='flat',cursor='hand2',padx=20,pady=10).pack(side='left')
        if modo=='enc':
            tk.Button(botones,text='Enviar cifrado a desencriptar →',command=self.transferir,bg='#263850',fg=TEXT,font=('Segoe UI',10),relief='flat',cursor='hand2',padx=15,pady=11).pack(side='left',padx=12)
        self.etiqueta(padre,'RESULTADOS Y PROCEDIMIENTO MATEMÁTICO').pack(anchor='w',padx=12,pady=(4,5))
        resultado=tk.Text(padre,height=7,font=('Consolas',10),bg=PANEL,fg=TEXT,relief='flat',wrap='word',state='disabled')
        resultado.pack(fill='x',padx=12,pady=(0,10))
        self.entradas[modo,'resultado']=resultado
        marco=tk.Frame(padre,bg=BG)
        marco.pack(fill='both',expand=True,padx=12,pady=(0,10))
        columnas=('numero','pareja','ascii','antes','despues')
        tabla=ttk.Treeview(marco,columns=columnas,show='headings',height=7)
        for columna,titulo,ancho in [('numero','#',45),('pareja','PAREJA',110),('ascii','ASCII (3+3)',145),('antes','BLOQUE m',150),('despues','BLOQUE c',150)]:
            tabla.heading(columna,text=titulo)
            tabla.column(columna,width=ancho,anchor='center')
        scroll=ttk.Scrollbar(marco,orient='vertical',command=tabla.yview)
        tabla.configure(yscrollcommand=scroll.set)
        tabla.pack(side='left',fill='both',expand=True)
        scroll.pack(side='right',fill='y')
        self.entradas[modo,'tabla']=tabla
        if modo=='enc':
            self.ejecutar('enc')

    def ejecutar(self,modo):
        self.limpiar_resultados(modo)
        if modo=='enc':
            self.ultimo=None
        try:
            p=self.entradas[modo,'p'].get()
            q=self.entradas[modo,'q'].get()
            e=self.entradas[modo,'e'].get()
            if modo=='enc':
                mensaje=self.entradas[modo,'mensaje'].get('1.0','end-1c')
                datos=encriptar(mensaje,p,q,e)
                self.ultimo=datos
                lineas=[f"LLAVE PÚBLICA (e, n): ({datos['e']}, {datos['n']})",f"n = p × q = {datos['n']}     φ(n) = (p−1)(q−1) = {datos['phi']}",f"MCD(e, φ) = {datos['mcd']}",f"LONGITUD ORIGINAL L = {datos['L']}     RELLENO = {'SÍ (un espacio)' if datos['relleno'] else 'NO'}",f"CIFRADO C = {datos['C']}","Fórmula por bloque: c = m^e mod n"]
            else:
                datos=desencriptar(self.entradas[modo,'C'].get('1.0','end-1c'),self.entradas[modo,'L'].get(),p,q,e)
                lineas=[f"n = {datos['n']}     φ(n) = {datos['phi']}     MCD(e, φ) = {datos['mcd']}",f"LLAVE PRIVADA (d, n): ({datos['d']}, {datos['n']})",f"Comprobación: (e × d) mod φ = {(datos['e']*datos['d'])%datos['phi']}",f"LONGITUD L = {datos['L']}     RELLENO = {'SÍ (retirado exactamente uno)' if datos['relleno'] else 'NO'}",f"MENSAJE RECUPERADO = {datos['mensaje']!r}","Fórmula por bloque: m = c^d mod n"]
            resultado=self.entradas[modo,'resultado']
            resultado.configure(state='normal')
            resultado.delete('1.0','end')
            resultado.insert('1.0','\n'.join(lineas))
            resultado.configure(state='disabled')
            tabla=self.entradas[modo,'tabla']
            tabla.delete(*tabla.get_children())
            for i,fila in enumerate(datos['filas'],1):
                tabla.insert('', 'end',values=(i,repr(fila['pareja']),fila['ascii'],f"{fila['m']:06d}",fila['cifrado']))
        except ValueError as exc:
            messagebox.showerror('Validación de datos',str(exc))

    def limpiar_resultados(self,modo):
        resultado=self.entradas[modo,'resultado']
        resultado.configure(state='normal')
        resultado.delete('1.0','end')
        resultado.configure(state='disabled')
        tabla=self.entradas[modo,'tabla']
        tabla.delete(*tabla.get_children())

    def transferir(self):
        datos=getattr(self,'ultimo',None)
        if datos is None:
            messagebox.showinfo('Aviso','Primero encripte un mensaje.')
            return
        self.limpiar_resultados('dec')
        for clave in ('p','q','e'):
            entrada=self.entradas['dec',clave]
            entrada.delete(0,'end')
            entrada.insert(0,str(datos[clave]))
        campo=self.entradas['dec','C']
        campo.delete('1.0','end')
        campo.insert('1.0',datos['C'])
        largo=self.entradas['dec','L']
        largo.delete(0,'end')
        largo.insert(0,str(datos['L']))
        self.tabs.select(1)
        messagebox.showinfo('Cifrado recibido','Cifrado recibido correctamente. Presiona DESENCRIPTAR para recuperar el mensaje original')

if __name__=='__main__':
    Aplicacion().mainloop()
