from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Home(HomeTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    user = anvil.users.get_user()
    if user:
      self.lbl_welcome.text = "Welcome, " + user['username'] + "!"
    else:
      open_form('Login')

  @handle("btn_new_entry", "click")
  def btn_new_entry_click(self, **event_args):
    open_form('NewEntry')

  @handle("btn_past_entries", "click")
  def btn_past_entries_click(self, **event_args):
    open_form('PastEntries')

  @handle("btn_settings", "click")
  def btn_settings_click(self, **event_args):
    open_form('Settings')

  @handle("btn_logout", "click")
  def btn_logout_click(self, **event_args):
    anvil.users.logout()
    open_form('Login')