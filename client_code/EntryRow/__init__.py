from ._anvil_designer import EntryRowTemplate
from anvil import *
import anvil.server
import anvil.users

class EntryRow(EntryRowTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    self.background = "#494547"

    for lbl in [self.lbl_title, self.lbl_date, self.lbl_tags]:
      lbl.foreground = "#d4b2e4"
      lbl.font = "Libre Baskerville"
      lbl.font_size = 13
      lbl.align = "center"

    self.btn_view.background = "#d4b2e4"
    self.btn_view.foreground = "#49326b"
    self.btn_view.font = "Libre Baskerville"
    self.btn_view.font_size = 13
    self.btn_view.bold = True

  def refresh_data_bindings(self):
    entry = self.item
    self.lbl_title.text = entry['title']
    self.lbl_date.text = str(entry['created_on'].strftime("%B %d, %Y"))
    tags = entry['tags']
    self.lbl_tags.text = "Tags: " + ", ".join(tags) if tags else ""

  @handle("btn_view", "click")
  def btn_view_click(self, **event_args):
    open_form('ViewEntry', entry=self.item)