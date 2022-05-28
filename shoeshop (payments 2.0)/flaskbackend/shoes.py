from flask import Flask,request,jsonify,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import stripe

app = Flask(__name__)
# For MAC
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/book'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/shoe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['STRIPE_PUBLIC_KEY']= "pk_test_51K5LIQJ2poMPNLhqlX6TVg0Hz4E11ReaJ40pZVm0x7y4TtgfIHgyMmeadICbdBpibVkML7405ulBjNPFSpjoTDs600RdNwACrp"
app.config['STRIPE_SECRET_KEY']="sk_test_51K5LIQJ2poMPNLhqOW4C1XifJeJlSbYgEWjiwaVIIRY6TZToZmSY7m2oN7n8Bx9AgT82MVlhv44ZfriRMF7fga1z00feB557vi"

# Initialisation of the db
db = SQLAlchemy(app)
CORS(app)

# Stripe api key
stripe.api_key = app.config['STRIPE_SECRET_KEY']



# class Shoe inherits a basic database model provided by SQLAlchemy
class Shoe(db.Model):
    __tablename__="shoe_items"

    shoe_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    imagename = db.Column(db.String(100), nullable=False)


    def __init__(self, name, price, description,quantity,imagename):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity
        self.imagename = imagename


    def json(self):
        return {"id": self.shoe_id, "name": self.name, "price": self.price, "quantity": self.quantity,"description":self.description,"imagename":self.imagename}

@app.route("/")
def home():
    return "test"

@app.route("/shoes")
def get_all():
    shoelist = Shoe.query.all()
    if len(shoelist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "shoes": [shoe.json() for shoe in shoelist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no shoes."
        }
    ), 404




# Creating stripe checkout session
@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    data = json.loads(request.data)
    print(data)
    # Convert into the data model that is required by flask. 
    # We will convert it to a form like this
    conversionData = []
    for item in data:
        conversionData.append(
            {
                'price_data':{
                    'currency':'sgd',
                    'unit_amount':item['price'],
                    'product_data':{
                        'name':item['name'],

                    }
                },
                'quantity':item['quantity'],
            }
        )

    
# line_items=[
#                 {
#                     'price_data': {
#                         'currency': 'gbp',
#                         'unit_amount': 4000,
#                         'product_data': {
#                             'name': 'Check Out Now',
#                             'images': ['https://i.imgur.com/EHyR2nP.png'],
#                         },
#                     },
#                     'quantity': 1,
#                 },
#             ],

    try:
        session = stripe.checkout.Session.create(
            line_items=conversionData,
            payment_method_types=['card'],
            mode="payment",
            success_url='http://localhost/developertrack/shoeshop%20(payments%202.0)/views/success.html',
            cancel_url='http://localhost/developertrack/shoeshop%20(payments%202.0)/views/catalogue.html'
            )


    except Exception as e:
        return str(e)


    # Once successful return session URL to the frontend side
    print(session.url)
    return jsonify({'url': session.url})

# Stripe Successful, update exams




if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)