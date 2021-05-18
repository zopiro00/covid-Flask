from covid import app

import csv
import json

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

# Abrir casos mediante dict reader
@app.route("/casosprovincias")
def casosprovincias():
    file = open("data/casos_diagnostico_provincia.csv", "r", encoding="utf8")
    
    dictreader = csv.DictReader(file)

    lista = []
    for registro in dictreader:
        lista.append(registro)
    return  json.dumps(lista)  

@app.route("/provincia/<codigo>")
def laprovincia(codigo):
    file = open("data/provincias.csv", "r", encoding="utf8")
    
    dictreader = csv.DictReader(file, fieldnames=["codigo","provincia"])
    
    for i in dictreader:
        if i["codigo"] == codigo:
            return i["provincia"]
    file.close()
    return "Esa provincia no existe. Lago de Aquí!!"

# Punto extra. Es como mucho arroz para el lunes @app.route("/casos/<int:year>/<int:mes>", defaults={"dia":None})
@app.route("/casos/<int:year>/<int:mes>/<int:dia>")
def casos(year, mes, dia):
    file = open("data/casos_diagnostico_provincia.csv", "r", encoding="utf8")
    
    dictreader = csv.DictReader(file)
    print(dictreader)
    file.close()
    return  json.dumps(dictreader)  

