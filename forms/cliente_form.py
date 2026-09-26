from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional


class ClienteForm(FlaskForm):

    cedula = StringField(
        "Cédula",
        validators=[
            Optional(),
            Length(
                min=10,
                max=20,
                message="La cédula debe tener entre 10 y 20 caracteres."
            )
        ]
    )

    nombre = StringField(
        "Nombre del cliente",
        validators=[
            DataRequired(
                message="El nombre del cliente es obligatorio."
            ),
            Length(
                min=3,
                max=100,
                message="El nombre debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    actividad = StringField(
        "Actividad",
        validators=[
            DataRequired(
                message="La actividad es obligatoria."
            ),
            Length(
                min=3,
                max=100,
                message="La actividad debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    ubicacion = StringField(
        "Ubicación",
        validators=[
            DataRequired(
                message="La ubicación es obligatoria."
            ),
            Length(
                min=3,
                max=100,
                message="La ubicación debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            Optional(),
            Length(
                min=7,
                max=20,
                message="El teléfono debe tener entre 7 y 20 caracteres."
            )
        ]
    )

    correo = StringField(
        "Correo electrónico",
        validators=[
            Optional(),
            Email(
                message="Ingrese un correo electrónico válido."
            ),
            Length(
                max=100,
                message="El correo no puede superar los 100 caracteres."
            )
        ]
    )

    enviar = SubmitField("Guardar cliente")