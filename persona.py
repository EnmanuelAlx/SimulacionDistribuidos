class Persona:
    def __init__(self, cedula, genero, fnac, edad, pais, estado, ciudad, profesion, ec, trabajo, vivePadres, tieneHermanos, cantHermanos):
        self._cedula = cedula
        self._genero = genero
        self._fnac = fnac
        self._edad = edad
        self._pais = pais
        self._estado = estado
        self._ciudad = ciudad
        self._profesion = profesion
        self._ec = ec
        self._trabajo = trabajo
        self._vivePadres = vivePadres
        self._tieneHermanos = tieneHermanos
        self._cantHermanos = cantHermanos

    def toDBCollection(self):
        return{
            "cedula": self._cedula,
            "genero": self._genero,
            "fecha_nacimiento": self._fnac,
            "edad": self._edad,
            "pais": self._pais,
            "estado": self._estado,
            "ciudad": self._ciudad,
            "profesion": self._profesion,
            "estadoCivil": self._ec,
            "tieneTrabajo": self._trabajo,
            "vivePadres": self._vivePadres,
            "tieneHermanos": self._tieneHermanos,
            "cantHermanos" : self._cantHermanos
        }

