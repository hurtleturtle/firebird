from flask import Blueprint, jsonify, request, current_app, render_template
from firebird.watcher import get_events
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


@bp.route('/')
def display():
    return render_template('index.html.j2')