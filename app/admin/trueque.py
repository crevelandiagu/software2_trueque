from typing import Any
import hashlib
from app.admin.elemento import Elemento
class Trueque:

    # class variable shared by all instances
    def __init__(self,
                 elemento_oferta=None,
                 elemento_puja=None,
                 estado=None,
                 usuario_ofertador=None,
                 usuario_pujador=None
                 ):
        self.__elemento_oferta = elemento_oferta
        self.__elemento_puja = elemento_puja
        self.__estado = estado
        self.__usuario_ofertador = usuario_ofertador
        self.__usuario_pujador = usuario_pujador

    def get_elemento_oferta (self):
        return self.__elemento_oferta

    def get_elemento_puja(self):
        return self.__elemento_puja

    def get_estado(self):
        return self.__estado

    def get_usuario_ofertador(self):
        return self.__usuario_ofertador

    def get_usuario_pujador(self):
        return self.__usuario_pujador

    def procesar_trueque(self):
        pass





