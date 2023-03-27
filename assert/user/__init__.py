from apiflask import APIBlueprint

user = APIBlueprint('user', __name__,url_prefix='/user')

from . import view
