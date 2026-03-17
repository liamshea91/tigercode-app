import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def create_default_admin():
  existing = app_tables.users.get(email="orange@admin.ls")
  if not existing:
    anvil.users.signup_with_email("orange@admin.ls", "0r3njE")
    user = app_tables.users.get(email="orange@admin.ls")
    if user:
      user['username'] = "orange"
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
  print("user found by username:", user)
  if user:
    email = user['email']
  else:
    email = username_or_email
  print("attempting login with email:", email)
  try:
    anvil.users.login_with_email(email, password)
    return "success"
  except Exception as e:
    print("login error:", str(e))
    return "invalid"

@anvil.server.callable
def validate_settings(current_password, new_username):
  user = anvil.users.get_user()
  try:
    anvil.users.login_with_email(user['email'], current_password)
  except Exception:
    return "wrong_password"
  if new_username:
    existing = app_tables.users.get(username=new_username)
    if existing and existing != user:
      return "username_taken"
  return "valid"

@anvil.server.callable
def update_user_settings(current_password, new_username, new_password):
  user = anvil.users.get_user()
  try:
    anvil.users.login_with_email(user['email'], current_password)
  except Exception:
    return "wrong_password"
  if new_username:
    existing = app_tables.users.get(username=new_username)
    if existing and existing != user:
      return "username_taken"
    user['username'] = new_username
  if new_password:
    anvil.users.reset_password(user['email'], new_password)
  return "success"

@anvil.server.callable
def get_word_bank():
  words = app_tables.word_bank.search()
  return [(row['word'], row['category']) for row in words]

@anvil.server.callable
def save_entry(title, body, tags):
  user = anvil.users.get_user()
  from datetime import datetime
  app_tables.entries.add_row(
    user=user,
    title=title,
    body=body,
    tags=tags,
    created_on=datetime.now()
  )
  return "success"

@anvil.server.callable
def get_entries(keyword, tag, date_from, date_to):
  user = anvil.users.get_user()
  entries = app_tables.entries.search(
    tables.order_by("created_on", ascending=False),
    user=user
  )
  results = []
  for entry in entries:
    if keyword and keyword.lower() not in entry['title'].lower() and keyword.lower() not in entry['body'].lower():
      continue
    if tag:
      entry_tags = [t.lower() for t in (entry['tags'] or [])]
      if tag.lower() not in entry_tags:
        continue
    entry_date = entry['created_on'].date()
    if date_from and date_to:
      if not (date_from <= entry_date <= date_to):
        continue
    elif date_from:
      if entry_date != date_from:
        continue
    results.append(entry)
  return results

@anvil.server.callable
def get_entries_multi_tag(keyword, tags, date_from, date_to):
  user = anvil.users.get_user()
  entries = app_tables.entries.search(
    tables.order_by("created_on", ascending=False),
    user=user
  )
  results = []
  for entry in entries:
    if keyword and keyword.lower() not in entry['title'].lower() and keyword.lower() not in entry['body'].lower():
      continue
    if tags:
      entry_tags = [t.lower() for t in (entry['tags'] or [])]
      if not all(t.lower() in entry_tags for t in tags):
        continue
    entry_date = entry['created_on'].date()
    if date_from and date_to:
      if not (date_from <= entry_date <= date_to):
        continue
    elif date_from:
      if entry_date != date_from:
        continue
    results.append(entry)
  return results

@anvil.server.callable
def delete_entry(entry_id):
  entry = app_tables.entries.get_by_id(entry_id)
  if entry:
    entry.delete()

@anvil.server.callable
def update_entry(entry_id, title, body, tags):
  entry = app_tables.entries.get_by_id(entry_id)
  if entry:
    entry['title'] = title
    entry['body'] = body
    entry['tags'] = tags
    return "success"
  return "error"

@anvil.server.callable
def get_all_tags():
  user = anvil.users.get_user()
  entries = app_tables.entries.search(user=user)
  all_tags = set()
  for entry in entries:
    if entry['tags']:
      for tag in entry['tags']:
        all_tags.add(tag)
  return sorted(list(all_tags))