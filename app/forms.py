from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, BooleanField, SubmitField, widgets
from wtforms.validators import DataRequired, Optional

class AnimalSearchForm(FlaskForm):
    # A dropdown to select the type of animal
    type = SelectField('Type', choices=[
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('other', 'Other')
    ], validators=[Optional()])

    # A dropdown to select the breed
    breed = SelectField('Breed', choices=[
        ('labrador', 'Labrador'),
        ('persian', 'Persian'),
        ('siamese', 'Siamese'),
        # Add other common breeds here
        ('other', 'Other')
    ], validators=[Optional()])

    # Checkboxes for disposition
    good_with_animals = BooleanField('Good with other animals')
    good_with_children = BooleanField('Good with children')
    must_be_leashed = BooleanField('Animal must be leashed at all times')

    # A dropdown to select availability
    availability = SelectField('Availability', choices=[
        ('not_available', 'Not Available'),
        ('available', 'Available'),
        ('pending', 'Pending'),
        ('adopted', 'Adopted')
    ], validators=[Optional()])

    # A submit button for the search form
    submit = SubmitField('Search')

class AnimalProfileForm(FlaskForm):
    # Form fields for creating an animal profile
    type_name = StringField('Animal Type', validators=[DataRequired()])
    breed_name = StringField('Breed', validators=[DataRequired()])
    
    # We use SelectMultipleField for dispositions so that multiple can be selected
    dispositions = SelectMultipleField(
        'Dispositions',
        choices=[
            ('good_with_animals', 'Good with other animals'),
            ('good_with_children', 'Good with children'),
            ('must_be_leashed', 'Animal must be leashed at all times')
        ],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False),
        validators=[DataRequired()]
    )

    availability = SelectField('Availability', choices=[
        ('not_available', 'Not Available'),
        ('available', 'Available'),
        ('pending', 'Pending'),
        ('adopted', 'Adopted')
    ], validators=[DataRequired()])
    
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Profile')
