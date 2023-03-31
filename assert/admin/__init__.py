from apiflask import APIBlueprint

admin = APIBlueprint('admin', __name__,url_prefix='/admin')

from . import view