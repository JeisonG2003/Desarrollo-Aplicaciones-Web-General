from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional


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

    enviar = SubmitField("Guardar proveedor")