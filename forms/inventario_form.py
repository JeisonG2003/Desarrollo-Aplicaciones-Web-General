from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length


class MovimientoInventarioForm(FlaskForm):
    id_producto = SelectField(
        "Producto", choices=[], coerce=int,
        validators=[DataRequired(message="Seleccione un producto.")]
    )
    tipo = SelectField(
        "Tipo de movimiento",
        choices=[
            ("ENTRADA", "Entrada de inventario"),
            ("AJUSTE_ENTRADA", "Ajuste de entrada"),
            ("AJUSTE_SALIDA", "Ajuste de salida")
        ],
        validators=[DataRequired(message="Seleccione un tipo de movimiento.")]
    )
    cantidad = IntegerField(
        "Cantidad",
        validators=[DataRequired(message="Ingrese una cantidad."), NumberRange(min=1, message="La cantidad debe ser mayor que cero.")]
    )
    motivo = TextAreaField(
        "Motivo / referencia",
        validators=[DataRequired(message="Indique el motivo del movimiento."), Length(min=3, max=300)]
    )
    enviar = SubmitField("Registrar movimiento")
