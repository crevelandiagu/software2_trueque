from typing import Any
import hashlib
from app.admin.elemento import Elemento
class SolicitudLogistica:

    # class variable shared by all instances
    def __init__(self,
                 numero_solicitud=None,
                 operador_logistico=None,
                 estado=None,
                 trueque=None,
                 ):
        self.__numero_solicitud= numero_solicitud
        self.__operador_logistico = operador_logistico
        self.__estado = estado
        self.__trueque = trueque

    def get_numero_solicitud (self):
        return self.__numero_solicitud

    def get_operador_logistico(self):
        return self.__operador_logistico

    def get_estado(self):
        return self.__estado

    def get_trueque(self):
        return self.__trueque

    def calculo_envio(self):
        pass




