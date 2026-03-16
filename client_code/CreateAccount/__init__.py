from ._anvil_designer import CreateAccountTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class CreateAccount(CreateAccountTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.lbl_error.text = ""

  @handle("btn_create", "click")
  def btn_create_click(self, **event_args):
    username = self.tb_username.text.strip()
    email = self.tb_email.text.strip()
    password = self.tb_password.text.strip()

    if not username or not email or not password:
      self.lbl_error.text = "All fields are required."
      return

    if anvil.server.call('check_username_taken', username):
      self.lbl_error.text = "That username is already taken."
      return

    try:
      anvil.users.signup_with_email(email, password)
      user = anvil.users.get_user()
      user['username'] = username
      alert("Account created! Please log in.")
      open_form('Login')
    except Exception as e:
      self.lbl_error.text = str(e)

  @handle("btn_go_login", "click")
  def btn_go_login_click(self, **event_args):
    open_form('Login')