# src/models/__init__.py

# Este ficheiro importa todos os seus modelos,
# garantindo que o SQLAlchemy os conheça ao construir as relações.

from .users import Users
from .clients import Client
from .vehicle import Vehicle
from .service import Service
from .scheduling import Scheduling
