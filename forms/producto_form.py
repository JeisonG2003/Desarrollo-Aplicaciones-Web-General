from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange


class ProductoForm(FlaskForm):

    nombre = StringField(
        "Nombre del producto",
        validators=[
            DataRequired(
                message="El nombre del producto es obligatorio."
            ),
            Length(
                min=3,
                max=100,
                message="El nombre debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    categoria = SelectField(
        "Categoría",
        choices=[
            ("", "Seleccione una categoría"),
            ("Semillas", "Semillas"),
            ("Fertilizantes", "Fertilizantes"),
            ("Herramientas", "Herramientas")
        ],
        validators=[
            DataRequired(
                message="Debe seleccionar una categoría."
            )
        ]
    )

    precio = FloatField(
        "Precio",
        validators=[
            InputRequired(
                message="El precio es obligatorio."
            ),
            NumberRange(
                min=0,
                message="El precio no puede ser negativo."
            )
        ]
    )

    stock = IntegerField(
        "Stock",
        validators=[
            InputRequired(
                message="El stock es obligatorio."
            ),
            NumberRange(
                min=0,
                message="El stock no puede ser negativo."
            )
        ]
    )

    # --- CAMPO AÑADIDO PARA PROVEEDOR ---
    id_proveedor = SelectField(
        "Proveedor",
        choices=[],
        coerce=int,
        validators=[
            DataRequired(
                message="Debe seleccionar un proveedor."
            )
        ]
    )

    enviar = SubmitField(
        "Registrar producto"
    )