from ._anvil_designer import NewEntryTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class NewEntry(NewEntryTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.lbl_error.text = ""
    self.lbl_tags.text = ""
    self.tb_title.placeholder = "Entry Title"
    self.ta_body.placeholder = "Write your entry here..."
    self.selected_tags = []
    self.panel_word_bank.visible = False
    self.load_word_bank()

  def load_word_bank(self):
    words = anvil.server.call('get_word_bank')
    self.panel_word_bank.clear()
    for word, category in words:
      btn = Button(text=word + " (" + category + ")")
      btn.tag = word
      btn.set_event_handler('click', self.word_clicked)
      self.panel_word_bank.add_component(btn)

  def word_clicked(self, sender, **event_args):
    word = sender.tag
    if word not in self.selected_tags:
      self.selected_tags.append(word)
      self.lbl_tags.text = "Tags: " + ", ".join(self.selected_tags)
    current = self.ta_body.text or ""
    if current and not current.endswith(" "):
      current += " "
    self.ta_body.text = current + word

  @handle("btn_word_bank", "click")
  def btn_word_bank_click(self, **event_args):
    self.panel_word_bank.visible = not self.panel_word_bank.visible

  @handle("btn_save", "click")
  def btn_save_click(self, **event_args):
    title = self.tb_title.text.strip()
    body = self.ta_body.text.strip()

    if not title or not body:
      self.lbl_error.text = "Please enter a title and body for your entry."
      return

    confirmed = confirm("Ready to save your entry?")
    if not confirmed:
      return

    result = anvil.server.call('save_entry', title, body, self.selected_tags)

    if result == "success":
      alert("🎉 Entry saved! Great job writing today!")
      open_form('Home')
    else:
      self.lbl_error.text = "Something went wrong. Please try again."

  @handle("btn_back", "click")
  def btn_back_click(self, **event_args):
    open_form('Home')