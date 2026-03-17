from ._anvil_designer import CreateAccountTemplate
from anvil import *
import anvil.users
import anvil.server

class CreateAccount(CreateAccountTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.lbl_error.text = ""
    self.tb_username.placeholder = "Username"
    self.tb_email.placeholder = "Email"
    self.tb_password.placeholder = "Password"
    anvil.server.call('create_default_admin')

  @handle("btn_create", "click")
  def btn_create_click(self, **event_args):
    username = self.tb_username.text.strip()
    email = self.tb_email.text.strip()
    password = self.tb_password.text.strip()

    if not username or not email or not password:
      self.lbl_error.text = "All fields are required."
      return

    result = anvil.server.call('create_user', username, email, password)

    if result == "username_taken":
      self.lbl_error.text = "That username is already taken."
    elif result == "success":
      alert("Account created! Please log in.")
      open_form('Login')

  @handle("btn_go_login", "click")
  def btn_go_login_click(self, **event_args):
    open_form('Login')