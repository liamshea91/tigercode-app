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

    self.background = "#494547"

    self.lbl_title.text = "Login"
    self.lbl_title.foreground = "#d4b2e4"
    self.lbl_title.font = "Libre Baskerville"
    self.lbl_title.font_size = 24
    self.lbl_title.bold = True
    self.lbl_title.align = "center"

    self.lbl_error.text = ""
    self.lbl_error.foreground = "#d4b2e4"
    self.lbl_error.font = "Red Hat Text"
    self.lbl_error.font_size = 12
    self.lbl_error.align = "center"

    for tb in [self.tb_login, self.tb_password]:
      tb.background = "#ececec"
      tb.foreground = "#3b3b3b"
      tb.font = "Red Hat Text"
      tb.font_size = 14
      tb.align = "center"

    self.tb_login.placeholder = "Username or Email"
    self.tb_password.placeholder = "Password"

    for btn in [self.btn_login, self.btn_go_create]:
      btn.background = "#d4b2e4"
      btn.foreground = "#49326b"
      btn.font = "Libre Baskerville"
      btn.font_size = 14
      btn.bold = True

    self.btn_login.text = "Log In"
    self.btn_go_create.text = "Don't have an account? Sign Up"

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