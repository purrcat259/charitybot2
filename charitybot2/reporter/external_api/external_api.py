import argparse
import time

from charitybot2.events.currency import Currency
from charitybot2.events.donation import Donation
from charitybot2.paths import production_repository_db_path
from charitybot2.storage.repository import Repository
from flask import Flask, request, jsonify, make_response, abort
from flask import render_template
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from tests.paths_for_tests import repository_db_path

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
test_repository_db_path = repository_db_path

api_address = '127.0.0.1'
api_port = 8000
api_url = 'http://' + api_address
api_full_url = api_url + ':' + str(api_port) + '/'
debug_mode = False
cli_debug_mode = False
console_version = '0.1.2'
http_server = WSGIServer((api_address, api_port), app)

api_paths = {
    'api': {
        'v1': [
            'events',
            'event/:event_name',
            'event/:event_name/donations',
            'event/:event_name/donations?limit=:limit',
            'event/:event_name/donations/last',
            'event/:event_name/donations/distribution'
        ]
    },
    'stats': [
        ':event_name'
    ],
    'overlay': [
        ':event_name'
    ]
}

repository = Repository(db_path=test_repository_db_path, debug=True)


def get_currency_symbol(event_name):
    key = repository.get_event_configuration(event_name=event_name).get_currency().get_key()
    return Currency(key=key).get_symbol()


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Configuration file missing'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def landing():
    return render_template('index.html')


@app.route('/api/v1/', methods=['GET'])
def index():
    return jsonify(
        {
            'paths': api_paths,
            'debug_allowed': cli_debug_mode,
            'debug': debug_mode
        })


@app.route('/api/v1/events', methods=['GET'])
def events():
    event_names = repository.get_event_names()
    if len(event_names) == 0:
        abort(404)
    return jsonify(events=event_names)


@app.route('/api/v1/event/<event_name>', methods=['GET'])
def event_details(event_name):
    if not repository.event_exists(event_name=event_name):
        abort(404)
    event_configuration = repository.get_event_configuration(event_name=event_name)
    event_data = {
        'name': event_name,
        'currency_symbol': get_currency_symbol(event_name=event_name),
        'start_time': event_configuration.get_start_time(),
        'end_time': event_configuration.get_end_time(),
        'amount_raised': repository.get_total_raised(event_name=event_name),
        'target_amount': event_configuration.get_target_amount()
    }
    return jsonify(event_data)


@app.route('/api/v1/event/<event_name>/donations')
def event_donations(event_name):
    if not repository.event_exists(event_name=event_name):
        abort(404)
    limit = request.args.get('limit')
    if limit is None:
        limit = 0
    print(limit)
    donations = repository.get_donations(event_name=event_name, amount=limit)
    donation_objects = [
        {
            'amount': donation.get_donation_amount(),
            'total_raised': donation.get_total_raised(),
            'timestamp': donation.get_timestamp()
        } for donation in donations
    ]
    return jsonify(donations=donation_objects)


@app.route('/api/v1/event/<event_name>/donations/info')
def donations_info(event_name):
    if not repository.event_exists(event_name=event_name):
        abort(404)
    last_timespan = 3600  # an hour in seconds
    current_time = int(time.time())
    last_timespan_donations = repository.get_donations_for_timespan(
        event_name=event_name,
        timespan_start=current_time - last_timespan,
        timespan_end=current_time)
    largest_donation = repository.get_largest_donation(event_name=event_name)
    largest_donation = {
        'amount': largest_donation.get_donation_amount(),
        'timestamp': largest_donation.get_timestamp()
    } if isinstance(largest_donation, Donation) else None
    last_donation = repository.get_last_donation(event_name=event_name)
    last_donation = {
        'amount': last_donation.get_donation_amount(),
        'timestamp': last_donation.get_timestamp()
    } if isinstance(last_donation, Donation) else None
    donations_info_object = {
        'count': repository.get_number_of_donations(event_name=event_name),
        'average': repository.get_average_donation(event_name=event_name),
        'largest': largest_donation,
        'last': last_donation,
        'specific': {
            'count': len(last_timespan_donations),
            'timespan': last_timespan
        }
    }
    return jsonify(donations_info=donations_info_object)


@app.route('/api/v1/event/<event_name>/donations/last')
def last_event_donation(event_name):
    if event_name not in repository.get_event_names():
        abort(404)
    last_donation = repository.get_last_donation(event_name=event_name)
    return jsonify(
        {
            'amount': last_donation.get_donation_amount(),
            'total_raised': last_donation.get_total_raised(),
            'timestamp': last_donation.get_timestamp()
        }
    )


@app.route('/api/v1/event/<event_name>/donations/distribution')
def event_donations_distribution(event_name):
    if event_name not in repository.get_event_names():
        abort(404)
    all_donations = repository.get_all_donations(event_name=event_name)
    distribution = {
        '0-9': 0,
        '10-19': 0,
        '20-29': 0,
        '30-39': 0,
        '40-49': 0,
        '50-75': 0,
        '76-99': 0,
        '100-10000': 0
    }
    for donation in all_donations:
        for bound_string, count in distribution.items():
            bounds = bound_string.split('-')
            lower_bound = int(bounds[0])
            upper_bound = int(bounds[1])
            if lower_bound <= donation.get_donation_amount() <= upper_bound:
                distribution[bound_string] += 1
    return jsonify(donations_distribution=distribution)


@app.route('/overlay/<event_name>')
def amount_raised(event_name):
    if not repository.event_exists(event_name=event_name):
        return render_template('overlay.html',
                               event_name=event_name,
                               amount_raised='...',
                               currency_symbol='')
    last_donation = repository.get_last_donation(event_name=event_name)
    # Take no donations present into consideration
    amount = last_donation if isinstance(last_donation, float) else last_donation.get_total_raised()
    # Remove decimal point and add thousands separators
    pretty_number = format(int(amount), ',d')
    return render_template('overlay.html',
                           event_name=event_name,
                           amount_raised=pretty_number,
                           currency_symbol=get_currency_symbol(event_name=event_name))


@app.route('/stats/<event_name>', methods=['GET'])
def status_console(event_name):
    if not repository.event_exists(event_name=event_name):
        abort(404)
    return render_template(
        'console.html',
        event_name=event_name,
        debug_mode=str(debug_mode).lower(),
        console_version=console_version)


@app.route('/debug')
def debug():
    if cli_debug_mode:
        global debug_mode
        debug_mode = True
        global repository
        repository = Repository(db_path=test_repository_db_path, debug=debug_mode)
        return 'Entered API debug mode'
    else:
        return 'Entering API debug mode is not allowed'


@app.route('/destroy')
def destroy():
    global debug_mode
    if debug_mode:
        stop_api()
        return 'Shutting down service'
    return 'Not in debug mode - shutting down in unavailable'


def create_api_process_parser():
    parser = argparse.ArgumentParser(description='Charitybot API')
    parser.add_argument('--debug', dest='debug', help='Run Charitybot API in debug mode', action='store_true')
    return parser


def start_api(args):
    global cli_debug_mode
    cli_debug_mode = args.debug
    global repository
    if cli_debug_mode:
        print('--- Starting in debug mode ---')
        repository = Repository(db_path=test_repository_db_path, debug=True)
    else:
        print('--- Starting in production mode ---')
        repository = Repository(db_path=production_repository_db_path, debug=True)
    global http_server
    http_server.serve_forever()


def stop_api():
    global http_server
    http_server.stop()


if __name__ == '__main__':
    args = create_api_process_parser().parse_args(['--debug'])
    start_api(args=args)
