from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, SubmitField
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

    id_cliente = SelectField(
        "Cliente",
        choices=[],
        coerce=int,
        validators=[
            DataRequired(
                message="Debe seleccionar un cliente."
            )
        ]
    )

    id_producto = SelectField(
        "Producto",
        choices=[],
        coerce=int,
        validators=[
            DataRequired(
                message="Debe seleccionar un producto."
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