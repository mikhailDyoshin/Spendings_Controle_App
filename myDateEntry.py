from tkcalendar import DateEntry

class MyDateEntry(DateEntry):
    def __init__(self, master=None, align='left', **kw):
        DateEntry.__init__(self, master, **kw)
        self.align = align

    def drop_down(self):
        """Display or withdraw the drop-down calendar depending on its current state."""
        if self._calendar.winfo_ismapped():
            self._top_cal.withdraw()
        else:
            self._validate_date()
            date = self.parse_date(self.get())
            if self.align == 'left':  # usual DateEntry
                x = self.winfo_rootx()
            else:  # right aligned drop-down
                # x = self.winfo_rootx() + self.winfo_width() - self._top_cal.winfo_reqwidth()
                x = self.winfo_rootx() + self.winfo_width()
            y = self.winfo_rooty() + self.winfo_height()
            if self.winfo_toplevel().attributes('-topmost'):
                self._top_cal.attributes('-topmost', True)
            else:
                self._top_cal.attributes('-topmost', False)
            self._top_cal.geometry('+%i+%i' % (x, y))
            self._top_cal.deiconify()
            self._calendar.focus_set()
            self._calendar.selection_set(date)