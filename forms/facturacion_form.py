from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class FacturacionForm(FlaskForm):

    numero = StringField(
        "Número de factura",
        validators=[
            DataRequired(
                message="El número de factura es obligatorio."
            ),
            Length(
                min=3,
                max=20,
                message="El número de factura debe tener entre 3 y 20 caracteres."
            )
        ]
    )

    cliente = StringField(
        "Cliente",
        validators=[
            DataRequired(
                message="El cliente es obligatorio."
            ),
            Length(
                min=3,
                max=100,
                message="El nombre del cliente debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    producto = StringField(
        "Producto",
        validators=[
            DataRequired(
                message="El producto es obligatorio."
            ),
            Length(
                min=2,
                max=100,
                message="El producto debe tener entre 2 y 100 caracteres."
            )
        ]
    )

    total = FloatField(
        "Total",
        validators=[
            DataRequired(
                message="El total es obligatorio."
            ),
            NumberRange(
                min=0,
                message="El total no puede ser negativo."
            )
        ]
    )

    enviar = SubmitField("Registrar factura")