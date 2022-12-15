import os
from werkzeug.utils import secure_filename

class Elemento:
    # class variable shared by all instances
    def __init__(self,
                 nombre=None,
                 descripcion=None,
                 imagen_url=None,
                 categoria=None,
                 precio_estimado=None,
                 estado=None,
                 trocador=None):
        self.__nombre = nombre
        self.__categoria = categoria
        self.__descripcion = descripcion
        self.__imagen_url = self.cargar_imagen(imagen_url)
        self.__estado = estado
        self.__precio_estimado= precio_estimado
        self.__trocador = trocador

    def get_nombre(self):
        return self.__nombre

    def get_descripcion(self):
        return self.__descripcion

    def get_imagen_url(self):
        return self.__imagen_url

    def get_categoria(self):
        return self.__categoria

    def get_precio_estimado(self):
        return self.__precio_estimado

    def get_trocador(self):
        return self.__trocador

    def validar_imagen(self, imagen):
        extenciones_permitidas = set(['jpeg', 'jpg', 'png', 'gif'])
        res = '.' in imagen and \
               imagen.rsplit('.', 1)[1] in extenciones_permitidas
        return res

    def cargar_imagen(self, imagen):
        if imagen and self.validar_imagen(imagen.filename):
            imagen_res = secure_filename(imagen.filename)
            imagen.save(os.path.join('static/uploads', imagen_res))
        return imagen_res