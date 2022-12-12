from typing import Any
import hashlib

class Usuario:

    # class variable shared by all instances
    def __init__(self,
                 nombre=None,
                 email=None,
                 contrasena=None,
                 departamento=None,
                 municipio=None,
                 direccion=None):
        self.__nombre = nombre
        self.__email = email
        self.__contrasena = contrasena
        self.__departamento = departamento
        self.__municipio = municipio
        self.__direccion = direccion

    def get_nombre(self):
        return self.__nombre

    def get_email(self):
        return self.__email

    def get_contrasena(self):
        return self.__contrasena

    def get_departamento(self):
        return self.__departamento

    def get_municipio(self):
        return self.__municipio

    def get_direccion(self):
        return self.__direccion

    def encriptar_clave(self, contrasena):
        if self.__contrasena != contrasena:
            return False
        else:
            m = hashlib.sha256()
            m.update(bytes(self.__contrasena, encoding='utf-8'))
            return m.hexdigest()

    def validar_hash(self):
        m = hashlib.sha256()
        m.update(bytes(self.__contrasena, encoding='utf-8'))
        return m.hexdigest()




    # def set_nombre(self, nombre):
    #     self.__nombre = nombre
    #
    # def set_email(self, email):
    #     self.__email = email
    #
    # def set_contrasena(self, contrasena):
    #     self.__contrasena = contrasena
    #
    # def set_departamento(self, departamento):
    #     self.__departamento = departamento
    #
    # def set_municipio(self, municipio):
    #     self.__municipio = municipio
    #
    # def set_direccion(self, direccion):
    #     self.__direccion = direccion
