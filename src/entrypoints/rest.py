from ..bootstrap import create_app
from ..router import apply_routes

app = create_app([apply_routes])
