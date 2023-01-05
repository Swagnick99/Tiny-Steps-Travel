from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'hello-bandor'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init_app(app)

    app.app_context().push()

    app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51KtZvNSD2iC3vN8t0mffTjAsISgKHb1wIA9cErnPJQBTMeewiwrWLEjUArNiTwcTWkUBhK3QwofLcRMqm8npnh1Y00jELT29jV'
    app.config['STRIPE_SECRET_KEY'] = 'sk_test_51KtZvNSD2iC3vN8tyK2CHOynvPcfFJM2LBLGLAAEcIaJE01XfGTucjfVkNOiTQ90SK5ovGd3De7suo7O8huc2QB1004VEXFTLl'

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import Tourist
    @login_manager.user_loader
    def load_user(user_id):
        return Tourist.query.get(int(user_id))

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app

# db.create_all(app=create_app())

# db.session.add_all([
#     TripPlan(transport='train',roomtype='economy',priceid='price_1LAyb5SD2iC3vN8tH3wDtRH1'),
#     TripPlan(transport='train',roomtype='deluxe',priceid='price_1KudJISD2iC3vN8tB0LPD6f2'),
#     TripPlan(transport='train',roomtype='luxury',priceid='price_1LAybfSD2iC3vN8tZiJjplVz'),
#     TripPlan(transport='bus',roomtype='economy',priceid='price_1LAydESD2iC3vN8tHc1HUVNV'),
#     TripPlan(transport='bus',roomtype='deluxe',priceid='price_1LAydeSD2iC3vN8tByoHuq10'),
#     TripPlan(transport='bus',roomtype='luxury',priceid='price_1LAydxSD2iC3vN8tekfLPr0R'),
#     TripPlan(transport='ship',roomtype='economy',priceid='price_1LAyeGSD2iC3vN8tprITebLA'),
#     TripPlan(transport='ship',roomtype='deluxe',priceid='price_1LAyedSD2iC3vN8tuWdzXPFE'),
#     TripPlan(transport='ship',roomtype='luxury',priceid='price_1LAyeuSD2iC3vN8tP0lPEsq5'),
#     TripPlan(transport='plane',roomtype='economy',priceid='price_1LAyfBSD2iC3vN8tkQD7YdQS'),
#     TripPlan(transport='plane',roomtype='deluxe',priceid='price_1LAyfVSD2iC3vN8tU6XPwNrz'),
#     TripPlan(transport='plane',roomtype='luxery',priceid='price_1LAyfoSD2iC3vN8t095YwuKh'),
# ])
# db.session.commit()

# TripPlan.__table__.drop(db.engine)

# db.session.query(booking).delete()
# db.session.commit()