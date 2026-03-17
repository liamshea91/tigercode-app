import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def create_default_admin():
  existing = app_tables.users.get(email="orange@admin.com")
  if not existing:
    anvil.users.signup_with_email("orange@admin.com", "passOrange")
    user = app_tables.users.get(email="orange@admin.com")
    if user:
      user['username'] = "adminOrange"
      user['confirmed_email'] = True

@anvil.server.callable
def create_user(username, email, password):
  existing = app_tables.users.get(username=username)
  if existing:
    return "username_taken"
  anvil.users.signup_with_email(email, password)
  user = app_tables.users.get(email=email)
  if user:
    user['username'] = username
    user['confirmed_email'] = True
  return "success"

@anvil.server.callable
def login_with_username_or_email(username_or_email, password):
  user = app_tables.users.get(username=username_or_email)
  if user:
    email = user['email']
  else:
    email = username_or_email
  try:
    anvil.users.login_with_email(email, password)
    return "success"
  except Exception as e:
    return "invalid"