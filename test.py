import ttkbootstrap as tb
from ttkbootstrap.constants import *

def set_placeholder(entry, placeholder, color='grey'):
    """Set placeholder text in the entry widget with auto-delete on typing."""
    entry.insert(0, placeholder)
    entry.config(foreground=color)
    entry._placeholder = placeholder
    entry._placeholder_color = color
    entry._default_fg = entry.cget("foreground")

    def clear_placeholder(event=None):
        """Clear placeholder when typing starts."""
        if entry.get() == entry._placeholder and entry.cget("foreground") == entry._placeholder_color:
            entry.delete(0, "end")
            entry.config(foreground=entry._default_fg)

    def restore_placeholder(event=None):
        """Restore placeholder if entry is empty."""
        if not entry.get():
            entry.insert(0, entry._placeholder)
            entry.config(foreground=entry._placeholder_color)

    # Bind events
    entry.bind("<FocusIn>", clear_placeholder)
    entry.bind("<KeyPress>", clear_placeholder)  # Auto-delete on typing
    entry.bind("<FocusOut>", restore_placeholder)

# ---------------- MAIN APP ----------------
app = tb.Window(themename="cosmo")
app.title("TTKBootstrap Auto-Delete Placeholder")
app.geometry("300x150")

entry = tb.Entry(app, width=30)
entry.pack(pady=30)

set_placeholder(entry, "Enter your name...")

app.mainloop()
