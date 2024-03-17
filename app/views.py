"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""
import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash, session, abort, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from app.models import PropertyProfile
from app.forms import createForm
from werkzeug.utils import secure_filename

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

#
#1
@app.route('/properties/')
def properties():
    """Renders the properties page."""
    properties = PropertyProfile.query.all()
    return render_template('properties.html', properties = properties)

#2
@app.route('/properties/create/', methods=['POST', 'GET'])
def create():
    form = createForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        rooms = form.rooms.data
        bathrooms = form.bathrooms.data
        price = form.price.data
        type = form.type.data
        location = form.location.data

        photo = form.photo.data
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        photo_path = filename
        property = PropertyProfile(title, description, rooms, bathrooms, price, type, location, filename)

        db.session.add(property)
        db.session.commit()
        flash('Property Added')
        return redirect(url_for('properties'))
    
    return render_template('create.html', form = form)

@app.route('/./properties/<propertyid>')
def propertyid():
    """Renders the respective <propertyid> page."""
    pass

@app.route('/properties/<int:propertyid>')
def property_id(propertyid):
    """Renders the respective property detail page."""
    property = PropertyProfile.query.get(propertyid)
    return render_template('property_id.html', property=property)

@app.route('/properties/<filename>')
def get_image(filename):
    return send_from_directory( os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename )