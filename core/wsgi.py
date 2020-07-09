from core.app import create_app
from .settings import Settings

app = create_app(__name__, Settings)
