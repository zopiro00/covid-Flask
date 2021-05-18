from types import MethodDescriptorType, MethodType
from flask import render_template, request, url_for
from covid import app

import csv
import json


#Abrir casos con csv mediante lista
@app.route("/provincias")
def provincias():
    file = open("data/provincias.csv", "r", encoding="utf8")
    csvreader = csv.reader(file, delimiter=",")

    lista =[]
    for registro in csvreader:
        d = {"codigo": registro[0], "valor": registro[1]}
        lista.append(d)

    file.close()
    print(lista)
    return  json.dumps(lista) 
"""
# Abrir casos mediante dict reader. Abre un diccionario
@app.route("/casosprovincias")
def casosprovincias():
    file = open("data/casos_diagnostico_provincia.csv", "r", encoding="utf8")
    
    dictreader = csv.DictReader(file)
    lista = []
    for registro in dictreader:
        lista.append(registro)
    return  json.dumps(lista)  
"""
@app.route("/provincia/<codigo>")
def laprovincia(codigo):
    file = open("data/provincias.csv", "r", encoding="utf8")
    
    dictreader = csv.DictReader(file, fieldnames=["codigo","provincia"])
    
    for i in dictreader:
        if i["codigo"] == codigo:
            return i["provincia"]
    file.close()
    return "Esa provincia no existe. Lago de Aquí!!"

@app.route("/casos/<int:year>", defaults={"mes":None, "dia":None})
@app.route("/casos/<int:year>/<int:mes>", defaults={"dia":None})
@app.route("/casos/<int:year>/<int:mes>/<int:dia>")
def casos(year, mes, dia):
    if not mes:
            fecha = "{:04d}".format(year)
    elif not dia:
        fecha = "{:04d}-{:02d}".format(year, mes)
    else:
        fecha = "{:04d}-{:02d}-{:02d}".format(year, mes, dia)

    file = open("data/casos_diagnostico_provincia.csv", "r", encoding="utf8")
    dictreader = csv.DictReader(file)

    casos_dia = 0 
    res = {
            "num_casos": 0,
            "num_casos_prueba_pcr": 0,
            "num_casos_prueba_test_ac": 0,
            "num_casos_prueba_ag": 0,
            "num_casos_prueba_elisa": 0,
            "num_casos_prueba_desconocida": 0}

    for i in dictreader:
        if fecha in i["fecha"]:
            for clave in res:
                res[clave] += int(i[clave])     
        elif i["fecha"] > fecha:
            break

    file.close()
    return  json.dumps(res)

@app.route("/incidenciasdiarias", methods = ['GET', 'POST'])
def incidencia():
    if request.method == 'GET':
        return render_template("alta.html")

    valores = request.form
    #Valorar num_casos_prueba_pcr >= 0 y entero
    try:
        num_pcr = int(valores["num_casos_prueba_pcr"])
        if num_pcr < 0:
            raise ValueError("EL número debe ser entero")
    except ValueError:
        return render_template("alta.html", casos_pcr=valores.num_casos_prueba_pcr)
    