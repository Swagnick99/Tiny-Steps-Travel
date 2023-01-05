# from base64 import b32hexencode
from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from flask_login import current_user
from werkzeug.utils import secure_filename
from .models import BlogPost, TripPlan, booking
from . import db
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
import stripe

main = Blueprint("main", __name__)

stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

@main.route('/')
def index():
    blogs = BlogPost.query.order_by(BlogPost.date_posted.desc()).limit(4).all()

    return render_template("index.html", title="Home", blogs=blogs)

@main.route('/contact/<string:name>', methods=['GET', 'POST'])
def contact(name):
    if request.method == 'POST':
        username = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('sub')
        data = request.form.get('data')

        msg = EmailMessage()
        content = "Name: {}\nEmail: {}\n\n{}".format(username, email, data)
        msg.set_content(content)

        msg['Subject'] = subject
        msg['From'] = "tinysteps88@yahoo.com"
        if name == 'Arpita Roy':
            msg['To'] = "royamitkanti@gmail.com"
        elif name == 'Baidyanath Kumar':
            msg['To'] = "b.sahu2507@gmail.com"
        elif name == 'Nalanagula Swetha':
            msg['To'] = "swetha140499@gmail.com"
        elif name == 'Sagnik Basu':
            msg['To'] = "sagnikbasu19@gmail.com"

        server = smtplib.SMTP("smtp.mail.yahoo.com", 587)
        server.starttls()
        server.login("tinysteps88@yahoo.com","ycfinlyobhkobhaj")
        server.send_message(msg)

        return redirect(url_for('main.index'))

    return render_template("contact_us.html", name=name, pic='_'.join(name.split(' '))+'.jpg')

@main.route('/blogs', methods=['GET', 'POST'])
def blogs():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        pic = request.files['pic']
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        pic.save(os.path.join(os.path.dirname(__file__), 'static/posts', filename))

        blog = BlogPost(date_posted=datetime.now(), title=title, content=content, pic=pic.read(), pic_name=filename, mimetype=mimetype, tourist=current_user)

        db.session.add(blog)
        db.session.commit()

        return redirect(url_for('main.index'))

    page = request.args.get('page', 1, int)
    blogs = BlogPost.query.paginate(page=page, per_page=6)
    
    return render_template("blogs.html", title="Blogs", blogs=blogs)

@main.route('/blogs/<int:id>')
def blogpost(id):
    post = BlogPost.query.filter_by(id=id).first()
    return render_template("blogpost.html", post=post)

@main.route('/about')
def aboutus():
    return render_template("about_us.html", title="About")

@main.route('/adventure', methods=['GET','POST'])
def adventure():
    price_id = ''

    if request.method=='POST':
        roomtype=request.form.get('roomtype')
        travel=request.form.get('travel')
        trip=TripPlan.query.filter(TripPlan.transport==travel,TripPlan.roomtype==roomtype).first()
        current_user.reservation.append(trip)
        db.session.commit()
        price_id = trip.priceid
    
    return render_template("customize_trip.html", title="Adventures", price_id=price_id)

@main.route('/pay')
def payment():
    priceid = request.args.get('priceid')

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': priceid,
            'quantity': 1
        }],
        mode='payment',
        success_url=url_for('main.index', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('main.index', _external=True)
    )
    # flash('Booking & payment done. Thank You','success')
    return {
        'checkout_session_id': session['id'],
        'checkout_public_key': current_app.config['STRIPE_PUBLIC_KEY']
    }

@main.route('/gallery')
def gallery():
    return render_template("gallery.html", title="Gallery")