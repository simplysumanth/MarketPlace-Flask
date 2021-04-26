from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length,EqualTo,Email,DataRequired,ValidationError
from market.models import User

class RegisterForm(FlaskForm):
    #FlaskForm will automatically go to validate_ methods and check if the field exists with the name after _ (that is username here)
    def validate_username(self,username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Try another one.')
    
    def validate_email_address(self,email_address_to_check):
        email = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email:
            raise ValidationError('Email Address already exists! Try another one.')

    username = StringField(label='User Name:',validators=[Length(min=2,max=30),DataRequired()])
    email_address = StringField(label='Email Address:',validators=[Email(),DataRequired()])
    password1 =  PasswordField(label='Password:',validators=[Length(min=6),DataRequired()])
    password2 =  PasswordField(label='Confirm Password:',validators=[EqualTo('password1'),DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='User Name:',validators=[DataRequired()])
    password = StringField(label='Password:',validators=[DataRequired()])
    submit = SubmitField(label='Signin')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item')

class SellItemForm(FlaskForm):
    submit = SubmitField(label="Sell Item")

class AdminAddItemForm(FlaskForm):
    name = StringField(label='Item Name:',validators=[Length(min=2,max=30),DataRequired()])
    barcode = StringField(label='Barcode: ',validators=[Length(min=13,max=13),DataRequired()])
    price =  StringField(label='Price:',validators=[DataRequired()])
    desc =  StringField(label='Description: ',validators=[DataRequired()])
    submit = SubmitField(label='Add Item')

class AdminUpdateItemForm(FlaskForm):
    name = StringField(label='Item Name:',validators=[Length(min=2,max=30),DataRequired()])
    barcode = StringField(label='Barcode: ',validators=[Length(min=13,max=13),DataRequired()])
    price =  StringField(label='Price:',validators=[DataRequired()])
    desc =  StringField(label='Description: ',validators=[DataRequired()])
    submit = SubmitField(label='Update Item')

class AdminDeleteItemForm(FlaskForm):
    submit = SubmitField(label="Delete Item")
