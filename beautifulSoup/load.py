# -*- coding: utf-8 -*-
#!/usr/bin/env python
from tkinter import *
from tkinter import messagebox
import bs4 as bs
import urllib.request
from tkinter import messagebox
from tkinter import *
import os
import sqlite3

def open_url(url,file):
    try:
        if os.path.exists(file):
                f = urllib.request.urlretrieve(url,file)
        else:
            f = urllib.request.urlretrieve(url,file)
        return file
    except:
        print  ("Error al conectarse a la página")
        return None


def get_data_categoria():
    count = 0
    fichero = "categorias"
    txt = open (r'C:\Users\Carmen\Documents\Universidad software\Cuarto_1920\Primer cuatrimestre\Accesos inteligente a la informacion (AII)\Aii\Proyecto\proyecto-aii\proyecto\principal\data\caterogias.txt','w', encoding="utf-8")
    url = "https://cocina-online.com/"
    if open_url(url,fichero):        
        f = open (fichero, encoding="utf8").read()
        soup = bs.BeautifulSoup(f, "lxml")
        categorias = soup.find('nav', {"id": "sideBar"}).find_all('ul')[0].find_all('li')
        for aux in categorias:
            titulo = aux.a.text
            url = aux.a.get("href")
            if url == 'https://cocina-online.com/recetas-de-cócteles-1/':
                url = url.replace('ó', 'o')
            if open_url(url,fichero):
                f = open (fichero, encoding="utf8").read()
                soup = bs.BeautifulSoup(f, "lxml")
                descripcion = soup.find('main', {"id": "section"}).find_all('article')[0].find_all('p')[0].text
            count = count + 1
            txt.write(str(count)+"||"+titulo+"||"+descripcion+"\n")
    messagebox.showinfo("Categorías de la web", "Las categorías se han cargado correctamente. \nHay " + str(count) + " categorías")
    txt.close()

def get_data_recetas():
    count = 0
    fichero = "recetas"
    txt = open (r'C:\Users\Carmen\Documents\Universidad software\Cuarto_1920\Primer cuatrimestre\Accesos inteligente a la informacion (AII)\Aii\Proyecto\proyecto-aii\proyecto\principal\data\recetas.txt','w', encoding="utf-8")
    url = "https://cocina-online.com/"
    if open_url(url,fichero):        
        f = open (fichero, encoding="utf8").read()
        soup = bs.BeautifulSoup(f, "lxml")
        categorias = soup.find('nav', {"id": "sideBar"}).find_all('ul')[0].find_all('li')
        categoria_id = 1
        for aux in categorias:
            url = aux.a.get("href")
            if url == 'https://cocina-online.com/recetas-de-cócteles-1/':
                url = url.replace('ó', 'o')
            if open_url(url,fichero):
                f = open (fichero, encoding="utf8").read()
                soup = bs.BeautifulSoup(f, "lxml")
                recetas = soup.find_all('div', {"class": "brd"})
                for recetas_aux in recetas:
                    pdf_url = recetas_aux.find('aside', {"id": "rIcons"}).a.get("href")
                    titulo = recetas_aux.find_all('p')[0].a.text
                    url_aux = recetas_aux.find_all('p')[0].a.get("href")
                    aux_informacion = recetas_aux.find_all('p')[1].text
                    aux_informacion = aux_informacion.split('\n')
                    dificultad = aux_informacion[1].split(':')
                    dificultad = dificultad[1].replace('\xa0', '')
                    cocina = aux_informacion[2].split(':')
                    cocina = cocina[1].replace('\xa0', '')
                    vegetariana = aux_informacion[3].split(':')
                    vegetariana = vegetariana[1].replace('\xa0', '')
                    celiacos = aux_informacion[4].split(':')
                    celiacos = celiacos[1].replace('\xa0', '')
                    if open_url(url_aux,fichero):
                        try:
                            f = open (fichero, encoding="utf8").read()
                        except:
                            f = open (fichero).read()
                        soup = bs.BeautifulSoup(f, "lxml")
                        foto = soup.find('main', {'id': 'section'}).find('article').find('header').img.get('src')
                        if foto == "https://cocina-online.com/icon/alta.png" or foto == "https://cocina-online.com/icon/media.png" or foto == "https://cocina-online.com/icon/baja.png":
                            foto = "https://image.freepik.com/foto-gratis/plato-vacio-vaso-agua-fondo-blanco-concepto-ayuno-medico_79830-768.jpg"
                        ingrediente = soup.find('main', {'id': 'section'}).find_all('p')[0].text
                        ingrediente = ingrediente.split('\n')
                        ingredientes = ""
                        for ingrediente_aux in ingrediente:
                            ingrediente_aux = ingrediente_aux.replace('-', '')
                            ingrediente_aux = ingrediente_aux.replace('•', '')
                            ingrediente_aux = ingrediente_aux.replace('.', '')
                            if ingrediente_aux != "":
                                ingrediente_aux = ingrediente_aux.replace(':', '')
                                ingredientes = ingredientes + ingrediente_aux + ":::::"
                        paso = soup.find('main', {'id': 'section'}).find_all('p')[1].text
                        paso = paso.split('\n')
                        pasos = ""
                        for paso_aux in paso:
                            if paso_aux != "":
                                pasos = pasos + paso_aux
                        count = count + 1
                        txt.write(str(count)+"||"+str(categoria_id)+"||"+titulo+"||"+pdf_url+
                                    "||"+dificultad+"||"+cocina+"||"+vegetariana+"||"+celiacos+"||"+foto+
                                    "||"+ingredientes+"||"+pasos+"\n")
                categoria_id = categoria_id + 1
    messagebox.showinfo("Recetas de la web", "Las recetas se han cargado correctamente. \nHay " + str(count) + " recetas")
    txt.close()

