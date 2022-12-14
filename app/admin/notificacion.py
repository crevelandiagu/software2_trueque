
class Notificacion:

    # class variable shared by all instances
    def __init__(self,
                 estado=None,
                 usuario_ofertador=None,
                 usuario_pujador=None,
                 mensaje=None
                 ):

        self.__estado = estado
        self.__usuario_ofertador= usuario_ofertador
        self.__usuario_pujador= usuario_pujador
        self.__mensaje= mensaje



    def get_estado(self):
        return self.__estado

    def get_mensaje(self):
        return self.__mensaje

    def get_usuario_ofertador(self):
        return self.__usuario_ofertador

    def get_usuario_pujador(self):
        return self.__usuario_pujador

