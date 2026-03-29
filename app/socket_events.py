from flask_login import current_user
from flask_socketio import join_room

from app.extensions import socketio


def register_socket_events():
    @socketio.on("connect")
    def handle_connect():
        if not current_user.is_authenticated:
            return False

        if current_user.rol == "admin":
            join_room("admins")

        if current_user.rol == "vendedor":
            join_room(f"vendedor_{current_user.id}")