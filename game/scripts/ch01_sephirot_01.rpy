# game/scripts/ch01_sephirot_01.rpy -- Ch1 王国/白花 Skeleton Chapter
# The Embrace of the Twin Angels
# Story: E2.5
# Ch1 = Sephirot 1 "王国", primary undertow EXIST_DENY (low intensity 2)
# Five-beat: ENCOUNTER -> STRUGGLE -> COMFORT -> CHOICE -> TRANSFORM

# ── Character definitions ──
define angel = Character("天使", color="#c8a0e6")
define beloved = Character("心爱的", color="#9b6bc5")
define narrator = Character(None)

# ── Placeholder image definitions ──
image bg placeholder_01 = Solid("#2a2a3a")
image angel placeholder = "placeholder/angel_placeholder.png"
image beloved placeholder = "placeholder/beloved_placeholder.png"

label ch01_sephirot_01:

    # ── Chapter initialization ──
    $ current_chapter = 1
    $ current_sephirot_id = 1
    $ current_phase = Phase.FORGETTING
    $ active_narrative_tags = set()

    # Autosave at chapter start
    $ SaveSystem.autosave_chapter_start()

    # Chapter title card
    scene black
    show text "第一章 · 王国" at truecenter
    $ renpy.pause(3.0)
    hide text

    # ════════ ① ENCOUNTER ════════
    $ narrative_beat = NarrativeBeat.ENCOUNTER

    scene bg placeholder_01
    show beloved placeholder at center

    "灰色的天空下，废墟绵延到看不到尽头。"
    "心爱的站在废墟的中央，风吹起她的发。"
    "她的身后，一个紫色的身影静静站着。"

    show angel placeholder at left

    angel "我在。"

    "天使的声音很轻，但在风中听得很清楚。"

    # ════════ ② STRUGGLE ════════
    $ narrative_beat = NarrativeBeat.STRUGGLE

    # Set narrative tag -> triggers undertow
    $ set_narrative_tag("existence_denied")

    "废墟中传来低沉的声音。"
    "「你为什么要在这里？你的存在只是负担。如果没有你，这里不会变成废墟。」"

    # Trigger undertow: EXIST_DENY low intensity 2
    $ trigger_undertow("EXIST_DENY", 2)

    "心爱的的立绘微微变淡了。世界好像在否定她存在的意义。"

    # ════════ ③ COMFORT ════════
    $ narrative_beat = NarrativeBeat.COMFORT

    # Angel intervention (gentle, Phase 1 no cost)
    angel "你的存在不是负担。"
    angel "你是我存在的理由。"

    "天使轻轻走到心爱的身边。她的翅膀发出温暖的光。"
    "画面慢慢恢复了色彩。心爱的的立绘重新变得清晰。"

    # Deactivate undertow
    $ deactivate_undertow("EXIST_DENY")

    # ════════ ④ CHOICE ════════
    $ narrative_beat = NarrativeBeat.CHOICE

    "天使握住了心爱的的手。"
    angel "这片废墟不是你的错。但你可以选择——留在这里，还是往前走。"

    # Present choice using Ren'Py menu
    menu:
        "「我要往前走。即使不知道前方有什么。」":
            $ complete_sephirot_with_tag(1, ConfrontationTag.ENGAGE)
            $ bond_depth += 0.03
            angel "你真的很勇敢。"
            "天使的光芒似乎更亮了一些。"

        "「……我想留在这里。外面太可怕了。」":
            $ complete_sephirot_with_tag(1, ConfrontationTag.ESCAPE)
            angel "没关系。我在你身边。"

    # ════════ ⑤ TRANSFORM ════════
    $ narrative_beat = NarrativeBeat.TRANSFORM

    "无论心爱的做了什么选择，天使都站在她身边。"

    # Sephirot completion check (handled by complete_sephirot_with_tag above)
    # Route to next chapter
    $ route_to_chapter(2)

    jump ch02_sephirot_02
