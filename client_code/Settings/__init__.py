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

    self.background = "#494547"

    for lbl in [self.lbl_current_username, self.lbl_current_email]:
      lbl.foreground = "#d4b2e4"
      lbl.font = "Libre Baskerville"
      lbl.font_size = 14
      lbl.align = "center"

    self.lbl_error.text = ""
    self.lbl_error.foreground = "#d4b2e4"
    self.lbl_error.font = "Red Hat Text"
    self.lbl_error.font_size = 12
    self.lbl_error.align = "center"

    self.lbl_success.text = ""
    self.lbl_success.foreground = "#d4b2e4"
    self.lbl_success.font = "Red Hat Text"
    self.lbl_success.font_size = 12
    self.lbl_success.align = "center"

    for tb in [self.tb_current_password, self.tb_new_username, self.tb_confirm_username, self.tb_new_password, self.tb_confirm_password]:
      tb.background = "#ececec"
      tb.foreground = "#3b3b3b"
      tb.font = "Red Hat Text"
      tb.font_size = 14
      tb.align = "center"

    self.tb_current_password.placeholder = "Current Password"
    self.tb_new_username.placeholder = "New Username"
    self.tb_confirm_username.placeholder = "Confirm New Username"
    self.tb_new_password.placeholder = "New Password"
    self.tb_confirm_password.placeholder = "Confirm New Password"

    for btn in [self.btn_save, self.btn_back]:
      btn.background = "#d4b2e4"
      btn.foreground = "#49326b"
      btn.font = "Libre Baskerville"
      btn.font_size = 14
      btn.bold = True

    self.btn_save.text = "Save Changes"
    self.btn_back.text = "Back"

    user = anvil.users.get_user()
    if user:
      self.lbl_current_username.text = user['username']
      self.lbl_current_email.text = user['email']
    else:
      open_form('Login')

  @handle("btn_save", "click")
  def btn_save_click(self, **event_args):
    current_password = self.tb_current_password.text.strip()
    new_username = self.tb_new_username.text.strip()
    confirm_username = self.tb_confirm_username.text.strip()
    new_password = self.tb_new_password.text.strip()
    confirm_password = self.tb_confirm_password.text.strip()

    if not current_password:
      self.lbl_error.text = "Please enter your current password to make changes."
      return

    if not new_username and not new_password:
      self.lbl_error.text = "Please fill in at least one field to update."
      return

    if new_username and new_username != confirm_username:
      self.lbl_error.text = "Usernames do not match."
      return

    if new_password and new_password != confirm_password:
      self.lbl_error.text = "Passwords do not match."
      return

    validation = anvil.server.call('validate_settings', current_password, new_username)

    if validation == "wrong_password":
      self.lbl_error.text = "Current password is incorrect."
      return
    elif validation == "username_taken":
      self.lbl_error.text = "That username is already taken."
      return

    confirmed = confirm("Are you sure you want to save these changes?")
    if not confirmed:
      return

    result = anvil.server.call('update_user_settings', current_password, new_username, new_password)

    if result == "success":
      alert("Changes saved successfully!")
      self.lbl_error.text = ""
      user = anvil.users.get_user()
      self.lbl_current_username.text = user['username']
      self.lbl_current_email.text = user['email']
      self.tb_current_password.text = ""
      self.tb_new_username.text = ""
      self.tb_confirm_username.text = ""
      self.tb_new_password.text = ""
      self.tb_confirm_password.text = ""

  @handle("btn_back", "click")
  def btn_back_click(self, **event_args):
    open_form('Home')