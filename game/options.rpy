# game/options.rpy -- Ren'Py Global Configuration
# The Embrace of the Twin Angels
# Engine: Ren'Py 8.3.x

define config.name = _("双生天使的拥抱")
define config.version = "0.1.0"
define build.name = "TwinAngels"

define gui.show_name = True
define gui.text_size = 33
define gui.text_xsize = 40
define gui.name_text_size = 45
define gui.interface_text_size = 33
define gui.label_text_size = 36
define gui.notify_text_size = 24

define config.screen_width = 1920
define config.screen_height = 1080

define config.window_title = "{#gui.show_name}{#window_title}{#config.name} — {#config.version}"

# Save configuration
define config.save_directory = "TwinAngels-1234567890"

# Autosave frequency (manual control: triggered on chapter switch)
define config.autosave_frequency = 0

# Text speed
default preferences.text_cps = 50

# Skip settings
default preferences.skip_unseen = False
default preferences.skip_after_choices = False

# Volume
default preferences.music_volume = 0.8
default preferences.sfx_volume = 0.8

# Fullscreen
default preferences.fullscreen = False

# Theme colors (purple/gold)
define gui.accent_color = '#9b6bc5'
define gui.idle_color = '#4a4a4a'
define gui.hover_color = '#c8a0e6'
define gui.selected_color = '#c8a0e6'
define gui.insensitive_color = '#8c8c8c'

# Textbox
define gui.textbox_height = 278
define gui.textbox_yalign = 1.0

# Namebox
define gui.name_xpos = 360
define gui.name_ypos = 0
define gui.namebox_width = 420
define gui.namebox_height = 40

# Version tag (save compatibility)
define config.script_version = 1
