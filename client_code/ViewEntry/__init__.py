from ._anvil_designer import ViewEntryTemplate
from anvil import *
import anvil.server
import anvil.users

class ViewEntry(ViewEntryTemplate):
  def __init__(self, entry=None, **properties):
    self.init_components(**properties)
    self.entry = entry

    self.background = "#494547"

    for lbl in [self.lbl_title, self.lbl_date, self.lbl_tags]:
      lbl.foreground = "#d4b2e4"
      lbl.font = "Libre Baskerville"
      lbl.font_size = 14
      lbl.align = "center"

    self.lbl_body.foreground = "#d4b2e4"
    self.lbl_body.font = "Red Hat Text"
    self.lbl_body.font_size = 14

    for btn in [self.btn_edit, self.btn_delete, self.btn_back]:
      btn.background = "#d4b2e4"
      btn.foreground = "#49326b"
      btn.font = "Libre Baskerville"
      btn.font_size = 14
      btn.bold = True

    self.btn_edit.text = "Edit"
    self.btn_delete.text = "Delete"
    self.btn_back.text = "Back"

    if entry:
      self.lbl_title.text = entry['title']
      self.lbl_date.text = str(entry['created_on'].strftime("%B %d, %Y"))
      self.lbl_body.text = entry['body']
      tags = entry['tags']
      self.lbl_tags.text = "Tags: " + ", ".join(tags) if tags else ""

  @handle("btn_edit", "click")
  def btn_edit_click(self, **event_args):
    open_form('EditEntry', entry=self.entry)

  @handle("btn_delete", "click")
  def btn_delete_click(self, **event_args):
    confirmed = confirm("Are you sure you want to delete this entry? This cannot be undone.")
    if confirmed:
      anvil.server.call('delete_entry', self.entry.get_id())
      alert("Entry deleted.")
      open_form('PastEntries')

  @handle("btn_back", "click")
  def btn_back_click(self, **event_args):
    open_form('PastEntries')