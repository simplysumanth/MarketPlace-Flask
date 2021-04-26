from market import app
from flask import render_template,redirect,url_for,flash,request
from market.models import Item,User
from market.forms import RegisterForm,LoginForm,PurchaseItemForm,SellItemForm,AdminAddItemForm,AdminUpdateItemForm,AdminDeleteItemForm
from market import db
from flask_login import login_user,logout_user,login_required,current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market',methods = ['GET','POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        #Purchase Item Logic
        purchased_item = request.form.get("purchased_item") #comes from form->input name from items_modals.html
        p_item_object = Item.query.filter_by(name=purchased_item).first()    
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"You have purchased {p_item_object.name} for ${p_item_object.price} Current Balance: {current_user.budget}",category='success')
            else:
                flash(f"Insufficient Balance to buy {p_item_object.name}",category="danger")
        #Sell Item Logic
        sold_item = request.form.get("sold_item")
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"You have sold {s_item_object.name} for ${s_item_object.price} Current Balance: {current_user.budget}",category='success')
            else:
                flash(f"Something went wrong in selling {s_item_object.name}")
        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html',items=items,purchase_form=purchase_form,owned_items=owned_items,selling_form=selling_form)

@app.route('/admin',methods=['GET','POST'])
def admin_page():
    admin_add_item_form = AdminAddItemForm()
    admin_update_item_form = AdminUpdateItemForm()
    admin_delete_item_form = AdminDeleteItemForm()
 
    if request.method == "GET":
        items = Item.query.all()
        users = User.query.all()
        owned_users = []
        for item in items:
            owned_users.append(User.query.filter_by(id=item.owner))
        return render_template('admin.html',items=items,owned_users=owned_users,users=users,
        admin_add_item_form=admin_add_item_form,admin_update_item_form=admin_update_item_form,admin_delete_item_form=admin_delete_item_form)
    
    if request.form["submit"]=="Add Item":
        if request.method == "POST":
            item_to_add = Item(name = admin_add_item_form.name.data,
                                barcode=admin_add_item_form.barcode.data,
                                price=admin_add_item_form.price.data,
                                description=admin_add_item_form.desc.data)
            db.session.add(item_to_add)
            db.session.commit()
            flash('Item succesfully added',category='success')
            return redirect(url_for("admin_page"))
    
    if request.form["submit"]=="Update Item":
        if request.method == "POST":
            updated_item = request.form.get("updated_item")
            to_be_updated = Item.query.filter_by(id=updated_item).first()
            to_be_updated.name = admin_update_item_form.name.data
            to_be_updated.barcode = admin_update_item_form.barcode.data
            to_be_updated.price = admin_update_item_form.price.data
            to_be_updated.description = admin_update_item_form.desc.data
            db.session.commit()
            flash("Item updated",category="success")
            return redirect(url_for("admin_page"))
    
    if request.form["submit"]=="Delete Item":
        if request.method == "POST":
            deleted_item = request.form.get("deleted_item")
            Item.query.filter_by(id=deleted_item).delete()
            db.session.commit()
            flash("Item deleted",category="success")
            return redirect(url_for("admin_page"))

@app.route('/register',methods = ['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username = form.username.data,
                              email_address = form.email_address.data,
                              password = form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created. You are now logged in as {user_to_create.username.capitalize()}",category='success')

        return redirect(url_for('market_page'))
    if form.errors != {}: #If there are no errors from validations
        for err_msg in form.errors.values():
            flash(f'{err_msg}',category='danger')

    return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password = form.password.data):
            if attempted_user.username == 'admin':
                login_user(attempted_user)
                flash("Welcome Admin",category="success")
                return redirect(url_for('admin_page'))
            else:
                login_user(attempted_user)
                flash(f"Login Successfull! Welcome: {attempted_user.username.capitalize()}",category='success')
                return redirect(url_for('market_page'))
        else:
            flash('Username and password not matched',category = 'danger')

    return render_template('login.html',form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out.',category='info')
    return render_template('home.html')
