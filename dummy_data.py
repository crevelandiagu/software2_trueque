from app_init import app

from app.models import Elementos, Usuarios
from app.models import db

def insert_dummy_data():

    with app.app_context():
        us = [[
            'polo', 'polo@polo.com', '1317dfa6a0c51245a1fbd37c6de9819ac469d2e5f71f70a42eec6c6181a30fa7', 'polo', 'polo', 'polo'
        ], [
            'a', 'a@a.com', 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb', 'a', 'a', 'a'
        ]]
        for x in us:
            print(x)
            nuevo_usuario = Usuarios(
                nombre=x[0],
                email=x[1],
                contrasena=x[2],
                departamento=x[3],
                municipio=x[4],
                direccion=x[5])

            # Elementos.insertar[nuevo_usuario]
            db.session.add(nuevo_usuario)
            db.session.commit()

        el= [[
            'audifonos', 'audifono logitec', 'audifono_logitec.png','5',150000,1
        ],[
            'Chromecast', 'chromecast salmon', 'chromecast.png','5',500000,2
        ],[
            'ipad', 'ipad pro', 'ipad.jpeg', '5', 1500000, 2
        ],[
            'huawei mate', 'huawei mate 20 ', 'HUAWEI_MATE20.png', '5', 1500000, 1
        ],[
            'iphone12', 'iphone 12 Pro ', 'iphone_12_PNG3.png', '5', 3500000, 1
        ]]
        for x in el:
            print(x)

            nuevo_elemento = Elementos(
                nombre=x[0],
                precio_estimado=x[4],
                descripcion=x[1],
                imagen_url=x[2],
                categoria=5,
                trocador=x[5]
            )
            # Elementos.insertar[nuevo_usuario]
            db.session.add(nuevo_elemento)
            db.session.commit()

if __name__ == "__main__":
    insert_dummy_data()