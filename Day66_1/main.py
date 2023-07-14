from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import choice

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        #Method 1. 
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            #Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            if column.name == 'id':
                pass
            else:
                dictionary[column.name] = getattr(self, column.name)
        return dictionary


@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record

@app.route('/random',methods=['GET'])
#normally get method initially included but we typed it regardless.
def get_random_cafe():
    with app.app_context():
        all_cafes = db.session.query(Cafe).all()
        rc = choice(all_cafes)
        #AT BELOW BOTH ARE WORKS SAME AND FINE 2ND MORE PRACTICAL.
        # json_file = jsonify(id=rc.id,name=rc.name,map_url=rc.map_url,img_url=rc.img_url,
        #                     location=rc.location,seats=rc.seats,has_toilet=rc.has_toilet,
        #                     has_wifi=rc.has_wifi,has_sockets=rc.has_sockets,can_take_calls=rc.can_take_calls,
        #                     coffee_price=rc.coffee_price)
        json_file = jsonify(rc.to_dict())
        return json_file
    
@app.route('/all')
def all_cafes():
    all_cafes = db.session.query(Cafe).all()
    all_cafes_dictionary = {}
    for cafe in all_cafes:
        all_cafes_dictionary[cafe.id] = cafe.to_dict()
    return jsonify(all_cafes_dictionary)

@app.route('/search')
def search():
    #IN COMMENTED LINE YOU HAVE MULTIPLE OPTIONS!!!!!
    # all_cafes = db.session.query(Cafe).all()
    # all_cafes_dictionary_with_correct_location = {}
    # location = request.args.get('loc')
    # for cafe in all_cafes:
    #     if cafe.location == location:
    #         all_cafes_dictionary_with_correct_location[cafe.id] = cafe.to_dict()
    query_location = request.args.get("loc")
    cafe = db.session.query(Cafe).filter_by(location=query_location).first()
    if cafe:
        return jsonify(cafe=cafe.to_dict())
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})
      



        

#the code above wasnt working because instance folder error dont forget.
    

## HTTP POST - Create Record

@app.route("/add", methods=["GET","POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.args.get("name"),
        map_url=request.args.get("map_url"),
        img_url=request.args.get("img_url"),
        location=request.args.get("loc"),
        has_sockets=bool(request.args.get("sockets")),
        has_toilet=bool(request.args.get("toilet")),
        has_wifi=bool(request.args.get("wifi")),
        can_take_calls=bool(request.args.get("calls")),
        seats=request.args.get("seats"),
        coffee_price=request.args.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})

## HTTP PUT/PATCH - Update Record

@app.route("/update/<cafe_id>",methods=["PATCH"])
def update(cafe_id):
    with app.app_context():
        cafe_to_update = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
        cafe_to_update.coffee_price = request.args.get("new_price")
        db.session.commit()
    return jsonify(response={"success": f"Successfully updated the cafe"})


## HTTP DELETE - Delete Record

@app.route("/delete/<cafe_id>",methods=['DELETE'])
def delete(cafe_id):
    with app.app_context():
        book_to_delete = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
        db.session.delete(book_to_delete)
        db.session.commit()
    return jsonify(response={'message': 'Book deleted succesfully'})



if __name__ == '__main__':
    app.run(debug=True)
    
