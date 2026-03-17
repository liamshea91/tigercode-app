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

    categories = {}
    for word, category in words:
      if category not in categories:
        categories[category] = []
      categories[category].append(word)

    flow_categories = FlowPanel()
    self.panel_word_bank.add_component(flow_categories)

    flow_words = FlowPanel()
    self.panel_word_bank.add_component(flow_words)

    for category, word_list in categories.items():
      cat_btn = Button(text="▶ " + category)
      cat_btn.tag = category
      cat_btn.set_event_handler('click', self.category_clicked)
      flow_categories.add_component(cat_btn)

      word_panel = ColumnPanel()
      word_panel.tag = category
      word_panel.visible = False
      for word in word_list:
        word_btn = Button(text=word)
        word_btn.tag = word
        word_btn.set_event_handler('click', self.word_clicked)
        word_panel.add_component(word_btn)
      flow_words.add_component(word_panel)

  def category_clicked(self, sender, **event_args):
    category = sender.tag
    for component in self.panel_word_bank.get_components():
      if isinstance(component, FlowPanel):
        for inner in component.get_components():
          if hasattr(inner, 'tag') and inner.tag == category and isinstance(inner, ColumnPanel):
            inner.visible = not inner.visible
            sender.text = ("▼ " if inner.visible else "▶ ") + category
            break

  def update_tags_display(self):
    if self.selected_tags:
      self.lbl_tags.text = "Tags: " + ", ".join(self.selected_tags)
    else:
      self.lbl_tags.text = ""

  def word_clicked(self, sender, **event_args):
    word = sender.tag
    if word in self.selected_tags:
      # Remove tag if already selected
      self.selected_tags.remove(word)
      sender.bold = False
    else:
      # Add tag
      self.selected_tags.append(word)
      sender.bold = True
    self.update_tags_display()

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