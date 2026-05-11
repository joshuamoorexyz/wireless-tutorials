from manim import *

config.background_color = "#1a1a2e"


class FiveGInitialSetup(Scene):
    def setup_scene_common(self, title_text, phase_text, phase_number):
        self.clear()
        bg = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color="#1a1a2e",
            fill_opacity=1,
            stroke_width=0,
        )
        self.add(bg)

        phase_tag = Rectangle(width=1.2, height=0.6, fill_color="#e94560", fill_opacity=1, stroke_width=0)
        phase_tag.shift(UP * 3.5 + LEFT * 6.5)
        phase_num = Text(str(phase_number), font_size=28, color=WHITE)
        phase_num.move_to(phase_tag.get_center())
        self.add(phase_tag, phase_num)

        title = Text(title_text, font_size=36, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.8)
        self.add(title)

        phase_label = Text(phase_text, font_size=20, color="#e94560", weight=BOLD)
        phase_label.next_to(title, DOWN, buff=0.15)
        self.add(phase_label)

    def animate_data_flow(self, start, end, color=YELLOW, label=""):
        arrow = Arrow(start, end, color=color, stroke_width=3, buff=0.15)
        self.play(Create(arrow), run_time=0.5)
        if label:
            mid = (start + end) / 2 + UP * 0.25
            lbl = Text(label, font_size=18, color=color)
            lbl.move_to(mid)
            self.play(Write(lbl), run_time=0.3)
        self.wait(0.3)
        return arrow

    def create_box(self, text, color=BLUE_D, width=2.2, height=0.9, font_size=22):
        rect = Rectangle(width=width, height=height, fill_color=color, fill_opacity=0.85, stroke_width=1, stroke_color=WHITE)
        lbl = Text(text, font_size=font_size, color=WHITE)
        lbl.move_to(rect.get_center())
        return VGroup(rect, lbl)

    def animate_box_in(self, box, position, scale=1):
        box.scale(scale)
        box.move_to(position)
        self.play(FadeIn(box, shift=DOWN * 0.3), run_time=0.5)
        self.wait(0.2)

    # ─── PHASE 1: UE Power On & Cell Search ───────────────────────────
    def phase_1_cell_search(self):
        self.setup_scene_common("Cell Search & Synchronization", "UE scans for 5G NR cells", 1)

        ue = self.create_box("UE", "#0f3460")
        gnb = self.create_box("gNB", "#16213e")

        ue_pos = LEFT * 4 + DOWN * 0.5
        gnb_pos = RIGHT * 4 + DOWN * 0.5

        self.animate_box_in(ue, ue_pos)
        self.animate_box_in(gnb, gnb_pos)

        freq_label = Text("Scanning NR bands...", font_size=22, color=YELLOW)
        freq_label.next_to(ue, UP, buff=0.6)
        self.play(Write(freq_label), run_time=0.6)
        self.wait(0.3)

        waves = VGroup()
        for i in range(3):
            w = Circle(radius=0.3 + i * 0.4, stroke_color=YELLOW, stroke_width=2)
            w.move_to(ue.get_center())
            waves.add(w)
        self.play(LaggedStart(*[Create(w) for w in waves], lag_ratio=0.3), run_time=1)
        self.wait(0.2)

        sync_msg = Text("SSB (PSS/SSS) → sync", font_size=20, color=GREEN)
        sync_msg.next_to(gnb, UP, buff=0.6)
        self.play(Write(sync_msg), run_time=0.6)
        self.wait(0.5)

    # ─── PHASE 2: MIB & SIB1 Acquisition ──────────────────────────────
    def phase_2_system_info(self):
        self.setup_scene_common("System Information Acquisition", "UE reads MIB & SIB1", 2)

        ue = self.create_box("UE", "#0f3460")
        gnb = self.create_box("gNB", "#16213e")

        ue_pos = LEFT * 4 + DOWN * 0.5
        gnb_pos = RIGHT * 4 + DOWN * 0.5

        self.animate_box_in(ue, ue_pos)
        self.animate_box_in(gnb, gnb_pos)

        mib = Rectangle(width=3, height=0.7, fill_color=PURPLE_D, fill_opacity=0.9, stroke_width=1, stroke_color=WHITE)
        mib_lbl = Text("MIB (PBCH)", font_size=20, color=WHITE)
        mib_lbl.move_to(mib.get_center())
        mib_group = VGroup(mib, mib_lbl)
        mib_group.next_to(gnb, UP, buff=0.5)
        self.play(FadeIn(mib_group, shift=UP * 0.3), run_time=0.5)

        arrow1 = Arrow(mib_group.get_bottom(), gnb.get_top(), color=PURPLE, stroke_width=2)
        self.play(Create(arrow1), run_time=0.3)

        self.wait(0.3)

        sib1 = Rectangle(width=3, height=0.7, fill_color="#c77dff", fill_opacity=0.9, stroke_width=1, stroke_color=WHITE)
        sib1_lbl = Text("SIB1 (PDSCH)", font_size=20, color=WHITE)
        sib1_lbl.move_to(sib1.get_center())
        sib1_group = VGroup(sib1, sib1_lbl)
        sib1_group.next_to(mib_group, UP, buff=0.5)
        self.play(FadeIn(sib1_group, shift=UP * 0.3), run_time=0.5)

        arrow2 = Arrow(sib1_group.get_bottom(), mib_group.get_top(), color="#c77dff", stroke_width=2)
        self.play(Create(arrow2), run_time=0.3)

        info = Text("Cell access params, scheduling info", font_size=18, color=GOLD)
        info.next_to(sib1_group, UP, buff=0.4)
        self.play(Write(info), run_time=0.5)
        self.wait(0.5)

    # ─── PHASE 3: Random Access (RACH) ────────────────────────────────
    def phase_3_rach(self):
        self.setup_scene_common("Random Access Procedure", "UE → gNB: RACH (MSG1–MSG4)", 3)

        ue = self.create_box("UE", "#0f3460")
        gnb = self.create_box("gNB", "#16213e")

        ue_pos = LEFT * 4 + DOWN * 0.5
        gnb_pos = RIGHT * 4 + DOWN * 0.5

        self.animate_box_in(ue, ue_pos)
        self.animate_box_in(gnb, gnb_pos)

        msgs = [
            ("MSG1: PRACH Preamble", YELLOW, ue, gnb, 1),
            ("MSG2: RAR (Random Access Response)", GREEN, gnb, ue, -1),
            ("MSG3: RRC Setup Request", YELLOW, ue, gnb, 1),
            ("MSG4: Contention Resolution", GREEN, gnb, ue, -1),
        ]

        y_offset = 1.2
        for text, color, sender, receiver, direction in msgs:
            lbl = Text(text, font_size=18, color=color, weight=BOLD)

            if direction == 1:
                pad = sender.get_top() + UP * y_offset
            else:
                pad = sender.get_bottom() + DOWN * y_offset

            lbl.move_to(pad)
            self.play(Write(lbl), run_time=0.4)
            arrow = Arrow(
                sender.get_center(),
                receiver.get_center(),
                color=color,
                stroke_width=2.5,
                buff=0.2,
            )
            if direction == 1:
                arrow.shift(UP * (y_offset - 0.2))
            else:
                arrow.shift(DOWN * (y_offset - 0.2))
            self.play(Create(arrow), run_time=0.35)
            self.wait(0.25)
            y_offset += 0.7

        self.wait(0.5)

    # ─── PHASE 4: RRC Connection Setup ────────────────────────────────
    def phase_4_rrc_setup(self):
        self.setup_scene_common("RRC Connection Setup", "Establishing signaling radio bearer", 4)

        ue = self.create_box("UE", "#0f3460")
        gnb = self.create_box("gNB", "#16213e")

        ue_pos = LEFT * 4 + DOWN * 0.5
        gnb_pos = RIGHT * 4 + DOWN * 0.5

        self.animate_box_in(ue, ue_pos)
        self.animate_box_in(gnb, gnb_pos)

        msgs = [
            ("RRCSetupRequest", YELLOW, ue, gnb, UP),
            ("RRCSetup", GREEN, gnb, ue, DOWN),
            ("RRCSetupComplete", YELLOW, ue, gnb, UP),
        ]

        y_offset = 1.2
        for text, color, sender, receiver, direction in msgs:
            lbl = Text(text, font_size=20, color=color, weight=BOLD)
            if direction == UP:
                pad = sender.get_top() + UP * y_offset
            else:
                pad = sender.get_bottom() + DOWN * y_offset
            lbl.move_to(pad)

            self.play(Write(lbl), run_time=0.4)
            arrow = Arrow(
                sender.get_center(),
                receiver.get_center(),
                color=color,
                stroke_width=2.5,
                buff=0.2,
            )
            if direction == UP:
                arrow.shift(UP * (y_offset - 0.2))
            else:
                arrow.shift(DOWN * (y_offset - 0.2))
            self.play(Create(arrow), run_time=0.35)
            self.wait(0.25)
            y_offset += 0.7

        srbs = Text("SRB1 established", font_size=22, color="#00ff88")
        srbs.next_to(gnb, DOWN, buff=0.8)
        self.play(Write(srbs), run_time=0.5)
        self.wait(0.5)

    # ─── PHASE 5: Registration & Authentication ──────────────────────
    def phase_5_registration(self):
        self.setup_scene_common("Registration & Authentication", "UE ↔ Core Network (AMF)", 5)

        ue = self.create_box("UE", "#0f3460")
        gnb = self.create_box("gNB", "#16213e")
        amf = self.create_box("AMF", "#1a1a4e")
        ausf = self.create_box("AUSF/UDM", "#2d1a4e")

        ue_pos = LEFT * 5 + DOWN * 1.5
        gnb_pos = LEFT * 1.5 + DOWN * 1.5
        amf_pos = RIGHT * 2 + DOWN * 1.5
        ausf_pos = RIGHT * 5 + DOWN * 1.5

        self.animate_box_in(ue, ue_pos)
        self.animate_box_in(gnb, gnb_pos)
        self.animate_box_in(amf, amf_pos)
        self.animate_box_in(ausf, ausf_pos)

        steps = [
            ("Registration Request", ue, gnb, YELLOW),
            ("Registration Request", gnb, amf, YELLOW),
            ("Auth Request/Response", amf, ausf, ORANGE),
            ("Security Mode Command", amf, gnb, GREEN),
            ("Security Mode Command", gnb, ue, GREEN),
            ("Registration Accept", amf, gnb, "#00ff88"),
            ("Registration Accept", gnb, ue, "#00ff88"),
        ]

        y = 1.0
        for text, sender, receiver, color in steps:
            lbl = Text(text, font_size=17, color=color, weight=BOLD)
            lbl.next_to(sender, UP, buff=y)
            self.play(Write(lbl), run_time=0.3)
            arr = Arrow(
                sender.get_center(),
                receiver.get_center(),
                color=color,
                stroke_width=2,
                buff=0.15,
            )
            self.play(Create(arr), run_time=0.3)
            y += 0.01
            self.wait(0.15)

        self.wait(0.5)

    # ─── PHASE 6: PDU Session Establishment ──────────────────────────
    def phase_6_pdu_session(self):
        self.setup_scene_common("PDU Session Establishment", "Data connectivity for the UE", 6)

        ue = self.create_box("UE", "#0f3460")
        gnb = self.create_box("gNB", "#16213e")
        upf = self.create_box("UPF", "#1a3a1e")
        dn = self.create_box("Data Network", "#1a2e3e", width=2.8, height=0.9, font_size=20)

        ue_pos = LEFT * 5 + DOWN * 0.5
        gnb_pos = LEFT * 2 + DOWN * 0.5
        upf_pos = RIGHT * 2 + DOWN * 0.5
        dn_pos = RIGHT * 5 + DOWN * 0.5

        self.animate_box_in(ue, ue_pos)
        self.animate_box_in(gnb, gnb_pos)
        self.animate_box_in(upf, upf_pos)
        self.animate_box_in(dn, dn_pos)

        labels_text = [
            "PDU Session Est. Request",
            "N2 PDU Session Request",
            "N4 Session Establishment",
            "N6 Data Forwarding",
        ]
        positions = [
            (ue, gnb),
            (gnb, upf),
            (upf, upf),
            (upf, dn),
        ]
        colors_list = [YELLOW, YELLOW, ORANGE, "#00ff88"]

        for i, (lbl_txt, (s, r), c) in enumerate(zip(labels_text, positions, colors_list)):
            lbl = Text(lbl_txt, font_size=17, color=c, weight=BOLD)
            lbl.next_to(s, UP, buff=1.0 + i * 0.5)
            self.play(Write(lbl), run_time=0.4)
            if s != r:
                arr = Arrow(
                    s.get_center(), r.get_center(), color=c, stroke_width=2.5, buff=0.15
                )
                self.play(Create(arr), run_time=0.35)
            self.wait(0.2)

        ip_assign = Text("IP Address allocated", font_size=20, color="#00ff88")
        ip_assign.next_to(dn, DOWN, buff=0.8)
        self.play(Write(ip_assign), run_time=0.5)
        self.wait(0.5)

    # ─── SUMMARY ──────────────────────────────────────────────────────
    def phase_7_summary(self):
        self.setup_scene_common("5G Initial Setup Complete", "End-to-End Flow Summary", 7)

        steps = [
            "1.  Cell Search  —  SSB sync (PSS/SSS)",
            "2.  System Info  —  MIB (PBCH) + SIB1 (PDSCH)",
            "3.  Random Access  —  MSG1–MSG4 (RACH)",
            "4.  RRC Setup  —  SRB1 established",
            "5.  Registration  —  UE ↔ AMF (auth + security)",
            "6.  PDU Session  —  UE ↔ UPF ↔ Data Network",
        ]

        base_y = 2.0
        for i, step in enumerate(steps):
            dot = Dot(LEFT * 5 + UP * (base_y - i * 0.7), color="#e94560", radius=0.08)
            txt = Text(step, font_size=20, color=WHITE)
            txt.next_to(dot, RIGHT, buff=0.3)
            self.play(FadeIn(dot), Write(txt), run_time=0.3)

        complete = Text("UE is now connected and ready!", font_size=28, color="#00ff88", weight=BOLD)
        complete.shift(DOWN * 2.5)
        self.play(Write(complete), run_time=0.6)
        self.wait(1)

    # ─── MAIN FLOW ──────────────────────────────────────────────────
    def construct(self):
        self.phase_1_cell_search()
        self.wait(0.5)
        self.phase_2_system_info()
        self.wait(0.5)
        self.phase_3_rach()
        self.wait(0.5)
        self.phase_4_rrc_setup()
        self.wait(0.5)
        self.phase_5_registration()
        self.wait(0.5)
        self.phase_6_pdu_session()
        self.wait(0.5)
        self.phase_7_summary()
        self.wait(1)
