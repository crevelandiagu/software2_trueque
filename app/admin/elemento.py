
class Elemento:

    # class variable shared by all instances
    def __init__(self, nombre, descripcion, imagen_url, categoria, trocador):

        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__imagen_url = imagen_url
        self.__categoria = categoria
        self.__trocador = trocador
