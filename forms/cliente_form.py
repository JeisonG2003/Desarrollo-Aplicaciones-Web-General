from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ClienteForm(FlaskForm):

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

    enviar = SubmitField("Registrar cliente")