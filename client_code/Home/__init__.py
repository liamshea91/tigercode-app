from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.users
import anvil.server

class Home(HomeTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    self.background = "#494547"

    self.lbl_welcome.foreground = "#d4b2e4"
    self.lbl_welcome.font = "Libre Baskerville"
    self.lbl_welcome.font_size = 28
    self.lbl_welcome.bold = True
    self.lbl_welcome.align = "center"

    for btn in [self.btn_new_entry, self.btn_past_entries, self.btn_settings, self.btn_stats, self.btn_logout]:
      btn.background = "#d4b2e4"
      btn.foreground = "#49326b"
      btn.font = "Libre Baskerville"
      btn.font_size = 14
      btn.bold = True

    self.btn_new_entry.text = "New Entry"
    self.btn_past_entries.text = "Past Entries"
    self.btn_settings.text = "Settings"
    self.btn_stats.text = "Stats"
    self.btn_logout.text = "Log Out"

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

  @handle("btn_stats", "click")
  def btn_stats_click(self, **event_args):
    open_form('Stats')

  @handle("btn_logout", "click")
  def btn_logout_click(self, **event_args):
    anvil.users.logout()
    open_form('Login')