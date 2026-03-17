from ._anvil_designer import StatsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Stats(StatsTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    self.background = "#494547"

    # Title
    self.lbl_title.text = "Stats"
    self.lbl_title.foreground = "#d4b2e4"
    self.lbl_title.font = "Libre Baskerville"
    self.lbl_title.font_size = 24
    self.lbl_title.bold = True
    self.lbl_title.align = "center"

    # Section headers
    self.lbl_streak_header.text = "Streak Stats"
    self.lbl_general_header.text = "General Stats"
    for lbl in [self.lbl_streak_header, self.lbl_general_header]:
      lbl.foreground = "#d4b2e4"
      lbl.font = "Libre Baskerville"
      lbl.font_size = 18
      lbl.bold = True
      lbl.align = "center"

    # Stat labels
    for lbl in [self.lbl_current_streak, self.lbl_longest_streak, self.lbl_streak_started, self.lbl_first_entry, self.lbl_total_entries]:
      lbl.foreground = "#d4b2e4"
      lbl.font = "Libre Baskerville"
      lbl.font_size = 14
      lbl.align = "center"

    # Button
    self.btn_back.background = "#d4b2e4"
    self.btn_back.foreground = "#49326b"
    self.btn_back.font = "Libre Baskerville"
    self.btn_back.font_size = 14
    self.btn_back.bold = True
    self.btn_back.text = "Back"

    self.load_stats()

  def load_stats(self):
    anvil.server.call('recalculate_stats')
    stats = anvil.server.call('get_user_stats')
    if stats:
      self.lbl_current_streak.text = "Current Streak: " + str(stats['current_streak']) + (" day" if stats['current_streak'] == 1 else " days")
      self.lbl_longest_streak.text = "Longest Streak: " + str(stats['longest_streak']) + (" day" if stats['longest_streak'] == 1 else " days")
      self.lbl_streak_started.text = "Streak Started: " + stats['streak_started'].strftime("%B %d, %Y") if stats['streak_started'] else "Streak Started: —"
      self.lbl_first_entry.text = "First Entry: " + stats['first_entry'].strftime("%B %d, %Y") if stats['first_entry'] else "First Entry: —"
      self.lbl_total_entries.text = "Total Entries: " + str(stats['total_entries'])
    else:
      self.lbl_current_streak.text = "Current Streak: 0 days"
      self.lbl_longest_streak.text = "Longest Streak: 0 days"
      self.lbl_streak_started.text = "Streak Started: —"
      self.lbl_first_entry.text = "First Entry: —"
      self.lbl_total_entries.text = "Total Entries: 0"

  @handle("btn_back", "click")
  def btn_back_click(self, **event_args):
    open_form('Home')