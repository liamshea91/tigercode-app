from ._anvil_designer import SettingsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Settings(SettingsTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.lbl_error.text = ""
    self.lbl_success.text = ""
    self.tb_current_password.placeholder = "Current Password"
    self.tb_new_username.placeholder = "New Username"
    self.tb_confirm_username.placeholder = "Confirm New Username"
    self.tb_new_password.placeholder = "New Password"
    self.tb_confirm_password.placeholder = "Confirm New Password"
    user = anvil.users.get_user()
    if user:
      self.lbl_current_username.text = "Username: " + user['username']
      self.lbl_current_email.text = "Email: " + user['email']
    else:
      open_form('Login')

  @handle("btn_save", "click")
  def btn_save_click(self, **event_args):
    current_password = self.tb_current_password.text.strip()
    new_username = self.tb_new_username.text.strip()
    confirm_username = self.tb_confirm_username.text.strip()
    new_password = self.tb_new_password.text.strip()
    confirm_password = self.tb_confirm_password.text.strip()