def get_data_usuarios():
    count = 0
    fichero = "usuarios"
    txt = open (r'C:\Users\Carmen\Documents\Universidad software\Cuarto_1920\Primer cuatrimestre\Accesos inteligente a la informacion (AII)\Aii\Proyecto\proyecto-aii\proyecto\principal\data\usuarios.txt','w', encoding="utf-8")
    url = "https://www.aboutespanol.com/los-200-nombres-de-bebe-en-espanol-mas-populares-1176840"
    if open_url(url,fichero):        
        f = open (fichero, encoding="utf8").read()
        soup = bs.BeautifulSoup(f, "lxml")
        usuarios = soup.find('div', {"class": "mntl-sc-block-table__table-wrapper"}).find_all('tr')
        for aux in usuarios:
            aux1 = aux.find_all('td')
            if aux1[1].text != "Nombres de niña":
                nombre = aux1[1].text
                sexo = "M"
                count = count + 1
                txt.write(str(count)+"||"+nombre+"||"+sexo+"\n")
                nombre = aux1[2].text
                sexo = "H"
                count = count + 1
                txt.write(str(count)+"||"+nombre+"||"+sexo+"\n")
    messagebox.showinfo("Usuarios de la web", "Las usuarios se han cargado correctamente. \nHay " + str(count) + " usuarios")
    txt.close()

def ventana_principal():
    top = Tk()
    top.title("Extaer datos")

    def close_window():
        top.destroy()

    categorias = Button(top, text="Extaer categorias", background="pink", activeforeground="#F50743", command = get_data_categoria)
    recetas = Button(top, text="Extaer recetas de cocina", background="pink", activeforeground="#F50743", command = get_data_recetas)
    usuarios = Button(top, text="Extaer usuarios", background="pink", activeforeground="#F50743", command = get_data_usuarios)
    cerrar = Button(top, text="Cerrar", background="green", activeforeground="#F50743", command = close_window)
    categorias.pack(side = LEFT)
    recetas.pack(side = LEFT)
    usuarios.pack(side = LEFT)
    cerrar.pack(side = LEFT)
    top.mainloop()

if __name__ == "__main__":
    ventana_principal()