from apiflask import APIBlueprint

ledger = APIBlueprint('ledger', __name__,url_prefix='/ledger')

from . import view
