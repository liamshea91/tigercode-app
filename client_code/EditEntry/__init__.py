from ._anvil_designer import EditEntryTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class EditEntry(EditEntryTemplate):
  def __init__(self, entry=None, **properties):
    self.init_components(**properties)
    self.entry = entry

    self.background = "#494547"

    self.lbl_error.text = ""
    self.lbl_error.foreground = "#d4b2e4"
    self.lbl_error.font = "Red Hat Text"
    self.lbl_error.font_size = 12
    self.lbl_error.align = "center"

    self.lbl_tags.text = ""
    self.lbl_tags.foreground = "#d4b2e4"
    self.lbl_tags.font = "Libre Baskerville"
    self.lbl_tags.font_size = 12
    self.lbl_tags.align = "center"

    self.tb_title.background = "#ececec"
    self.tb_title.foreground = "#3b3b3b"
    self.tb_title.font = "Libre Baskerville"
    self.tb_title.font_size = 16
    self.tb_title.align = "center"
    self.tb_title.placeholder = "Entry Title"

    self.ta_body.background = "#ececec"
    self.ta_body.foreground = "#3b3b3b"
    self.ta_body.font = "Red Hat Text"
    self.ta_body.font_size = 14
    self.ta_body.placeholder = "Write your entry here..."

    for btn in [self.btn_word_bank, self.btn_save, self.btn_back]:
      btn.background = "#d4b2e4"
      btn.foreground = "#49326b"
      btn.font = "Libre Baskerville"
      btn.font_size = 14
      btn.bold = True

    self.btn_word_bank.text = "Word Bank"
    self.btn_save.text = "Save Changes"
    self.btn_back.text = "Back"

    self.selected_tags = list(entry['tags']) if entry and entry['tags'] else []
    self.tb_title.text = entry['title'] if entry else ""
    self.ta_body.text = entry['body'] if entry else ""
    self.update_tags_display()
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
      cat_btn.background = "#49326b"
      cat_btn.foreground = "#d4b2e4"
      cat_btn.font = "Libre Baskerville"
      cat_btn.font_size = 13
      cat_btn.set_event_handler('click', self.category_clicked)
      flow_categories.add_component(cat_btn)

      word_panel = ColumnPanel()
      word_panel.tag = category
      word_panel.visible = False
      for word in word_list:
        word_btn = Button(text=word)
        word_btn.tag = word
        word_btn.background = "#d4b2e4"
        word_btn.foreground = "#49326b"
        word_btn.font = "Red Hat Text"
        word_btn.font_size = 13
        word_btn.bold = word in self.selected_tags
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
      self.selected_tags.remove(word)
      sender.bold = False
    else:
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

    confirmed = confirm("Save changes to this entry?")
    if not confirmed:
      return

    result = anvil.server.call('update_entry', self.entry.get_id(), title, body, self.selected_tags)

    if result == "success":
      alert("✅ Entry updated!")
      open_form('PastEntries')
    else:
      self.lbl_error.text = "Something went wrong. Please try again."

  @handle("btn_back", "click")
  def btn_back_click(self, **event_args):
    open_form('PastEntries')