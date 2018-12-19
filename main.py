from persona import Persona
from pymongo import MongoClient
from datetime import datetime
from config import config
import random
import modeloprob as normal
import time
import mysql.connector
import argparse
import json

host, port = config()
mongoClient = MongoClient(host, port)
db = mongoClient.usuarios
collection = db.usuarios


def responder(db):
    id_preguntas = []
    prob = normal.Normal()
    respuesta = 0
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database=db
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT id_pregunta FROM preguntas")
    for x in mycursor.fetchall():
        id_preguntas.append(x[0])

    cursor = collection.find()    
    for usuario in cursor:
        for pregunta in id_preguntas:
            sql = "INSERT INTO respuestas (id_usuario, id_pregunta, id_respuesta) VALUES(%s ,%s, %s)"
            probabilidad = prob.generateProb()
            if(probabilidad<1):
                respuesta = 1
            elif(probabilidad > 1 and probabilidad<2):
                respuesta = 2
            elif(probabilidad > 2 and probabilidad<3):
                respuesta = 3
            elif(probabilidad > 3 and probabilidad<4):
                respuesta = 4
            elif(probabilidad > 4 and probabilidad<5):
                respuesta = 5
            val = (usuario['cedula'], pregunta, respuesta)
            mycursor.execute(sql, val)
            mydb.commit()
    

def generarCenso(cantPersonas, data, trabajos):
    inicio = datetime(1990, 1, 30)
    fin = datetime(2000, 12, 31)
    prob = normal.Normal()
    for i in range(1,cantPersonas+1):
        cantHermanos = 0;
        genero = random.randint(0,1)
        randomDate = inicio + (fin - inicio) * random.random()
        trabaja = (True if prob.generateProb()>1.5 else False)
        vivePadres = (True if prob.generateProb()>1.5 else False)
        tieneHermanos = (True if prob.generateProb()>1.5 else False)
        estadoCivil = ("S" if prob.generateProb()>1.5 else "C")
        edad = time.localtime(time.time()).tm_year - randomDate.year
        fechaNacimiento = "{}-{}-{}".format(randomDate.year, randomDate.month,randomDate.day)
        if(tieneHermanos):
            cantHermanos = round(prob.generateProb())
        pais, estado, ciudad = getPaisEstadoCiudad(data)
        trabajo = getTrabajo(trabajos)
        persona = Persona(i, genero,fechaNacimiento, edad,pais, estado, ciudad, trabajo, estadoCivil, trabaja, vivePadres, tieneHermanos, cantHermanos)
        collection.insert(persona.toDBCollection())


def getTrabajo(data):
    prob = normal.Normal(127, 30)
    pro1 = int(round(abs(prob.generateProb())))
    return (data[pro1])

def getPaisEstadoCiudad(data):
    prob = normal.Normal(123.5, 30)
    pro1 = round(abs(prob.generateProb()))
    p = 'Venezuela'
    estado = 'Bolivar'
    city = ''
    for pais in data:
        if(pais.get('id') == int(pro1)):
            p = pais.get('name')
            randState = random.randint(0, len(pais.get('states').items())-1)
            state = list(pais.get('states').items())[randState]
            estado = state[0]
            randCity = random.randint(0, len(state[1]))
            if(len(state[1]) > 0):
                city = state[1][randCity-1]
            else:
                city = estado
    return p, estado, city


def cargarDatos(ruta):
    with open(ruta) as contenido:
        resultado = json.load(contenido)
    return resultado


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cantPersonas',
                        help='Cantidad de personas',
                        type=int)
    arg = parser.parse_args()
    ruta = 'data/all.json'
    resultado = cargarDatos(ruta)
    trabajos = cargarDatos('data/works.json')
    generarCenso(arg.cantPersonas, resultado, trabajos)
    responder("instinto")
    responder("pensamiento")
    responder("sentimiento")

