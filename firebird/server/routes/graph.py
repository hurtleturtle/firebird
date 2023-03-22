from flask import Blueprint, jsonify, request, current_app, render_template
from firebird.watcher import get_events, get_intended_temp
import asyncio


__all__ = [
    'bp'
]
bp = Blueprint('graph', __name__)


@bp.route('/init')
def initialise_graph():
    default_count = current_app.config.get('DEFAULT_EVENT_COUNT', 100)

    try:
        count = request.args.get('count', default=default_count, type=int)
    except ValueError:
        count = default_count

    events = asyncio.run(get_events(count=count))
    current_app.logger.info(events)
    return jsonify(events)


@bp.route('/temperature')
def temperature():
    temp = get_intended_temp(current_app.config.get('BOOT_CONFIG', '/boot/config.txt'))
    return str(temp), 200


@bp.route('/')
def display():
    return render_template('index.html.j2')