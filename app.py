from flask import Flask
from flask import jsonify
from flask import render_template
from flask_compress import Compress
from webargs import fields
from webargs.flaskparser import use_args

from code.prediction_service import PredictionService

prediction_service = None  # type:PredictionService


def create_app():
    """
    Initialize Flask App and internal state
    :return:
    """
    app = Flask(__name__)
    compress = Compress()
    compress.init_app(app)

    def run_on_start(*args, **argv):
        global prediction_service
        prediction_service = PredictionService()

    run_on_start()
    return app


app = create_app()


@app.errorhandler(422)
def handle_unprocessable_entity(err):
    """
    Deal with missing param arguments
    :param err:
    :return:
    """
    # webargs attaches additional metadata to the `data` attribute
    exc = getattr(err, 'exc')
    if exc:
        # Get validations from the ValidationError object
        messages = exc.messages
    else:
        messages = ['Invalid request']
    return jsonify({
        'messages': messages,
    }), 422


@app.route('/ping')
def ping():
    return "pong"


prediction_args = {
    'arriving': fields.Bool(required=True)
    , 'hour': fields.Int(required=True)
}


@app.route('/prediction', methods=['POST', 'GET'])
@use_args(prediction_args)
def predict(args):
    # get sorted flow for nearest 5 stations to AbleTo based on arriving
    model_outputs = prediction_service.predict(hour=args['hour'], arriving=args['arriving'])
    # get the best station
    best_station = model_outputs[0]._asdict()
    res = jsonify(best_station)
    return res


@app.route('/')
def index():
    return render_template('hello.html')


if __name__ == '__main__':
    app.run(debug=False)
