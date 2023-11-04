from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class AnimalProfileForm(FlaskForm):
    type_id = SelectField('Animal Type', coerce=int, validators=[DataRequired()])
    breed_id = SelectField('Breed', coerce=int, validators=[DataRequired()])
    disposition_id = SelectField('Disposition', coerce=int, validators=[DataRequired()])
    availability_id = SelectField('Availability', coerce=int, validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    image = FileField('Animal Image', validators=[
        FileAllowed(['jpg', 'png', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Create Profile')
