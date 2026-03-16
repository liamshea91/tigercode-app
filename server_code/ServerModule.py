import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

@anvil.server.callable
def check_username_taken(username):
  existing = app_tables.users.get(username=username)
  return existing is not None