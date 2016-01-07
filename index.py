#!/Python27x86/python27

import os
import flask, flask.views
from flask import Markup
from flask import jsonify
import evaluate
# print __name__
app = flask.Flask(__name__)

# @app.route('/')
class Main(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')
    
class About(flask.views.MethodView):
    def get(self):
        return flask.render_template('about.html')
    
class Contact(flask.views.MethodView):
    def get(self):
        return flask.render_template('contact.html')   

app.add_url_rule('/',view_func=Main.as_view('main'), methods=["GET"])
app.add_url_rule('/about/',view_func=About.as_view('about'), methods=["GET"])
app.add_url_rule('/contact/',view_func=Contact.as_view('contact'), methods=["GET"])




@app.route('/_analyze')
def analyze():
    topic = flask.request.args.get('topic')
    location = {'lat':flask.request.args.get('lat'),'lng':flask.request.args.get('lng'),'rad':flask.request.args.get('rad')}
    # print location
    tweets_with_score = evaluate.getTweetsWithScore(topic, location, 20)
    # tweets_with_score = [("adf",'pos')]
    print tweets_with_score
    return jsonify(tweets_with_score)
app.debug = True

if __name__ == '__main__':
	evaluate.warmUp()
	app.run()