from principal.recommendations import  transformPrefs, calculateSimilarItems, getRecommendations, getRecommendedItems, topMatches
from django.shortcuts import render, redirect, get_object_or_404
from principal.models import Categoria, Receta, Usuario, Valoracion
from django.db.models import Avg
import sqlite3
import shelve
import os
from .forms import CatForm

def welcome(request):
    recetas = Receta.objects.annotate(avg_rating=Avg("valoracion__puntuacion")).order_by("-avg_rating")[:3]
    return render(request, "users/welcome.html", {"recetas": recetas})

def show_all(request):
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        cat = CatForm(request.POST)
        selected_value = request.POST['cat']
        print(selected_value)
        recetas = Receta.objects.filter(categoria_id = selected_value)
        return render(
                request,
                "users/show_all.html",
                {"recetas": recetas, "categorias": categorias},
            )
    else:
        recetas = Receta.objects.filter(categoria_id = 1)
        return render(request, "users/show_all.html", {"recetas": recetas, "categorias": categorias})

def mostrar_receta(request, id_receta):
    receta1 = Receta.objects.get(id_receta = id_receta)

    ingredientes = receta1.ingredientes.split(':::::')
    ingredientes = ingredientes[:-1]
    
    shelf = shelve.open("dataRS.dat")
    ItemsPrefs = shelf['ItemsPrefs']
    shelf.close()
    recommended = topMatches(ItemsPrefs, int(id_receta),n=6)
    recetas = []
    similar = []
    for re in recommended:
        recetas.append(Receta.objects.get(pk=re[1]))
        similar.append(re[0])
    items= zip(recetas,similar)

    return render(request, 'users/mostrar_receta.html', {"ingredientes": ingredientes, "receta1": receta1, "recetas": recetas, 'items': items})

################################
##       Cargar datos         ##
################################
def cargar_datos(request):
    Categoria.objects.all().delete()
    Receta.objects.all().delete()
    Usuario.objects.all().delete()
    Valoracion.objects.all().delete()

    module_dir = os.path.dirname(__file__)
    with open(module_dir + "/data/caterogias.txt", "r", encoding="utf8", errors="ignore") as f:
        print("Cargando categorias...")
        lines = f.read().splitlines()
        categorias = []
        for line in lines:
            if line == "":
                continue
            categoria = line.split("||")
            categoria_id = categoria[0]
            titulo = categoria[1]
            descripcion = categoria[2]
            categorias.append(Categoria(categoria_id=categoria_id , titulo=titulo, descripcion=descripcion))
        Categoria.objects.bulk_create(categorias)
        print("...categorias cargadas!")

    with open(module_dir + "/data/recetas.txt", "r", encoding="utf8", errors="ignore") as f:
        print("Cargando recetas...")
        lines = f.read().splitlines()
        recetas = []
        for line in lines:
            if line == "":
                continue
            receta = line.split("||")
            id_receta = receta[0]
            categoria_id = receta[1]
            titulo = receta[2]
            pdf_url = receta[3]
            dificultad = receta[4]
            cocina = receta[5]
            vegetariana = receta[6]
            celiacos = receta[7]
            foto = receta[8]
            ingredientes = receta[9]
            pasos = receta[10]
            recetas.append(Receta(id_receta=id_receta ,categoria_id=categoria_id, titulo=titulo, dificultad=dificultad,
                                pdf_url=pdf_url, cocina=cocina, vegetariana=vegetariana, celiacos=celiacos,
                                foto=foto, ingredientes=ingredientes, pasos=pasos))
        Receta.objects.bulk_create(recetas)
        print("...recetas cargadas!")

    with open(module_dir + "/data/usuarios.txt", "r", encoding="utf8", errors="ignore") as f:
        print("Cargando usuarios...")
        lines = f.read().splitlines()
        usuarios = []
        for line in lines:
            if line == "":
                continue
            usuario = line.split("||")
            id_usuario = usuario[0]
            nombre = usuario[1]
            sexo = usuario[2]
            usuarios.append(Usuario(id_usuario=id_usuario , nombre=nombre, sexo=sexo))
        Usuario.objects.bulk_create(usuarios)
        print("...usuarios cargadas!")

    ## https://www.generatedata.com/
    with open(module_dir + "/data/valoracion.txt", "r", encoding="utf8", errors="ignore") as f:
        print("Cargando valoraciones...")
        lines = f.read().splitlines()
        valoraciones = []
        for line in lines:
            if line == "":
                continue
            valoracion = line.split("|")
            puntuacion = valoracion[0]
            receta_id = valoracion[1]
            usuario_id = valoracion[2]
            valoraciones.append(Valoracion(puntuacion=puntuacion, receta_id=receta_id, usuario_id=usuario_id))
        Valoracion.objects.bulk_create(valoraciones)
        print("...valoraciones cargadas!")
    recetas = Receta.objects.annotate(avg_rating=Avg("valoracion__puntuacion")).order_by("-avg_rating")[:3]   
    return render(request, "users/load_data_success.html", {"recetas": recetas})

################################
##  Sistemas de recomendación ##
################################
def loadDict():
    Prefs={}   
    shelf = shelve.open("dataRS.dat")
    ratings = Valoracion.objects.all()
    for ra in ratings:
        user = int(ra.usuario_id)
        itemid = int(ra.receta.id_receta)
        rating = float(ra.puntuacion)
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating
    shelf['Prefs']=Prefs
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf.close()

def loadRS(request):
    loadDict()
    recetas = Receta.objects.annotate(avg_rating=Avg("valoracion__puntuacion")).order_by("-avg_rating")[:3]
    return render(request,'users/loadRS.html', {"recetas": recetas})