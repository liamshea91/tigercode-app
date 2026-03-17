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

@anvil.server.callable
def get_user_stats():
  user = anvil.users.get_user()
  stats = app_tables.user_stats.get(user=user)
  if not stats:
    return None
  return {
    'current_streak': stats['current_streak'],
    'longest_streak': stats['longest_streak'],
    'streak_started': stats['streak_started'],
    'first_entry': stats['first_entry'],
    'total_entries': stats['total_entries']
  }

@anvil.server.callable
def update_streak():
  from datetime import datetime, date, timedelta
  user = anvil.users.get_user()
  today = date.today()

  stats = app_tables.user_stats.get(user=user)

  # Check if there's already an entry today
  entries_today = [
    e for e in app_tables.entries.search(user=user)
    if e['created_on'].date() == today
  ]

  # More than 1 means this isn't the first entry today
  first_today = len(entries_today) == 1

  if not stats:
    # First ever entry
    app_tables.user_stats.add_row(
      user=user,
      current_streak=1,
      longest_streak=1,
      streak_started=datetime.now(),
      first_entry=datetime.now(),
      total_entries=1
    )
    return {'current_streak': 1, 'first_today': True}

    # Update total entries
  stats['total_entries'] = stats['total_entries'] + 1

  if not first_today:
    return {'current_streak': stats['current_streak'], 'first_today': False}

    # Check if yesterday had an entry
  yesterday = today - timedelta(days=1)
  entries_yesterday = [
    e for e in app_tables.entries.search(user=user)
    if e['created_on'].date() == yesterday
  ]

  if entries_yesterday:
    # Continue streak
    stats['current_streak'] = stats['current_streak'] + 1
    if stats['current_streak'] > stats['longest_streak']:
      stats['longest_streak'] = stats['current_streak']
  else:
    # Reset streak
    stats['current_streak'] = 1
    stats['streak_started'] = datetime.now()

  return {'current_streak': stats['current_streak'], 'first_today': True}