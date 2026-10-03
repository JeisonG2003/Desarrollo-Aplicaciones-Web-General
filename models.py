from flask_login import UserMixin


class Usuario(UserMixin):
    def __init__(self, id, usuario, password, rol="USUARIO", estado="ACTIVO"):
        self.id = id
        self.usuario = usuario
        self.password = password
        self.rol = rol
        self.estado = estado

    @property
    def is_active(self):
        return self.estado == "ACTIVO"
from flask_login import UserMixin


class Usuario(UserMixin):
    def __init__(self, id, usuario, password, rol="USUARIO", estado="ACTIVO"):
        self.id = id
        self.usuario = usuario
        self.password = password
        self.rol = rol
        self.estado = estado

    @property
    def es_admin(self):
        return self.rol == "ADMIN"
