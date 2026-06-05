# ui/theme.py
# Central theme configuration for the CPU Scheduling Simulator UI.
# All colors, fonts, and sizing constants are defined here.
# Import this module in any UI file that needs styling.

# --- Background Colors ---
BG_PRIMARY = "#1e1e2e"       # Main window background (dark navy)
BG_SECONDARY = "#2a2a3e"     # Panel background (slightly lighter)
BG_CARD = "#313145"          # Input card / table row background

# --- Accent Colors ---
ACCENT_BLUE = "#7aa2f7"      # Buttons, highlights
ACCENT_GREEN = "#9ece6a"     # Success states, run button
ACCENT_RED = "#f7768e"       # Remove button, error states
ACCENT_YELLOW = "#e0af68"    # Quantum input label

# --- Text Colors ---
TEXT_PRIMARY = "#c0caf5"     # Main text
TEXT_SECONDARY = "#565f89"   # Labels, hints
TEXT_HEADER = "#ffffff"      # Column headers

# --- Fonts ---
FONT_HEADER = ("Segoe UI", 11, "bold")
FONT_LABEL = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
FONT_MONO = ("Consolas", 10)

# --- Sizing ---
PAD_X = 12
PAD_Y = 8
BTN_WIDTH = 10
INPUT_WIDTH = 6