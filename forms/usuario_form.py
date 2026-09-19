from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class UsuarioForm(FlaskForm):

    usuario = StringField(
        "Usuario",
        validators=[
            DataRequired(message="Ingrese un nombre de usuario."),
            Length(
                min=3,
                max=50,
                message="El usuario debe tener entre 3 y 50 caracteres."
            )
        ]
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(message="Ingrese una contraseña."),
            Length(
                min=6,
                max=100,
                message="La contraseña debe tener al menos 6 caracteres."
            )
        ]
    )

    confirmar_password = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired(message="Confirme su contraseña."),
            EqualTo(
                "password",
                message="Las contraseñas deben coincidir."
            )
        ]
    )

    enviar = SubmitField("Registrar usuario")