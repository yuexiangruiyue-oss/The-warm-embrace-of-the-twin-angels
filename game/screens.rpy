# game/screens.rpy -- Basic Screen Definitions
# The Embrace of the Twin Angels
# Minimal screens for Batch 0 (Ren'Py defaults + project theming)

## Main Menu screen ############################################################

screen main_menu():
    tag menu
    style_prefix "main_menu"

    add "main_menu_bg"

    text "[config.name!t]":
        style "main_menu_title"

    text "[config.version!t]":
        style "main_menu_version"

    frame:
        style "main_menu_frame"

        vbox:
            style_prefix "main_menu_vbox"

            textbutton _("开始游戏") action Start():
                style "main_menu_button"
            textbutton _("继续游戏") action Show("load"):
                style "main_menu_button"
            textbutton _("设置") action Show("preferences"):
                style "main_menu_button"
            textbutton _("退出") action Quit(confirm=not main_menu):
                style "main_menu_button"

style main_menu_frame:
    xalign 0.0
    yalign 0.5

style main_menu_vbox:
    xalign 0.0
    yalign 0.5
    spacing 6

style main_menu_button:
    xalign 0.0
    yalign 0.0
    xsize 340

style main_menu_title:
    xalign 0.5
    yalign 0.1
    size 75
    color '#c8a0e6'

style main_menu_version:
    xalign 0.5
    yalign 0.2
    size 24
    color '#9b6bc5'

## Game Menu screen ############################################################

screen game_menu(title=None):
    layer "master"
    style_prefix "game_menu"

    frame:
        style "game_menu_frame"

        if title:
            text "[title!t]":
                style "game_menu_label"

        vbox:
            style_prefix "game_menu_vbox"

            textbutton _("返回") action Return():
                style "game_menu_button"

style game_menu_frame:
    xalign 0.5
    yalign 1.0
    xsize 1280
    ysize 120

style game_menu_vbox:
    xalign 0.5
    yalign 0.5
    spacing 6

style game_menu_button:
    xalign 0.5

style game_menu_label:
    xalign 0.5
    yalign 0.3
    size 36
    color '#c8a0e6'

## Say screen ##################################################################

screen say(who, what):
    style_prefix "say"

    window:
        id "window"

        if who is not None:
            window:
                id "namebox"
                style "Namebox"
                text who id "who"

        text what id "what"

    use quick_menu

style say_window:
    background None
    yalign 1.0
    xfill True
    ysize gui.textbox_height

style say_vbox:
    xalign 0.5
    yalign 1.0

style Namebox:
    xpos gui.name_xpos
    ypos gui.name_ypos
    xsize gui.namebox_width
    ysize gui.namebox_height

style say_who:
    color '#c8a0e6'
    size gui.name_text_size

style say_what:
    xpos gui.text_xpos
    ypos gui.text_ypos
    xsize gui.text_xsize
    color '#ffffff'
    size gui.text_size

## Choice screen ###############################################################

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action

style choice_vbox:
    xalign 0.5
    yalign 0.5
    spacing 4

style choice_button:
    xalign 0.5
    xsize gui.choice_button_width

style choice_button_text:
    xalign gui.choice_button_text_xalign
    text_align 0.5
    layout "subtitle"
    size gui.text_size

## Quick Menu ##################################################################

screen quick_menu():
    if quick_menu:
        hbox:
            style_prefix "quick"
            xalign 1.0
            yalign 1.0

            textbutton _("存档") action Show("save")
            textbutton _("读档") action Show("load")
            textbutton _("设置") action Show("preferences")
            textbutton _("标题") action MainMenu()

style quick_button:
    background None
    ysize 33

style quick_button_text:
    color '#9b6bc5'
    hover_color '#c8a0e6'
    selected_color '#c8a0e6'
    size 24

default quick_menu = True

## Save/Load screen (minimal) ##################################################

screen save():
    tag menu
    use file_slots("save")

screen load():
    tag menu
    use file_slots("load")

screen file_slots(title):
    default page_name = "page_1"
    default page = 1

    style_prefix "file_slots"

    frame:
        style "file_slots_frame"

        vbox:
            label "[title!t]"

            hbox:
                for i in range(1, 10):
                    textbutton str(i):
                        action SetField("file_slots", "page", i)

            grid gui.file_slot_columns gui.file_slot_rows:
                for i in range(1, 10):
                    $ slot = "{}-{}".format(page, i)
                    button:
                        action FileAction(slot)
                        has vbox
                        add FileScreenshot(slot)
                        text FileTime(slot, format=_("{#file_time}%Y-%m-%d %H:%M"), empty=_("空")):
                            color '#9b6bc5'

            textbutton _("返回") action Return()

style file_slots_frame:
    xalign 0.5
    yalign 0.5
    xsize 1280
    ysize 800

## Preferences screen (minimal) ################################################

screen preferences():
    tag menu

    style_prefix "preferences"

    frame:
        style "preferences_frame"

        vbox:
            label _("设置")

            hbox:
                vbox:
                    label _("文字速度")
                    bar value Preference("text speed")

                    label _("自动前进")
                    bar value Preference("auto-forward time")

                vbox:
                    label _("音乐音量")
                    bar value Preference("music volume")

                    label _("音效音量")
                    bar value Preference("sound volume")

            null height 20

            textbutton _("返回") action Return()

style preferences_frame:
    xalign 0.5
    yalign 0.5
    xsize 1280
    ysize 800
