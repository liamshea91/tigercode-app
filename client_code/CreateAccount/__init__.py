from ._anvil_designer import CreateAccountTemplate
from anvil import *
import anvil.users
import anvil.server

class CreateAccount(CreateAccountTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    self.background = "#494547"

    self.lbl_title.text = "Create Account"
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

    self.lbl_notice.text = "Note: Your email cannot be changed after account creation. Your username and password can be changed in Settings."
    self.lbl_notice.foreground = "#d4b2e4"
    self.lbl_notice.font = "Libre Baskerville"
    self.lbl_notice.font_size = 12
    self.lbl_notice.align = "center"

    for tb in [self.tb_username, self.tb_email, self.tb_password]:
      tb.background = "#ececec"
      tb.foreground = "#3b3b3b"
      tb.font = "Red Hat Text"
      tb.font_size = 14
      tb.align = "center"

    self.tb_username.placeholder = "Username"
    self.tb_email.placeholder = "Email"
    self.tb_password.placeholder = "Password"

    for btn in [self.btn_create, self.btn_go_login]:
      btn.background = "#d4b2e4"
      btn.foreground = "#49326b"
      btn.font = "Libre Baskerville"
      btn.font_size = 14
      btn.bold = True

    self.btn_create.text = "Create Account"
    self.btn_go_login.text = "Already have an account? Log In"

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