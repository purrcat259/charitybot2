from charitybot2.paths import production_repository_db_path, test_repository_db_path
from charitybot2.persistence.event_sqlite_repository import EventSQLiteRepository
from charitybot2.start_service import Service
from flask import Flask
from flask import g
from flask import render_template
from flask import request

app = Flask(__name__)

overlay_identity = 'CB2 Overlay'
overlay_address = '127.0.0.1'
overlay_port = 7000
debug_mode = True
overlay_service = Service(
    name=overlay_identity,
    app=app,
    address=overlay_address,
    port=overlay_port,
    debug=debug_mode)


def get_repository_path():
    # global debug_mode
    path = production_repository_db_path
    if overlay_service.debug:
        path = test_repository_db_path
    return path

event_repository = EventSQLiteRepository(db_path=get_repository_path())


def get_event_repository():
    event_repo = getattr(g, '_event_repository', None)
    if event_repo is None:
        event_repo = g._event_repository = EventSQLiteRepository(
            db_path=get_repository_path())
    return event_repo


def get_api_address():
    api_address = 'http://127.0.0.1:8001'
    if not debug_mode:
        api_address = 'https://api.charitybot.net'
    return api_address


def get_update_delay():
    delay = 1000
    if not debug_mode:
        delay = 3000
    return delay


@app.context_processor
def inject_api_url():
    return dict(
        api_address=get_api_address(),
        update_delay=get_update_delay())


@app.route('/')
def index():
    return 'Use any of the following: /:event/total, /:event/ticker or /:event/latest'


@app.route('/<event_identifier>/total')
def event_total(event_identifier):
    return render_template('total.html', event_identifier=event_identifier)


@app.route('/<event_identifier>/ticker')
def event_ticker(event_identifier):
    limit = request.args.get('limit')
    if limit is not None:
        try:
            limit = int(limit)
        except ValueError:
            limit = 10
    else:
        limit = 10
    return render_template('ticker.html', event_identifier=event_identifier, limit=limit)


@app.route('/<event_identifier>/latest')
def event_latest(event_identifier):
    return render_template('latest.html', event_identifier=event_identifier)


@app.route('/<event_identifier>/kitchensink')
def kitchen_sink(event_identifier):
    return render_template('kitchen_sink.html', event_identifier=event_identifier)


@app.route('/destroy/')
def destroy():
    if overlay_service.debug:
        stop_api()
        return 'Shutting down Overlay Service'
    return 'Debug mode is disabled - shutting down is unavailable'


def stop_api():
    overlay_service.stop()


if __name__ == '__main__':
    cli_args = overlay_service.create_service_argument_parser().parse_args()
    debug_mode = cli_args.debug
    overlay_service = Service.create_from_args(name=overlay_identity, app=app, cli_args=cli_args)
    overlay_service.start()
