import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def create_user(username, email, password):
  existing = app_tables.users.get(username=username)
  if existing:
    return "username_taken"

    # Sign up the user
  anvil.users.signup_with_email(email, password)

  # Get the user row directly from the table instead
  user = app_tables.users.get(email=email)
  if user:
    user['username'] = username

  return "success"