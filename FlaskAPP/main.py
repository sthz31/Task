from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
# {
#         'reviewer':reviewer,
#         'rate':rate,
#         'review':review,
#         'date':date
#     }
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reviewer = db.Column(db.String(500))
    rate = db.Column(db.String(15))
    review = db.Column(db.String(2055))
    date = db.Column(db.String(255))

    def __repr__(self):
        return '<Post %s>' % self.reviewer


class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "reviewer", "rate",  'review',"date")


post_schema = PostSchema()
posts_schema = PostSchema(many=True)

@app.route('/')
def index():
    reviews = Review.query.all()
    return render_template('index.html', reviews=reviews)


class ReviewResource(Resource):
    def post(self):
        print(request.json)
        new_review = Review(
            reviewer=request.json['reviewer'],
            rate=request.json['rate'],
            review=request.json['review'],
            date=request.json['date']
        )
        db.session.add(new_review)
        db.session.commit()
        return post_schema.dump(new_review)

api.add_resource(ReviewResource, '/add_review')

if __name__ == '__main__':
    app.run(debug=True)