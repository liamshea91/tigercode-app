from ._anvil_designer import PastEntriesTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class PastEntries(PastEntriesTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    self.background = "#494547"

    self.lbl_no_results.text = ""
    self.lbl_no_results.foreground = "#d4b2e4"
    self.lbl_no_results.font = "Red Hat Text"
    self.lbl_no_results.font_size = 14
    self.lbl_no_results.align = "center"

    self.tb_search.background = "#ececec"
    self.tb_search.foreground = "#3b3b3b"
    self.tb_search.font = "Red Hat Text"
    self.tb_search.font_size = 14
    self.tb_search.placeholder = "Search by keyword..."

    for dp in [self.dp_from, self.dp_to]:
      dp.background = "#ececec"
      dp.foreground = "#3b3b3b"
      dp.font = "Red Hat Text"
      dp.font_size = 14

    for btn in [self.btn_tags, self.btn_clear, self.btn_back]:
      btn.background = "#d4b2e4"
      btn.foreground = "#49326b"
      btn.font = "Libre Baskerville"
      btn.font_size = 14
      btn.bold = True

    self.btn_tags.text = "Filter by Tag"
    self.btn_clear.text = "Clear Filters"
    self.btn_back.text = "Back"

    self.selected_tags = []
    self.panel_tags.visible = False
    self.tb_search.set_event_handler('change', self.tb_search_change)
    self.dp_from.set_event_handler('change', self.dp_from_change)
    self.dp_to.set_event_handler('change', self.dp_to_change)
    self.load_tag_checkboxes()
    self.load_entries()

  def load_tag_checkboxes(self):
    tags = anvil.server.call('get_all_tags')
    self.panel_tags.clear()
    for tag in tags:
      cb = CheckBox(text=tag)
      cb.foreground = "#d4b2e4"
      cb.font = "Red Hat Text"
      cb.font_size = 13
      cb.set_event_handler('change', self.tag_checkbox_changed)
      self.panel_tags.add_component(cb)

  def tag_checkbox_changed(self, **event_args):
    self.selected_tags = []
    for component in self.panel_tags.get_components():
      if isinstance(component, CheckBox) and component.checked:
        self.selected_tags.append(component.text)
    self.load_entries()

  def load_entries(self):
    keyword = self.tb_search.text.strip() if self.tb_search.text else ""
    date_from = self.dp_from.date if self.dp_from.date else None
    date_to = self.dp_to.date if self.dp_to.date else None
    entries = anvil.server.call('get_entries_multi_tag', keyword, self.selected_tags, date_from, date_to)
    if entries:
      self.lbl_no_results.text = ""
      self.rp_entries.items = entries
    else:
      self.lbl_no_results.text = "No entries found."
      self.rp_entries.items = []

  def tb_search_change(self, **event_args):
    self.load_entries()

  def dp_from_change(self, **event_args):
    self.load_entries()

  def dp_to_change(self, **event_args):
    self.load_entries()

  @handle("btn_tags", "click")
  def btn_tags_click(self, **event_args):
    self.panel_tags.visible = not self.panel_tags.visible

  @handle("btn_clear", "click")
  def btn_clear_click(self, **event_args):
    self.tb_search.text = ""
    self.dp_from.date = None
    self.dp_to.date = None
    self.selected_tags = []
    for component in self.panel_tags.get_components():
      if isinstance(component, CheckBox):
        component.checked = False
    self.panel_tags.visible = False
    self.load_entries()

  @handle("btn_back", "click")
  def btn_back_click(self, **event_args):
    open_form('Home')