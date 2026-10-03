from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, HiddenField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional, Length


class FacturacionForm(FlaskForm):
    numero = StringField(
        "Número de factura",
        validators=[Optional()]
    )

    id_cliente = SelectField(
        "Cliente",
        choices=[],
        coerce=int,
        validators=[DataRequired(message="Debe seleccionar un cliente.")]
    )

    forma_pago = SelectField(
        "Forma de pago",
        choices=[
            ("01", "Efectivo / sin utilización del sistema financiero"),
            ("20", "Transferencia, tarjeta u otro medio financiero")
        ],
        validators=[DataRequired(message="Seleccione una forma de pago.")]
    )

    detalle_json = HiddenField(
        "Detalle",
        validators=[DataRequired(message="Agregue al menos un producto a la factura.")]
    )

    observaciones = TextAreaField(
        "Observaciones",
        validators=[Optional(), Length(max=300, message="Máximo 300 caracteres.")]
    )

    enviar = SubmitField("Emitir factura")


class AnularFacturaForm(FlaskForm):
    motivo = TextAreaField(
        "Motivo de anulación",
        validators=[
            DataRequired(message="Indique el motivo de la anulación."),
            Length(min=4, max=300, message="El motivo debe tener entre 4 y 300 caracteres.")
        ]
    )
    enviar = SubmitField("Anular factura")
