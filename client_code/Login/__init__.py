from ._anvil_designer import LoginTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Login(LoginTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.lbl_error.text = ""

  @handle("btn_login", "click")
  def btn_login_click(self, **event_args):
    username_or_email = self.tb_login.text.strip()
    password = self.tb_password.text.strip()

    if not username_or_email or not password:
      self.lbl_error.text = "Please enter your username or email and password."
      return

    result = anvil.server.call('login_with_username_or_email', username_or_email, password)

    if result == "success":
      open_form('Home')
    else:
      self.lbl_error.text = "Invalid username/email or password."

  @handle("btn_go_create", "click")
  def btn_go_create_click(self, **event_args):
    open_form('CreateAccount')