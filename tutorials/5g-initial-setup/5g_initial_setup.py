from manim import *
import numpy as np

config.background_color = "#0a0a1a"


class FiveGInitialSetup(Scene):
    # ─── Helpers ──────────────────────────────────────────────────
    def _setup_phase(self, title, subtitle, num):
        self.clear()
        bg = FullScreenRectangle()
        bg.set_fill(color="#0a0a1a", opacity=1)
        bg.set_stroke(width=0)
        self.add(bg)

        tag = Rectangle(width=1, height=0.5, fill_color="#e94560", fill_opacity=1, stroke_width=0)
        tag.to_corner(UL, buff=0.3)
        n = Text(str(num), font_size=26, color=WHITE, weight=BOLD).move_to(tag.get_center())
        self.add(tag, n)

        t = Text(title, font_size=34, color=WHITE, weight=BOLD).next_to(tag, RIGHT, buff=0.4).shift(UP * 0.05)
        st = Text(subtitle, font_size=18, color="#e94560", weight=BOLD).next_to(t, DOWN, buff=0.1).align_to(t, LEFT)
        self.add(t, st)
        self.wait(0.1)

    def _box(self, text, color="#1a1a3e", w=1.8, h=0.8, fs=20):
        r = Rectangle(width=w, height=h, fill_color=color, fill_opacity=0.85, stroke_width=1, stroke_color=WHITE)
        l = Text(text, font_size=fs, color=WHITE).move_to(r.get_center())
        return VGroup(r, l)

    def _tex(self, text, fs=28, color=WHITE, weight=NORMAL):
        return Text(text, font_size=fs, color=color, weight=weight)

    # ─── PHASE 1: Cell Search — visual + math ──────────────────────
    def phase_1_cell_search(self):
        self._setup_phase("Cell Search & Synchronization", "PSS / SSS detection and frame sync", 1)

        # ── Cell tower ─────────────────────────────────────────────
        pole = Rectangle(width=0.15, height=2.2, fill_color="#4a4a6a", fill_opacity=1, stroke_width=0)
        pole.shift(RIGHT * 4.5 + DOWN * 0.4)
        base = Rectangle(width=0.8, height=0.15, fill_color="#4a4a6a", fill_opacity=1, stroke_width=0)
        base.next_to(pole, DOWN, buff=0)
        antenna = Polygon(
            pole.get_top() + LEFT * 0.25, pole.get_top() + RIGHT * 0.25,
            pole.get_top() + UP * 0.5, stroke_width=0, fill_color="#e94560", fill_opacity=0.9,
        )
        tower = VGroup(pole, base, antenna)
        self.play(FadeIn(tower, shift=UP * 0.5), run_time=0.6)
        gnb_label = Text("gNB", font_size=18, color="#e94560").next_to(antenna, UP, buff=0.15)
        self.play(Write(gnb_label), run_time=0.3)

        # ── UE ─────────────────────────────────────────────────────
        ue_shape = RoundedRectangle(width=1.0, height=0.7, corner_radius=0.12, fill_color="#0f3460", fill_opacity=1, stroke_width=0)
        ue_shape.shift(LEFT * 4.5 + DOWN * 0.2)
        ue_label = Text("UE", font_size=18, color=WHITE).move_to(ue_shape.get_center())
        ue = VGroup(ue_shape, ue_label)
        self.play(FadeIn(ue, shift=UP * 0.5), run_time=0.5)

        # ── Scan animation ─────────────────────────────────────────
        scan = Text("Scanning NR bands...", font_size=20, color=YELLOW).next_to(ue, UP, buff=0.6)
        self.play(Write(scan), run_time=0.4)
        dots = VGroup(*[Dot(scan.get_right() + RIGHT * (i + 1) * 0.25, radius=0.04, color=YELLOW) for i in range(3)])
        self.play(LaggedStart(*[FadeIn(d, scale=0) for d in dots], lag_ratio=0.15), run_time=0.5)
        self.wait(0.2)

        # ── Radio waves from tower ─────────────────────────────────
        self.play(FadeOut(scan), FadeOut(dots), run_time=0.3)
        wave_label = Text("SS/PBCH Block (PSS + SSS)", font_size=20, color=GREEN).next_to(tower, UP, buff=0.7)
        self.play(Write(wave_label), run_time=0.5)

        for _ in range(2):
            waves = VGroup()
            for r in [0.8, 1.6, 2.4]:
                c = Circle(radius=r, stroke_color=BLUE, stroke_width=2, stroke_opacity=1 - r * 0.25)
                c.move_to(antenna.get_top() + UP * 0.2)
                waves.add(c)
            self.play(Create(waves), run_time=0.8)
            self.wait(0.15)

        # ── Math: Zadoff-Chu for PSS ───────────────────────────────
        eq1 = self._tex("PSS:  a_u(n) = exp( -j\u03C0 u n(n+1) / N_ZC )", fs=32, color=YELLOW)
        eq1.shift(LEFT * 3 + UP * 1.5)
        eq1_desc = self._tex("Zadoff-Chu sequence, root indices u = 25, 29, 34", fs=16, color=GREY)
        eq1_desc.next_to(eq1, DOWN, buff=0.1)
        self.play(Write(eq1), Write(eq1_desc), run_time=0.8)
        self.wait(0.3)

        eq2 = self._tex("N_ZC = 127,  0 \u2264 n < N_ZC", fs=28, color=BLUE)
        eq2.next_to(eq1_desc, DOWN, buff=0.25)
        self.play(Write(eq2), run_time=0.5)
        self.wait(0.3)

        # ── Math: m-sequence for SSS ────────────────────────────────
        eq3 = self._tex("SSS:  d(n) = [1 - 2 x\u2080(n)] \u00D7 [1 - 2 x\u2081(n)]", fs=28, color=ORANGE)
        eq3.shift(RIGHT * 3 + UP * 1.5)
        eq3_desc = self._tex("Product of two Gold-code m-sequences", fs=16, color=GREY)
        eq3_desc.next_to(eq3, DOWN, buff=0.1)
        self.play(Write(eq3), Write(eq3_desc), run_time=0.7)
        self.wait(0.5)

        # ── Correlation peak plot ──────────────────────────────────
        self.play(
            FadeOut(eq1), FadeOut(eq2), FadeOut(eq3),
            FadeOut(eq1_desc), FadeOut(eq3_desc),
            FadeOut(wave_label), run_time=0.4,
        )

        axes = Axes(
            x_range=[0, 6, 1], y_range=[0, 1.2, 0.2],
            x_length=6, y_length=2.5,
            axis_config={"color": GREY, "font_size": 18},
            x_axis_config={"label_direction": DOWN},
        ).shift(DOWN * 0.3)
        xl = Text("Frequency offset (subcarriers)", font_size=14, color=GREY).next_to(axes, DOWN, buff=0.2)
        yl = Text("Correlation", font_size=14, color=GREY).next_to(axes, LEFT, buff=0.4).rotate(PI / 2)
        self.play(Create(axes), Write(xl), Write(yl), run_time=0.6)

        xs = np.linspace(0, 6, 80)
        ys = 0.3 + 0.7 * np.exp(-((xs - 3) ** 2) / 0.5) + 0.05 * np.random.randn(80)
        corr = VGroup(*[
            Line(axes.c2p(x, 0), axes.c2p(x, max(0.01, y)), color=BLUE, stroke_width=3)
            for x, y in zip(xs, ys)
        ])
        self.play(LaggedStart(*[Create(c) for c in corr[:40]], lag_ratio=0.02), run_time=1)
        self.wait(0.1)
        self.play(LaggedStart(*[Create(c) for c in corr[40:]], lag_ratio=0.02), run_time=0.8)

        peak_label = Text("Correlation peak \u2192 Cell ID found", font_size=18, color=GREEN).next_to(axes, UP, buff=0.3)
        self.play(Write(peak_label), run_time=0.5)

        cell_id = self._tex("N_ID_cell = 3 x N_ID_1 + N_ID_2", fs=28, color=YELLOW)
        cell_id.shift(RIGHT * 3.5 + UP * 1)
        cid_desc = self._tex("Full Physical Cell Identity", fs=14, color=GREY).next_to(cell_id, DOWN, buff=0.1)
        self.play(Write(cell_id), Write(cid_desc), run_time=0.5)
        self.wait(0.5)

        self.play(
            *[FadeOut(m) for m in [axes, xl, yl, corr, peak_label, cell_id, cid_desc]],
            run_time=0.4,
        )
        self.wait(0.2)

    # ─── PHASE 2: NR Resource Grid + System Info ──────────────────
    def phase_2_system_info(self):
        self._setup_phase("System Information Acquisition", "MIB (PBCH) + SIB1 (PDSCH) on the resource grid", 2)

        # ── Resource grid ──────────────────────────────────────────
        grid_title = Text("NR Time-Frequency Resource Grid", font_size=20, color=GREY).shift(LEFT * 3 + UP * 2.2)
        self.play(Write(grid_title), run_time=0.3)

        rows, cols = 12, 14
        cell_size = 0.18
        gap = 0.02
        grid = VGroup()
        colors_map = {}
        for r in range(rows):
            for c in range(cols):
                x = (c - cols / 2) * (cell_size + gap) - 1.5
                y = (rows / 2 - r) * (cell_size + gap) + 0.5
                color = "#1a1a2e"
                if 4 <= c <= 11 and 2 <= r <= 9:
                    color = "#2d5a2d"
                if 4 <= c <= 7 and 2 <= r <= 9:
                    color = "#3a7a3a"
                rect = Square(side_length=cell_size, fill_color=color, fill_opacity=0.8, stroke_width=0.3, stroke_color="#333355")
                rect.move_to([x, y, 0])
                grid.add(rect)
                colors_map[(r, c)] = rect

        grid.shift(DOWN * 1.5)
        self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in grid], lag_ratio=0.005), run_time=1.2)

        freq_arrow = Arrow(UP * 0.3, UP * 0.7, color=GREY, stroke_width=2).next_to(grid, LEFT, buff=0.2)
        freq_lbl = Text("Freq", font_size=12, color=GREY).next_to(freq_arrow, LEFT, buff=0.05)
        time_arrow = Arrow(LEFT * 0.3, RIGHT * 0.3, color=GREY, stroke_width=2).next_to(grid, DOWN, buff=0.1)
        time_lbl = Text("Time", font_size=12, color=GREY).next_to(time_arrow, DOWN, buff=0.02)
        self.play(Create(freq_arrow), Write(freq_lbl), Create(time_arrow), Write(time_lbl), run_time=0.4)

        # ── Highlight PBCH ─────────────────────────────────────────
        pbch_box = SurroundingRectangle(
            VGroup(*[colors_map[(r, c)] for r in range(2, 10) for c in range(4, 8)]),
            color=PURPLE, stroke_width=2, buff=0.02,
        )
        pbch_lbl = Text("PBCH (MIB)", font_size=16, color=PURPLE).next_to(pbch_box, UP, buff=0.15)
        self.play(Create(pbch_box), Write(pbch_lbl), run_time=0.5)
        self.wait(0.3)

        sib1_box = SurroundingRectangle(
            VGroup(*[colors_map[(r, c)] for r in range(2, 10) for c in range(8, 12)]),
            color="#c77dff", stroke_width=2, buff=0.02,
        )
        sib1_lbl = Text("PDSCH (SIB1)", font_size=16, color="#c77dff").next_to(sib1_box, UP, buff=0.15)
        self.play(Create(sib1_box), Write(sib1_lbl), run_time=0.5)
        self.wait(0.3)

        # ── MIB bit fields ─────────────────────────────────────────
        mib_title = Text("MIB Contents (23 bits)", font_size=18, color=PURPLE).shift(RIGHT * 3 + UP * 2)
        self.play(Write(mib_title), run_time=0.3)

        mib_fields = [
            ("systemFrameNumber (6 bits)", " 6 "),
            ("subCarrierSpacingCommon (1 bit)", " 1 "),
            ("ssb-SubcarrierOffset (4 bits)", " 4 "),
            ("dmrs-TypeA-Position (1 bit)", " 1 "),
            ("pdcch-ConfigSIB1 (8 bits)", " 8 "),
            ("reserved (3 bits)", " 3 "),
        ]
        mib_group = VGroup()
        for i, (name, bits) in enumerate(mib_fields):
            r = Rectangle(width=2.8, height=0.32, fill_color=PURPLE_D, fill_opacity=0.6, stroke_width=0.5, stroke_color=PURPLE)
            r.shift(RIGHT * 3 + UP * (1.4 - i * 0.35))
            lbl = Text(name, font_size=11, color=WHITE).move_to(r.get_center()).shift(LEFT * 0.3)
            bit_r = Rectangle(width=0.5, height=0.32, fill_color=YELLOW_D, fill_opacity=0.7, stroke_width=0.5, stroke_color=YELLOW)
            bit_r.next_to(r, RIGHT, buff=0.02)
            bit_lbl = Text(bits, font_size=10, color=WHITE, weight=BOLD).move_to(bit_r.get_center())
            g = VGroup(r, lbl, bit_r, bit_lbl)
            mib_group.add(g)
            self.play(FadeIn(g, shift=LEFT * 0.2), run_time=0.2)

        self.wait(0.4)

        sib1_sched = Text("SIB1 \u2192 Period = 160 ms, SI-window = 5 ms", font_size=24, color="#c77dff")
        sib1_sched.shift(DOWN * 2.5)
        self.play(Write(sib1_sched), run_time=0.5)
        self.wait(0.5)

        self.play(
            *[FadeOut(m) for m in [grid, grid_title, pbch_box, pbch_lbl, sib1_box, sib1_lbl,
                                    mib_title, mib_group, sib1_sched, freq_arrow, freq_lbl,
                                    time_arrow, time_lbl]],
            run_time=0.4,
        )
        self.wait(0.2)

    # ─── PHASE 3: RACH — preamble math + timing advance ──────────
    def phase_3_rach(self):
        self._setup_phase("Random Access Procedure", "4-step RACH with preamble, RAR, and timing advance", 3)

        # ── Preamble sequence math ──────────────────────────────────
        title_preamble = Text("PRACH Preamble Generation", font_size=20, color=YELLOW).shift(LEFT * 4 + UP * 1.5)
        self.play(Write(title_preamble), run_time=0.3)

        prach_eq = self._tex(
            "x_u(n) = exp( -j\u03C0 u n(n+1) / N_ZC ),  0 \u2264 n < N_ZC",
            fs=26, color=YELLOW,
        ).shift(LEFT * 3.5 + UP * 0.8)
        self.play(Write(prach_eq), run_time=0.5)
        self.wait(0.2)

        prach_desc = self._tex(
            "N_ZC = 839 (FR1),  139 (FR2);  Cyclic shift C_v for Zadoff-Chu",
            fs=22, color=BLUE,
        ).next_to(prach_eq, DOWN, buff=0.2)
        self.play(Write(prach_desc), run_time=0.5)
        self.wait(0.3)

        # ── Preamble waveform ──────────────────────────────────────
        ax = Axes(
            x_range=[0, 10, 1], y_range=[-1.5, 1.5, 0.5],
            x_length=5, y_length=2,
            axis_config={"color": GREY, "font_size": 14},
        ).shift(RIGHT * 2.5 + UP * 0.5)

        cp_text = Text("Cyclic Prefix (TCP)", font_size=14, color=GREEN).next_to(ax, LEFT, buff=0.2).shift(DOWN * 1)
        seq_text = Text("Preamble Sequence (TSEQ)", font_size=14, color=YELLOW).next_to(ax, RIGHT, buff=0.1).shift(DOWN * 1)
        self.play(Create(ax), Write(cp_text), Write(seq_text), run_time=0.5)

        t_vals = np.linspace(0, 10, 200)
        waveform = VGroup()
        for i, t in enumerate(t_vals[:-1]):
            amp = 1.0 if t < 2 else (0.5 + 0.5 * np.sin(3 * (t - 2) * PI)) * np.exp(-0.1 * (t - 2))
            p1 = ax.c2p(t, amp)
            amp2 = 1.0 if t_vals[i + 1] < 2 else (0.5 + 0.5 * np.sin(3 * (t_vals[i + 1] - 2) * PI)) * np.exp(-0.1 * (t_vals[i + 1] - 2))
            p2 = ax.c2p(t_vals[i + 1], amp2)
            waveform.add(Line(p1, p2, color=YELLOW, stroke_width=2))

        self.play(Create(waveform), run_time=1.5)
        self.wait(0.3)

        # ── Timing advance ─────────────────────────────────────────
        self.play(
            *[FadeOut(m) for m in [title_preamble, prach_eq, prach_desc, ax, waveform, cp_text, seq_text]],
            run_time=0.3,
        )

        ta_title = Text("Timing Advance Calculation", font_size=20, color=GREEN).shift(LEFT * 3.5 + UP * 1.5)
        self.play(Write(ta_title), run_time=0.3)

        ta_eq1 = self._tex("N_TA = (T_Rx - T_Tx) / 2", fs=30, color=GREEN)
        ta_eq1.shift(LEFT * 3 + UP * 0.6)
        self.play(Write(ta_eq1), run_time=0.5)
        self.wait(0.2)

        ta_eq2 = self._tex("T_TA = (N_TA + N_TA_offset) x T_c", fs=28, color=BLUE)
        ta_eq2.next_to(ta_eq1, DOWN, buff=0.3)
        self.play(Write(ta_eq2), run_time=0.5)
        self.wait(0.2)

        ta_desc = Text("T_c = 0.509 ns  (basic NR time unit)", font_size=18, color=GREY)
        ta_desc.next_to(ta_eq2, DOWN, buff=0.2)
        self.play(Write(ta_desc), run_time=0.4)
        self.wait(0.3)

        # ── 4-step handshake ──────────────────────────────────────
        ue = self._box("UE", "#0f3460").shift(LEFT * 4.5 + DOWN * 1.5)
        gnb = self._box("gNB", "#16213e").shift(RIGHT * 4.5 + DOWN * 1.5)
        self.play(FadeIn(ue), FadeIn(gnb), run_time=0.4)

        rach_msgs = [
            ("MSG1: PRACH Preamble", YELLOW, ue, gnb, 1),
            ("MSG2: RAR (TA + UL grant)", GREEN, gnb, ue, -1),
            ("MSG3: RRC Setup Request", YELLOW, ue, gnb, 1),
            ("MSG4: Contention Resolution", GREEN, gnb, ue, -1),
        ]

        y_off = 1.2
        for text, color, sender, receiver, direction in rach_msgs:
            lbl = Text(text, font_size=15, color=color, weight=BOLD)
            if direction == 1:
                lbl.next_to(sender, UP, buff=y_off)
            else:
                lbl.next_to(sender, DOWN, buff=y_off)
            self.play(Write(lbl), run_time=0.25)
            arr = Arrow(sender.get_center(), receiver.get_center(), color=color, stroke_width=2, buff=0.15)
            if direction == 1:
                arr.shift(UP * (y_off - 0.15))
            else:
                arr.shift(DOWN * (y_off - 0.15))
            self.play(Create(arr), run_time=0.3)
            self.wait(0.2)
            y_off += 0.6

        self.wait(0.5)
        self.play(*[FadeOut(m) for m in [ta_title, ta_eq1, ta_eq2, ta_desc, ue, gnb]], run_time=0.3)

    # ─── PHASE 4: RRC Setup — state machine ───────────────────────
    def phase_4_rrc_setup(self):
        self._setup_phase("RRC Connection Setup", "SRB1 + RRC states and transitions", 4)

        # ── RRC states ──────────────────────────────────────────────
        states_title = Text("RRC State Machine", font_size=20, color=GREY).shift(UP * 2.2)
        self.play(Write(states_title), run_time=0.3)

        idle = self._box("RRC_IDLE", "#2a2a4e", w=2.0, h=0.8, fs=18).shift(LEFT * 4 + DOWN * 0.5)
        connected = self._box("RRC_CONNECTED", "#2a4e2a", w=2.0, h=0.8, fs=18).shift(RIGHT * 4 + DOWN * 0.5)
        inactive = self._box("RRC_INACTIVE", "#4e2a4e", w=2.0, h=0.8, fs=18).shift(DOWN * 2)

        self.play(FadeIn(idle), run_time=0.3)
        self.play(FadeIn(connected), run_time=0.3)
        self.wait(0.2)

        a1 = Arrow(idle.get_right(), connected.get_left(), color=YELLOW, stroke_width=2.5, buff=0.1)
        a1_lbl = Text("RRCSetup", font_size=14, color=YELLOW, weight=BOLD).next_to(a1, UP, buff=0.05)
        self.play(Create(a1), Write(a1_lbl), run_time=0.4)
        self.wait(0.15)

        a2 = Arrow(connected.get_left(), idle.get_right(), color=ORANGE, stroke_width=2, buff=0.1, path_arc=-0.5)
        a2_lbl = Text("RRCRelease", font_size=14, color=ORANGE, weight=BOLD).next_to(a2, DOWN, buff=0.05)
        self.play(Create(a2), Write(a2_lbl), run_time=0.4)

        self.play(FadeIn(inactive), run_time=0.3)
        a3 = Arrow(connected.get_bottom(), inactive.get_top(), color="#c77dff", stroke_width=2, buff=0.08)
        a3_lbl = Text("RRCInactive", font_size=13, color="#c77dff").next_to(a3, RIGHT, buff=0.05)
        self.play(Create(a3), Write(a3_lbl), run_time=0.35)
        self.wait(0.3)

        self.play(
            *[FadeOut(m) for m in [states_title, idle, connected, inactive, a1, a2, a3, a1_lbl, a2_lbl, a3_lbl]],
            run_time=0.3,
        )

        # ── SRB establishment ──────────────────────────────────────
        ue = self._box("UE", "#0f3460").shift(LEFT * 4 + DOWN * 0.5)
        gnb = self._box("gNB", "#16213e").shift(RIGHT * 4 + DOWN * 0.5)
        self.play(FadeIn(ue), FadeIn(gnb), run_time=0.3)

        srbs_title = Text("Signaling Radio Bearer Setup", font_size=20, color=GREEN).shift(UP * 2)
        self.play(Write(srbs_title), run_time=0.3)

        msgs = [
            ("RRCSetupRequest", YELLOW, ue, gnb, 1),
            ("RRCSetup (SRB1 config)", GREEN, gnb, ue, -1),
            ("RRCSetupComplete", YELLOW, ue, gnb, 1),
        ]
        y_off = 1.2
        for text, color, sender, receiver, direction in msgs:
            lbl = Text(text, font_size=15, color=color, weight=BOLD)
            if direction == 1:
                lbl.next_to(sender, UP, buff=y_off)
            else:
                lbl.next_to(sender, DOWN, buff=y_off)
            self.play(Write(lbl), run_time=0.25)
            arr = Arrow(sender.get_center(), receiver.get_center(), color=color, stroke_width=2, buff=0.15)
            if direction == 1:
                arr.shift(UP * (y_off - 0.15))
            else:
                arr.shift(DOWN * (y_off - 0.15))
            self.play(Create(arr), run_time=0.3)
            self.wait(0.15)
            y_off += 0.6

        srb_done = Text("SRB1 established  \u2192  NAS transport ready", font_size=18, color="#00ff88")
        srb_done.next_to(gnb, DOWN, buff=0.8)
        self.play(Write(srb_done), run_time=0.4)
        self.wait(0.5)

        self.play(*[FadeOut(m) for m in [ue, gnb, srbs_title, srb_done]], run_time=0.3)

    # ─── PHASE 5: Registration — 5G AKA key hierarchy ────────────
    def phase_5_registration(self):
        self._setup_phase("Registration & Authentication", "5G AKA \u2014 key derivation and security", 5)

        # ── Network nodes ──────────────────────────────────────────
        ue = self._box("UE", "#0f3460", w=1.5, h=0.7, fs=16).shift(LEFT * 5.5 + DOWN * 1.5)
        gnb = self._box("gNB", "#16213e", w=1.5, h=0.7, fs=16).shift(LEFT * 2.5 + DOWN * 1.5)
        amf = self._box("AMF", "#1a1a4e", w=1.5, h=0.7, fs=16).shift(RIGHT * 0.5 + DOWN * 1.5)
        ausf = self._box("AUSF", "#2d1a4e", w=1.5, h=0.7, fs=16).shift(RIGHT * 3.5 + DOWN * 1.5)

        self.play(FadeIn(ue), FadeIn(gnb), FadeIn(amf), FadeIn(ausf), run_time=0.4)

        steps = [
            ("Registration Request", ue, gnb, YELLOW),
            ("Registration Request", gnb, amf, YELLOW),
            ("Auth Vector Request", amf, ausf, ORANGE),
            ("Auth Vector Response", ausf, amf, ORANGE),
            ("Auth Request\n(RAND + AUTN)", amf, gnb, GREEN),
            ("Auth Request\n(RAND + AUTN)", gnb, ue, GREEN),
            ("Auth Response\n(RES)", ue, gnb, YELLOW),
            ("Auth Response\n(RES)", gnb, amf, YELLOW),
            ("Security Mode\nCommand", amf, gnb, GREEN),
            ("Security Mode\nCommand", gnb, ue, GREEN),
            ("Registration\nAccept", amf, gnb, "#00ff88"),
            ("Registration\nAccept", gnb, ue, "#00ff88"),
        ]

        y = 1.0
        for text, sender, receiver, color in steps:
            lbl = Text(text, font_size=11, color=color, weight=BOLD, line_spacing=0.8)
            lbl.next_to(sender, UP, buff=y)
            self.play(Write(lbl), run_time=0.2)
            arr = Arrow(sender.get_center(), receiver.get_center(), color=color, stroke_width=1.5, buff=0.12)
            self.play(Create(arr), run_time=0.2)
            y += 0.01
            self.wait(0.08)

        # ── Key hierarchy ──────────────────────────────────────────
        self.play(*[FadeOut(m) for m in [ue, gnb, amf, ausf]], run_time=0.3)
        key_title = Text("5G Key Hierarchy", font_size=20, color=GREEN).shift(UP * 2.5)
        self.play(Write(key_title), run_time=0.3)

        k_box = self._box("K (permanent)", "#e94560", w=2.8, h=0.6, fs=16).shift(UP * 1.5)
        ck_ik_box = self._box("CK || IK\n(cipher + integrity)", "#c77dff", w=2.8, h=0.7, fs=14).shift(UP * 0.5)
        kausf_box = self._box("K_AUSF", "#4a6a4a", w=2.5, h=0.6, fs=16).shift(DOWN * 0.5)
        kseaf_box = self._box("K_SEAF", "#4a4a6a", w=2.5, h=0.6, fs=16).shift(DOWN * 1.3)
        kamf_box = self._box("K_AMF", "#6a4a4a", w=2.5, h=0.6, fs=16).shift(DOWN * 2.1)
        knas_box = self._box("K_NASint + K_NASenc", "#4a6a6a", w=3.0, h=0.6, fs=15).shift(DOWN * 2.9)

        self.play(FadeIn(k_box), run_time=0.3)
        self.wait(0.1)
        self.play(FadeIn(ck_ik_box), run_time=0.3)
        a1 = Arrow(k_box.get_bottom(), ck_ik_box.get_top(), color=YELLOW, stroke_width=1.5)
        l1 = Text("KDF", font_size=14, color=YELLOW).next_to(a1, RIGHT, buff=0.05)
        self.play(Create(a1), Write(l1), run_time=0.3)

        for parent, child in [
            (ck_ik_box, kausf_box),
            (kausf_box, kseaf_box),
            (kseaf_box, kamf_box),
            (kamf_box, knas_box),
        ]:
            self.play(FadeIn(child), run_time=0.25)
            a = Arrow(parent.get_bottom(), child.get_top(), color=YELLOW, stroke_width=1.5)
            l = Text("KDF", font_size=14, color=YELLOW).next_to(a, RIGHT, buff=0.05)
            self.play(Create(a), Write(l), run_time=0.25)
            self.wait(0.08)

        self.wait(0.5)
        self.play(*[FadeOut(m) for m in [key_title, k_box, ck_ik_box, kausf_box, kseaf_box, kamf_box, knas_box, a1, l1]], run_time=0.3)

    # ─── PHASE 6: PDU Session — protocol stack + QoS ─────────────
    def phase_6_pdu_session(self):
        self._setup_phase("PDU Session Establishment", "Protocol stack, QoS flow, and GTP tunneling", 6)

        # ── Protocol stack ──────────────────────────────────────────
        stack_title = Text("User Plane Protocol Stack", font_size=20, color=GREY).shift(UP * 2.5)
        self.play(Write(stack_title), run_time=0.3)

        layers = ["SDAP", "PDCP", "RLC", "MAC", "PHY"]
        colors = ["#e94560", "#c77dff", "#4a6a4a", "#4a4a6a", "#6a4a2a"]
        ue_stack = VGroup()
        gnb_stack = VGroup()
        for i, (layer, color) in enumerate(zip(layers, colors)):
            y = 1.2 - i * 0.4
            ur = Rectangle(width=0.9, height=0.3, fill_color=color, fill_opacity=0.7, stroke_width=0).shift(LEFT * 3 + UP * y)
            ul = Text(layer, font_size=11, color=WHITE, weight=BOLD).move_to(ur.get_center())
            ue_stack.add(VGroup(ur, ul))
            gr = Rectangle(width=0.9, height=0.3, fill_color=color, fill_opacity=0.7, stroke_width=0).shift(RIGHT * 3 + UP * y)
            gl = Text(layer, font_size=11, color=WHITE, weight=BOLD).move_to(gr.get_center())
            gnb_stack.add(VGroup(gr, gl))

        self.play(
            LaggedStart(*[FadeIn(s) for s in ue_stack], lag_ratio=0.1),
            LaggedStart(*[FadeIn(s) for s in gnb_stack], lag_ratio=0.1),
            run_time=1,
        )

        ue_lbl = Text("UE", font_size=14, color=BLUE).next_to(ue_stack, LEFT, buff=0.15)
        gnb_lbl = Text("gNB / UPF", font_size=14, color=BLUE).next_to(gnb_stack, RIGHT, buff=0.15)
        self.play(Write(ue_lbl), Write(gnb_lbl), run_time=0.3)

        for i in range(5):
            y = 1.2 - i * 0.4
            a = Arrow(LEFT * 2.5 + UP * y, RIGHT * 2.5 + UP * y, color=YELLOW, stroke_width=1.5)
            self.play(Create(a), run_time=0.15)

        self.wait(0.3)

        # ── QoS flow ───────────────────────────────────────────────
        self.play(
            *[FadeOut(m) for m in [stack_title, ue_stack, gnb_stack, ue_lbl, gnb_lbl]],
            run_time=0.3,
        )

        qos_title = Text("QoS Flow \u2192 DRB Mapping", font_size=20, color=GREEN).shift(UP * 2.2)
        self.play(Write(qos_title), run_time=0.3)

        qos_flow = Rectangle(width=1.2, height=0.6, fill_color=GREEN_D, fill_opacity=0.7, stroke_width=0).shift(LEFT * 4 + DOWN * 0.3)
        qos_lbl = Text("QoS Flow", font_size=14, color=WHITE, weight=BOLD).move_to(qos_flow.get_center())
        self.play(FadeIn(VGroup(qos_flow, qos_lbl)), run_time=0.3)

        drb = Rectangle(width=1.2, height=0.6, fill_color=ORANGE, fill_opacity=0.7, stroke_width=0).shift(RIGHT * 4 + DOWN * 0.3)
        drb_lbl = Text("DRB", font_size=14, color=WHITE, weight=BOLD).move_to(drb.get_center())
        self.play(FadeIn(VGroup(drb, drb_lbl)), run_time=0.3)

        mapping = Arrow(qos_flow.get_right(), drb.get_left(), color=GREEN, stroke_width=2.5, buff=0.1)
        mapping_lbl = Text("Mapping Rule", font_size=18, color=GREEN).next_to(mapping, UP, buff=0.05)
        self.play(Create(mapping), Write(mapping_lbl), run_time=0.4)

        qos_eq = Text("5QI \u2208 {1, 2, 3, ..., 85}  |  GBR / Non-GBR / Delay-Critical", font_size=22, color=GREEN)
        qos_eq.shift(DOWN * 2)
        self.play(Write(qos_eq), run_time=0.5)
        self.wait(0.5)

        # ── GTP tunneling ──────────────────────────────────────────
        self.play(
            *[FadeOut(m) for m in [qos_title, qos_flow, qos_lbl, drb, drb_lbl, mapping, mapping_lbl, qos_eq]],
            run_time=0.3,
        )

        gtp_title = Text("GTP-U Tunneling (N3 / N9 interfaces)", font_size=20, color=ORANGE).shift(UP * 2.2)
        self.play(Write(gtp_title), run_time=0.3)

        gtp_eq = Text("GTP header: TEID (32 bit) + SeqNo + N-PDU", font_size=24, color=ORANGE)
        gtp_eq.shift(UP * 1.2)
        self.play(Write(gtp_eq), run_time=0.4)

        ip_box = self._box("UE IP: 10.10.0.x/32", "#1a4e1a", w=3.0, h=0.7, fs=18).shift(DOWN * 0.8)
        self.play(FadeIn(ip_box), run_time=0.3)

        ip_eq = Text("PDU Session type \u2192 IPv4 / IPv6 / IPv4v6", font_size=22, color="#00ff88")
        ip_eq.shift(DOWN * 1.8)
        self.play(Write(ip_eq), run_time=0.4)
        self.wait(0.5)

        self.play(*[FadeOut(m) for m in [gtp_title, gtp_eq, ip_box, ip_eq]], run_time=0.3)

    # ─── PHASE 7: Summary ──────────────────────────────────────────
    def phase_7_summary(self):
        self._setup_phase("End-to-End Summary", "6 phases of 5G Initial Setup", 7)

        phases = [
            "Cell Search  \u2014  SSB sync, PSS/SSS, Zadoff-Chu correlation",
            "System Info  \u2014  MIB (PBCH) + SIB1 (PDSCH) on resource grid",
            "Random Access  \u2014  4-step RACH, timing advance calculation",
            "RRC Setup  \u2014  SRB1, state machine (IDLE / CONNECTED / INACTIVE)",
            "Registration  \u2014  5G AKA, KDF key hierarchy",
            "PDU Session  \u2014  Protocol stack, QoS flows, GTP-U tunneling",
        ]
        colors = [BLUE, PURPLE, YELLOW, GREEN, ORANGE, "#c77dff"]

        base_y = 2.0
        for i, (phase, color) in enumerate(zip(phases, colors)):
            dot = Dot(LEFT * 5 + UP * (base_y - i * 0.65), color=color, radius=0.08)
            num = Text(f"{i+1}", font_size=12, color=WHITE, weight=BOLD).move_to(dot.get_center())
            txt = Text(phase, font_size=15, color=WHITE)
            txt.next_to(dot, RIGHT, buff=0.25)
            self.play(FadeIn(dot), Write(num), Write(txt), run_time=0.25)

        complete = Text("UE is now connected and ready for data!", font_size=26, color="#00ff88", weight=BOLD)
        complete.shift(DOWN * 2.8)
        self.play(Write(complete), run_time=0.5)
        self.wait(1)

    # ─── MAIN ──────────────────────────────────────────────────────
    def construct(self):
        self.phase_1_cell_search()
        self.wait(0.3)
        self.phase_2_system_info()
        self.wait(0.3)
        self.phase_3_rach()
        self.wait(0.3)
        self.phase_4_rrc_setup()
        self.wait(0.3)
        self.phase_5_registration()
        self.wait(0.3)
        self.phase_6_pdu_session()
        self.wait(0.3)
        self.phase_7_summary()
        self.wait(1)
