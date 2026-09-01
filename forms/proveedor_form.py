from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class ProveedorForm(FlaskForm):

    nombre = StringField(
        "Nombre del proveedor",
        validators=[
            DataRequired(
                message="El nombre del proveedor es obligatorio."
            ),
            Length(
                min=3,
                max=100,
                message="El nombre debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    descripcion = StringField(
        "Descripción",
        validators=[
            DataRequired(
                message="La descripción es obligatoria."
            ),
            Length(
                min=5,
                max=200,
                message="La descripción debe tener entre 5 y 200 caracteres."
            )
        ]
    )

    estado = SelectField(
        "Estado",
        choices=[
            ("", "Seleccione un estado"),
            ("Activo", "Activo"),
            ("Inactivo", "Inactivo")
        ],
        validators=[
            DataRequired(
                message="Debe seleccionar un estado."
            )
        ]
    )

    enviar = SubmitField("Registrar proveedor")