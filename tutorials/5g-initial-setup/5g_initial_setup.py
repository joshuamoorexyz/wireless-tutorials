from manim import *
import numpy as np

config.background_color = "#0a0a1a"


class FiveGInitialSetup(Scene):
    # ─── Layout constants ──────────────────────────────────────────
    TITLE_TOP = 3.2
    CONTENT_TOP = 2.0
    CONTENT_BOTTOM = -2.5
    PHASE_TAG_POS = [-7, 3.5, 0]

    # ─── Utilities ─────────────────────────────────────────────────
    def phase_header(self, num, title, subtitle):
        tag = Rectangle(width=0.8, height=0.4, fill_color="#e94560", fill_opacity=1, stroke_width=0)
        tag.move_to(self.PHASE_TAG_POS)
        n = Text(str(num), font_size=22, color=WHITE, weight=BOLD).move_to(tag.get_center())
        t = Text(title, font_size=30, color=WHITE, weight=BOLD).next_to(tag, RIGHT, buff=0.3).shift(UP * 0.03)
        st = Text(subtitle, font_size=16, color="#e94560").next_to(t, DOWN, buff=0.08).align_to(t, LEFT)
        return VGroup(tag, n, t, st)

    def eq(self, text, fs=28, color=WHITE):
        return Text(text, font_size=fs, color=color)

    def box(self, text, color="#1a1a3e", w=1.8, h=0.8, fs=20):
        r = Rectangle(width=w, height=h, fill_color=color, fill_opacity=0.85, stroke_width=1, stroke_color=WHITE)
        l = Text(text, font_size=fs, color=WHITE).move_to(r.get_center())
        return VGroup(r, l)

    def slide_in_from(self, mob, direction=LEFT):
        mob.shift(direction * config.frame_width / 2 + direction * 0.5)
        return mob

    # ─── PHASE 1: Cell Search ─────────────────────────────────────
    def phase_1_cell_search(self):
        # ── Sub 1: Tower + waves ──────────────────────────────────
        header = self.phase_header(1, "Cell Search & Synchronization", "PSS / SSS detection and frame sync")
        self.add(header)
        self.wait(0.15)

        # Tower
        pole = Rectangle(width=0.12, height=2.0, fill_color="#3a3a5a", fill_opacity=1, stroke_width=0)
        pole.shift(RIGHT * 4 + DOWN * 0.2)
        base = Rectangle(width=0.7, height=0.12, fill_color="#3a3a5a", fill_opacity=1, stroke_width=0)
        base.next_to(pole, DOWN, buff=0)
        antenna = Polygon(
            pole.get_top() + LEFT * 0.2, pole.get_top() + RIGHT * 0.2,
            pole.get_top() + UP * 0.4, stroke_width=0, fill_color="#e94560", fill_opacity=0.9,
        )
        tower = VGroup(pole, base, antenna)
        tower.next_to(header, DOWN, buff=0.5).shift(RIGHT * 2)
        self.play(DrawBorderThenFill(tower), run_time=0.8)
        gnb_lbl = Text("gNB", font_size=16, color="#e94560").next_to(antenna, UP, buff=0.1)
        self.play(Write(gnb_lbl), run_time=0.3)

        # UE
        ue_r = RoundedRectangle(width=0.9, height=0.6, corner_radius=0.1, fill_color="#0f3460", fill_opacity=1, stroke_width=0)
        ue_r.shift(LEFT * 4.5 + DOWN * 0.2)
        ue_l = Text("UE", font_size=16, color=WHITE).move_to(ue_r.get_center())
        ue = VGroup(ue_r, ue_l)
        ue.next_to(tower, LEFT, buff=3)
        self.play(DrawBorderThenFill(ue), run_time=0.5)

        # Scanning
        scan = Text("Scanning NR bands...", font_size=18, color=YELLOW).next_to(ue, UP, buff=0.4)
        self.play(Write(scan), run_time=0.3)
        self.wait(0.2)

        # Waves from tower
        self.play(FadeOut(scan), run_time=0.2)
        ssb = Text("SS/PBCH Block (PSS + SSS)", font_size=18, color=GREEN).next_to(antenna, UP, buff=0.5)
        self.play(Write(ssb), run_time=0.3)

        for _ in range(2):
            rings = VGroup()
            for r in [0.6, 1.3, 2.0]:
                c = Circle(radius=r, stroke_color=BLUE, stroke_width=1.5, stroke_opacity=1 - r * 0.3)
                c.move_to(antenna.get_top() + UP * 0.15)
                rings.add(c)
            self.play(Create(rings), run_time=0.6)
            self.wait(0.1)

        # ── Sub 2: Equations ──────────────────────────────────────
        self.play(
            FadeOut(tower, shift=DOWN * 0.3),
            FadeOut(ue, shift=DOWN * 0.3),
            FadeOut(gnb_lbl, shift=DOWN * 0.3),
            FadeOut(ssb, shift=DOWN * 0.3),
            run_time=0.4,
        )

        eq1 = self.eq("PSS:   a_u(n) = exp( -j\u03C0 u n(n+1) / N_ZC )", 32, YELLOW)
        eq1.shift(UP * 1.2)
        self.play(Write(eq1), run_time=0.6)

        eq1d = self.eq("Zadoff-Chu sequence, root indices u = 25, 29, 34", 18, GREY)
        eq1d.next_to(eq1, DOWN, buff=0.2)
        self.play(Write(eq1d), run_time=0.4)

        eq2 = self.eq("N_ZC = 127,  0 \u2264 n < N_ZC", 28, BLUE)
        eq2.next_to(eq1d, DOWN, buff=0.3)
        self.play(Write(eq2), run_time=0.4)
        self.wait(0.2)

        # Transition to SSS
        eq3 = self.eq("SSS:   d(n) = [1 - 2x\u2080(n)] \u00D7 [1 - 2x\u2081(n)]", 28, ORANGE)
        eq3.next_to(eq2, DOWN, buff=0.5)
        eq3d = self.eq("Product of two Gold-code m-sequences", 18, GREY)
        eq3d.next_to(eq3, DOWN, buff=0.2)
        self.play(Write(eq3), Write(eq3d), run_time=0.6)
        self.wait(0.3)

        cell_id = self.eq("N_ID_cell = 3N_ID\u00B9 + N_ID\u00B2", 28, YELLOW)
        cell_id.next_to(eq3d, DOWN, buff=0.4)
        cid_d = self.eq("Full Physical Cell Identity (0...1007)", 18, GREY)
        cid_d.next_to(cell_id, DOWN, buff=0.15)
        self.play(Write(cell_id), Write(cid_d), run_time=0.5)
        self.wait(0.3)

        # ── Sub 3: Correlation plot ───────────────────────────────
        self.play(
            *[FadeOut(m, shift=LEFT * 0.3) for m in [eq1, eq1d, eq2, eq3, eq3d, cell_id, cid_d]],
            run_time=0.4,
        )

        axes = Axes(
            x_range=[0, 6, 1], y_range=[0, 1.2, 0.2],
            x_length=7, y_length=2.8,
            axis_config={"color": "#555577"},
        ).shift(DOWN * 0.3)
        xl = Text("Frequency offset (subcarriers)", font_size=14, color="#555577").next_to(axes, DOWN, buff=0.15)
        yl = Text("Correlation", font_size=14, color="#555577").next_to(axes, LEFT, buff=0.35).rotate(PI / 2)
        self.play(Create(axes), Write(xl), Write(yl), run_time=0.6)

        xs = np.linspace(0, 6, 100)
        ys = 0.3 + 0.7 * np.exp(-((xs - 3) ** 2) / 0.5) + 0.03 * np.random.randn(100)
        corr_bars = VGroup(*[
            Line(axes.c2p(x, 0), axes.c2p(x, max(0.01, y)), color=BLUE, stroke_width=3.5)
            for x, y in zip(xs, ys)
        ])
        self.play(LaggedStart(*[Create(b) for b in corr_bars], lag_ratio=0.008), run_time=1.5)

        peak = Text("Correlation peak \u2192 Cell ID detected", font_size=18, color=GREEN).next_to(axes, UP, buff=0.3)
        self.play(Write(peak), run_time=0.4)
        self.wait(0.5)

        self.play(
            FadeOut(axes), FadeOut(xl), FadeOut(yl),
            FadeOut(corr_bars), FadeOut(peak),
            FadeOut(header),
            run_time=0.3,
        )
        self.wait(0.15)

    # ─── PHASE 2: System Info ─────────────────────────────────────
    def phase_2_system_info(self):
        header = self.phase_header(2, "System Information Acquisition", "MIB (PBCH) + SIB1 (PDSCH)")
        self.add(header)
        self.wait(0.15)

        # ── Resource grid ─────────────────────────────────────────
        rows, cols = 12, 14
        cell = 0.18
        gap = 0.02
        grid = VGroup()
        cmap = {}
        ox = -cols * (cell + gap) / 2
        oy = rows * (cell + gap) / 2
        for r in range(rows):
            for c in range(cols):
                x = ox + c * (cell + gap)
                y = oy - r * (cell + gap)
                color = "#14142e"
                if 4 <= c <= 11 and 2 <= r <= 9:
                    color = "#1a3a1a"
                if 4 <= c <= 7 and 2 <= r <= 9:
                    color = "#2a4a2a"
                sq = Square(side_length=cell, fill_color=color, fill_opacity=0.9, stroke_width=0.3, stroke_color="#2a2a4e")
                sq.move_to([x, y, 0])
                grid.add(sq)
                cmap[(r, c)] = sq
        grid.next_to(header, DOWN, buff=0.4)
        self.play(LaggedStart(*[FadeIn(s, scale=0.3) for s in grid], lag_ratio=0.004), run_time=1)

        # Annotations
        fa = Arrow(UP * 0.2, UP * 0.6, color="#555577", stroke_width=2).next_to(grid, LEFT, buff=0.15)
        fl = Text("Freq", font_size=12, color="#555577").next_to(fa, LEFT, buff=0.04)
        ta = Arrow(LEFT * 0.2, RIGHT * 0.2, color="#555577", stroke_width=2).next_to(grid, DOWN, buff=0.08)
        tl = Text("Time", font_size=12, color="#555577").next_to(ta, DOWN, buff=0.02)
        self.play(Create(fa), Write(fl), Create(ta), Write(tl), run_time=0.3)

        # PBCH highlight
        pbch_cells = VGroup(*[cmap[(r, c)] for r in range(2, 10) for c in range(4, 8)])
        for sq in pbch_cells:
            sq.set_fill(PURPLE_D, opacity=0.8)
        self.play(*[sq.animate.set_stroke(PURPLE, width=0.8) for sq in pbch_cells], run_time=0.4)
        pbch_l = Text("PBCH (MIB)", font_size=16, color=PURPLE).next_to(grid, UP, buff=0.4).align_to(grid, LEFT)
        self.play(Write(pbch_l), run_time=0.3)
        self.wait(0.2)

        # SIB1 highlight
        sib1_cells = VGroup(*[cmap[(r, c)] for r in range(2, 10) for c in range(8, 12)])
        for sq in sib1_cells:
            sq.set_fill("#3a1a5a", opacity=0.8)
        self.play(*[sq.animate.set_stroke("#c77dff", width=0.8) for sq in sib1_cells], run_time=0.4)
        sib1_l = Text("PDSCH (SIB1)", font_size=16, color="#c77dff").next_to(pbch_l, RIGHT, buff=0.5)
        self.play(Write(sib1_l), run_time=0.3)
        self.wait(0.3)

        # ── Transition: MIB fields ────────────────────────────────
        self.play(
            FadeOut(grid, shift=DOWN * 0.3),
            FadeOut(fa), FadeOut(fl), FadeOut(ta), FadeOut(tl),
            FadeOut(pbch_l), FadeOut(sib1_l),
            run_time=0.3,
        )

        mib_t = self.eq("MIB Contents (23 bits)", 22, PURPLE)
        mib_t.shift(UP * 2)
        self.play(Write(mib_t), run_time=0.3)

        fields = [
            ("systemFrameNumber", "6 bits"),
            ("subCarrierSpacingCommon", "1 bit"),
            ("ssb-SubcarrierOffset", "4 bits"),
            ("dmrs-TypeA-Position", "1 bit"),
            ("pdcch-ConfigSIB1", "8 bits"),
            ("reserved", "3 bits"),
        ]
        field_group = VGroup()
        for i, (name, bits) in enumerate(fields):
            r = Rectangle(width=3.2, height=0.3, fill_color=PURPLE_D, fill_opacity=0.5, stroke_width=0.5, stroke_color=PURPLE)
            y = 1.0 - i * 0.38
            r.shift(UP * y)
            nl = Text(name, font_size=13, color=WHITE).move_to(r.get_center()).shift(LEFT * 0.6)
            br = Rectangle(width=0.7, height=0.3, fill_color=YELLOW_D, fill_opacity=0.6, stroke_width=0.5, stroke_color=YELLOW)
            br.next_to(r, RIGHT, buff=0.03)
            bl = Text(bits, font_size=11, color=WHITE, weight=BOLD).move_to(br.get_center())
            g = VGroup(r, nl, br, bl)
            field_group.add(g)
            self.play(FadeIn(g, shift=LEFT * 0.15), run_time=0.2)

        self.wait(0.3)

        sib1_info = self.eq("SIB1: period = 160 ms,  SI-window = 5 ms \u2192 schedules all other SIBs", 22, "#c77dff")
        sib1_info.shift(DOWN * 2)
        self.play(Write(sib1_info), run_time=0.5)
        self.wait(0.5)

        self.play(
            *[FadeOut(m) for m in [header, mib_t, field_group, sib1_info]],
            run_time=0.3,
        )
        self.wait(0.15)

    # ─── PHASE 3: RACH ────────────────────────────────────────────
    def phase_3_rach(self):
        header = self.phase_header(3, "Random Access Procedure", "4-step RACH + timing advance")
        self.add(header)
        self.wait(0.15)

        # ── Preamble math ─────────────────────────────────────────
        pt = self.eq("PRACH Preamble", 24, YELLOW)
        pt.shift(UP * 2)
        self.play(Write(pt), run_time=0.3)

        peq1 = self.eq("x_u(n) = exp( -j\u03C0 u n(n+1) / N_ZC ),  0 \u2264 n < N_ZC", 26, YELLOW)
        peq1.shift(UP * 1.0)
        self.play(Write(peq1), run_time=0.5)

        peq1d = self.eq("N_ZC = 839 (FR1) / 139 (FR2),  cyclic shift C_v for Zadoff-Chu", 20, BLUE)
        peq1d.next_to(peq1, DOWN, buff=0.25)
        self.play(Write(peq1d), run_time=0.4)

        # Waveform
        ax = Axes(
            x_range=[0, 10, 1], y_range=[-1.5, 1.5, 0.5],
            x_length=5.5, y_length=2.2,
            axis_config={"color": "#555577"},
        )
        ax.next_to(peq1d, DOWN, buff=0.4)
        self.play(Create(ax), run_time=0.5)

        cp_lbl = Text("Cyclic Prefix", font_size=14, color=GREEN).next_to(ax, LEFT, buff=0.2).shift(DOWN * 0.8)
        seq_lbl = Text("Preamble sequence", font_size=14, color=YELLOW).next_to(ax, RIGHT, buff=0.1).shift(DOWN * 0.8)
        self.play(Write(cp_lbl), Write(seq_lbl), run_time=0.3)

        t_vals = np.linspace(0, 10, 250)
        wf = VGroup()
        for i, t in enumerate(t_vals[:-1]):
            a1 = 1.0 if t < 2 else (0.5 + 0.5 * np.sin(3 * (t - 2) * PI)) * np.exp(-0.1 * (t - 2))
            a2 = 1.0 if t_vals[i + 1] < 2 else (0.5 + 0.5 * np.sin(3 * (t_vals[i + 1] - 2) * PI)) * np.exp(-0.1 * (t_vals[i + 1] - 2))
            wf.add(Line(ax.c2p(t, a1), ax.c2p(t_vals[i + 1], a2), color=YELLOW, stroke_width=2))
        self.play(Create(wf), run_time=1.2)
        self.wait(0.3)

        # ── Timing advance ───────────────────────────────────────
        self.play(
            FadeOut(pt), FadeOut(peq1), FadeOut(peq1d),
            FadeOut(ax), FadeOut(wf), FadeOut(cp_lbl), FadeOut(seq_lbl),
            run_time=0.3,
        )

        tat = self.eq("Timing Advance", 24, GREEN)
        tat.shift(UP * 1.8)
        self.play(Write(tat), run_time=0.3)

        ta1 = self.eq("N_TA = (T_Rx - T_Tx) / 2", 30, GREEN)
        ta1.shift(UP * 0.8)
        self.play(Write(ta1), run_time=0.4)

        ta2 = self.eq("T_TA = (N_TA + N_TA_offset) \u00D7 T_c", 28, BLUE)
        ta2.next_to(ta1, DOWN, buff=0.35)
        self.play(Write(ta2), run_time=0.4)

        ta3 = self.eq("T_c = 0.509 ns  (basic NR time unit)", 20, GREY)
        ta3.next_to(ta2, DOWN, buff=0.25)
        self.play(Write(ta3), run_time=0.3)
        self.wait(0.3)

        # ── 4-step handshake ─────────────────────────────────────
        self.play(FadeOut(tat), FadeOut(ta1), FadeOut(ta2), FadeOut(ta3), run_time=0.2)

        ue = self.box("UE", "#0f3460", w=1.6, h=0.7, fs=16).shift(LEFT * 4.5 + DOWN * 0.3)
        gnb = self.box("gNB", "#16213e", w=1.6, h=0.7, fs=16).shift(RIGHT * 4.5 + DOWN * 0.3)
        self.play(DrawBorderThenFill(ue), DrawBorderThenFill(gnb), run_time=0.5)

        msgs = [
            ("MSG1: PRACH Preamble", YELLOW, ue, gnb, 1),
            ("MSG2: RAR (TA + UL grant)", GREEN, gnb, ue, -1),
            ("MSG3: RRC Setup Request", YELLOW, ue, gnb, 1),
            ("MSG4: Contention Resolution", GREEN, gnb, ue, -1),
        ]
        yo = 0.8
        for text, color, sender, receiver, direction in msgs:
            lbl = Text(text, font_size=14, color=color, weight=BOLD)
            lbl.next_to(sender, UP if direction == 1 else DOWN, buff=yo)
            self.play(Write(lbl), run_time=0.2)
            start = sender.get_center()
            end = receiver.get_center()
            arr = Arrow(start, end, color=color, stroke_width=2, buff=0.12, max_tip_length_to_length_ratio=0.15)
            if direction == 1:
                arr.shift(UP * (yo - 0.1))
            else:
                arr.shift(DOWN * (yo - 0.1))
            self.play(Create(arr), run_time=0.25)
            self.wait(0.15)
            yo += 0.5

        self.wait(0.4)
        self.play(FadeOut(ue), FadeOut(gnb), FadeOut(header), run_time=0.3)
        self.wait(0.15)

    # ─── PHASE 4: RRC Setup ──────────────────────────────────────
    def phase_4_rrc_setup(self):
        header = self.phase_header(4, "RRC Connection Setup", "SRB1 and RRC states")
        self.add(header)
        self.wait(0.15)

        # ── State machine ─────────────────────────────────────────
        st = self.eq("RRC State Machine", 22, GREY)
        st.shift(UP * 2)
        self.play(Write(st), run_time=0.3)

        idle = self.box("RRC_IDLE", "#2a2a4e", w=1.8, h=0.7, fs=17).shift(LEFT * 4 + DOWN * 0.3)
        conn = self.box("RRC_CONNECTED", "#2a4e2a", w=1.8, h=0.7, fs=17).shift(RIGHT * 4 + DOWN * 0.3)
        inact = self.box("RRC_INACTIVE", "#4e2a4e", w=1.8, h=0.7, fs=17).shift(DOWN * 1.8)

        self.play(DrawBorderThenFill(idle), DrawBorderThenFill(conn), run_time=0.4)
        self.wait(0.1)

        a1 = Arrow(idle.get_right(), conn.get_left(), color=YELLOW, stroke_width=2.5, buff=0.08)
        a1l = Text("RRCSetup", font_size=13, color=YELLOW, weight=BOLD).next_to(a1, UP, buff=0.04)
        self.play(Create(a1), Write(a1l), run_time=0.35)

        a2 = Arrow(conn.get_left(), idle.get_right(), color=ORANGE, stroke_width=2, buff=0.08, path_arc=-0.4)
        a2l = Text("RRCRelease", font_size=13, color=ORANGE, weight=BOLD).next_to(a2, DOWN, buff=0.04)
        self.play(Create(a2), Write(a2l), run_time=0.35)
        self.wait(0.1)

        self.play(DrawBorderThenFill(inact), run_time=0.25)
        a3 = Arrow(conn.get_bottom(), inact.get_top(), color="#c77dff", stroke_width=2, buff=0.06)
        a3l = Text("RRCInactive", font_size=12, color="#c77dff").next_to(a3, RIGHT, buff=0.04)
        self.play(Create(a3), Write(a3l), run_time=0.3)

        a4 = Arrow(inact.get_top(), conn.get_bottom(), color=GREEN, stroke_width=2, buff=0.06)
        a4l = Text("RRCResume", font_size=12, color=GREEN).next_to(a4, LEFT, buff=0.04)
        self.play(Create(a4), Write(a4l), run_time=0.3)
        self.wait(0.4)

        # ── SRB flow ─────────────────────────────────────────────
        self.play(
            FadeOut(st), FadeOut(idle), FadeOut(conn), FadeOut(inact),
            FadeOut(a1), FadeOut(a2), FadeOut(a3), FadeOut(a4),
            FadeOut(a1l), FadeOut(a2l), FadeOut(a3l), FadeOut(a4l),
            run_time=0.3,
        )

        ue = self.box("UE", "#0f3460", w=1.6, h=0.7, fs=16).shift(LEFT * 4 + DOWN * 0.3)
        gnb = self.box("gNB", "#16213e", w=1.6, h=0.7, fs=16).shift(RIGHT * 4 + DOWN * 0.3)
        self.play(DrawBorderThenFill(ue), DrawBorderThenFill(gnb), run_time=0.4)

        srb_t = self.eq("Signaling Radio Bearer 1", 22, GREEN)
        srb_t.shift(UP * 2)
        self.play(Write(srb_t), run_time=0.3)

        for text, color, sender, receiver, direction in [
            ("RRCSetupRequest", YELLOW, ue, gnb, 1),
            ("RRCSetup (SRB1 config)", GREEN, gnb, ue, -1),
            ("RRCSetupComplete", YELLOW, ue, gnb, 1),
        ]:
            lbl = Text(text, font_size=14, color=color, weight=BOLD)
            lbl.next_to(sender, UP if direction == 1 else DOWN, buff=0.8)
            self.play(Write(lbl), run_time=0.25)
            arr = Arrow(sender.get_center(), receiver.get_center(), color=color, stroke_width=2, buff=0.12)
            arr.shift(UP * (0.8 - 0.1) if direction == 1 else DOWN * (0.8 - 0.1))
            self.play(Create(arr), run_time=0.3)
            self.wait(0.15)

        done = Text("SRB1 established  \u2192  NAS transport ready", font_size=18, color="#00ff88")
        done.next_to(gnb, DOWN, buff=0.7)
        self.play(Write(done), run_time=0.35)
        self.wait(0.5)

        self.play(
            FadeOut(ue), FadeOut(gnb), FadeOut(srb_t), FadeOut(done),
            FadeOut(header), run_time=0.3,
        )
        self.wait(0.15)

    # ─── PHASE 5: Registration ───────────────────────────────────
    def phase_5_registration(self):
        header = self.phase_header(5, "Registration & Authentication", "5G AKA key derivation")
        self.add(header)
        self.wait(0.15)

        # ── Network flow ──────────────────────────────────────────
        ue = self.box("UE", "#0f3460", w=1.4, h=0.6, fs=15).shift(LEFT * 5.5 + DOWN * 1)
        gnb = self.box("gNB", "#16213e", w=1.4, h=0.6, fs=15).shift(LEFT * 2.5 + DOWN * 1)
        amf = self.box("AMF", "#1a1a4e", w=1.4, h=0.6, fs=15).shift(RIGHT * 0.5 + DOWN * 1)
        ausf = self.box("AUSF", "#2d1a4e", w=1.4, h=0.6, fs=15).shift(RIGHT * 3.5 + DOWN * 1)

        self.play(
            DrawBorderThenFill(ue), DrawBorderThenFill(gnb),
            DrawBorderThenFill(amf), DrawBorderThenFill(ausf),
            run_time=0.6,
        )

        steps = [
            ("Registration Req.", ue, gnb, YELLOW),
            ("Registration Req.", gnb, amf, YELLOW),
            ("Auth Vector Req.", amf, ausf, ORANGE),
            ("Auth Vector Resp.", ausf, amf, ORANGE),
            ("Auth Req.\n(RAND+AUTN)", amf, gnb, GREEN),
            ("Auth Req.\n(RAND+AUTN)", gnb, ue, GREEN),
            ("Auth Resp. (RES)", ue, gnb, YELLOW),
            ("Auth Resp. (RES)", gnb, amf, YELLOW),
            ("Security Mode", amf, gnb, GREEN),
            ("Security Mode", gnb, ue, GREEN),
            ("Reg. Accept", amf, gnb, "#00ff88"),
            ("Reg. Accept", gnb, ue, "#00ff88"),
        ]

        y = 0.7
        for text, sender, receiver, color in steps:
            lbl = Text(text, font_size=11, color=color, weight=BOLD, line_spacing=0.7)
            lbl.next_to(sender, UP, buff=y)
            self.play(Write(lbl), run_time=0.15)
            arr = Arrow(sender.get_center(), receiver.get_center(), color=color, stroke_width=1.3, buff=0.1)
            self.play(Create(arr), run_time=0.15)
            y += 0.01

        self.wait(0.3)

        # ── Key hierarchy ─────────────────────────────────────────
        self.play(FadeOut(ue), FadeOut(gnb), FadeOut(amf), FadeOut(ausf), run_time=0.3)

        kt = self.eq("5G Key Hierarchy (KDF chain)", 22, GREEN)
        kt.shift(UP * 2.2)
        self.play(Write(kt), run_time=0.3)

        def key_box(text, color, y, w=2.6):
            r = Rectangle(width=w, height=0.5, fill_color=color, fill_opacity=0.7, stroke_width=0)
            r.shift(UP * y)
            l = Text(text, font_size=15, color=WHITE, weight=BOLD).move_to(r.get_center())
            return VGroup(r, l)

        keys = [
            ("K (permanent key)", "#e94560", 1.4),
            ("CK || IK", "#c77dff", 0.6),
            ("K_AUSF", "#4a6a4a", -0.2),
            ("K_SEAF", "#4a4a6a", -1.0),
            ("K_AMF", "#6a4a4a", -1.8),
            ("K_NASint + K_NASenc", "#4a6a6a", -2.6),
        ]

        all_keys = VGroup()
        prev = None
        for i, (txt, color, y) in enumerate(keys):
            kb = key_box(txt, color, y)
            all_keys.add(kb)
            self.play(FadeIn(kb, shift=RIGHT * 0.2), run_time=0.2)
            if prev is not None:
                a = Arrow(prev.get_bottom(), kb.get_top(), color=YELLOW, stroke_width=1.5, buff=0.05)
                l = Text("KDF", font_size=12, color=YELLOW).next_to(a, RIGHT, buff=0.03)
                all_keys.add(a)
                all_keys.add(l)
                self.play(Create(a), Write(l), run_time=0.2)
            prev = kb

        self.wait(0.5)
        self.play(FadeOut(kt), FadeOut(all_keys), FadeOut(header), run_time=0.3)
        self.wait(0.15)

    # ─── PHASE 6: PDU Session ────────────────────────────────────
    def phase_6_pdu_session(self):
        header = self.phase_header(6, "PDU Session Establishment", "Protocol stack, QoS, and tunneling")
        self.add(header)
        self.wait(0.15)

        # ── Protocol stack ─────────────────────────────────────────
        st = self.eq("User Plane Protocol Stack", 22, GREY)
        st.shift(UP * 2.2)
        self.play(Write(st), run_time=0.3)

        layers = ["SDAP", "PDCP", "RLC", "MAC", "PHY"]
        colors = ["#e94560", "#c77dff", "#4a6a4a", "#4a4a6a", "#6a4a2a"]
        ue_stack = VGroup()
        gnb_stack = VGroup()
        for i, (layer, color) in enumerate(zip(layers, colors)):
            y = 1.2 - i * 0.38
            ur = Rectangle(width=0.8, height=0.28, fill_color=color, fill_opacity=0.7, stroke_width=0).shift(LEFT * 3 + UP * y)
            ul = Text(layer, font_size=11, color=WHITE, weight=BOLD).move_to(ur.get_center())
            ue_stack.add(VGroup(ur, ul))
            gr = Rectangle(width=0.8, height=0.28, fill_color=color, fill_opacity=0.7, stroke_width=0).shift(RIGHT * 3 + UP * y)
            gl = Text(layer, font_size=11, color=WHITE, weight=BOLD).move_to(gr.get_center())
            gnb_stack.add(VGroup(gr, gl))

        self.play(
            LaggedStart(*[DrawBorderThenFill(s) for s in ue_stack], lag_ratio=0.08),
            LaggedStart(*[DrawBorderThenFill(s) for s in gnb_stack], lag_ratio=0.08),
            run_time=0.8,
        )

        # Peer arrows
        for i in range(5):
            y = 1.2 - i * 0.38
            a = Arrow(LEFT * 2.5 + UP * y, RIGHT * 2.5 + UP * y, color=YELLOW, stroke_width=1.5)
            self.play(Create(a), run_time=0.12)

        self.wait(0.2)

        # ── QoS Flow ─────────────────────────────────────────────
        self.play(
            FadeOut(st), FadeOut(ue_stack), FadeOut(gnb_stack),
            run_time=0.3,
        )

        qt = self.eq("QoS Flow \u2192 DRB Mapping", 22, GREEN)
        qt.shift(UP * 2)
        self.play(Write(qt), run_time=0.3)

        qos = Rectangle(width=1.2, height=0.55, fill_color=GREEN_D, fill_opacity=0.7, stroke_width=0)
        qos.shift(LEFT * 4)
        qos_l = Text("QoS Flow", font_size=14, color=WHITE, weight=BOLD).move_to(qos.get_center())
        self.play(DrawBorderThenFill(VGroup(qos, qos_l)), run_time=0.3)

        drb = Rectangle(width=1.2, height=0.55, fill_color=ORANGE, fill_opacity=0.7, stroke_width=0)
        drb.shift(RIGHT * 4)
        drb_l = Text("DRB", font_size=14, color=WHITE, weight=BOLD).move_to(drb.get_center())
        self.play(DrawBorderThenFill(VGroup(drb, drb_l)), run_time=0.3)

        ma = Arrow(qos.get_right(), drb.get_left(), color=GREEN, stroke_width=2.5, buff=0.08)
        mal = self.eq("Mapping Rule", 18, GREEN).next_to(ma, UP, buff=0.05)
        self.play(Create(ma), Write(mal), run_time=0.35)

        qi = self.eq("5QI \u2208 {1, 2, 3, ..., 85}  |  GBR / Non-GBR / Delay-Critical", 20, GREEN)
        qi.shift(DOWN * 2)
        self.play(Write(qi), run_time=0.4)
        self.wait(0.3)

        # ── GTP tunneling ─────────────────────────────────────────
        self.play(
            FadeOut(qt), FadeOut(qos), FadeOut(qos_l),
            FadeOut(drb), FadeOut(drb_l), FadeOut(ma), FadeOut(mal), FadeOut(qi),
            run_time=0.3,
        )

        gt = self.eq("GTP-U Tunneling (N3 / N9 interfaces)", 22, ORANGE)
        gt.shift(UP * 1.8)
        self.play(Write(gt), run_time=0.3)

        geq = self.eq("GTP header: TEID (32 bit) + SeqNo + N-PDU", 24, ORANGE)
        geq.shift(UP * 0.8)
        self.play(Write(geq), run_time=0.35)

        ip = self.box("UE IP: 10.10.0.x/32", "#1a4e1a", w=2.8, h=0.6, fs=17).shift(DOWN * 0.5)
        self.play(DrawBorderThenFill(ip), run_time=0.3)

        ipt = self.eq("PDU Session type \u2192 IPv4 / IPv6 / IPv4v6", 20, "#00ff88")
        ipt.shift(DOWN * 1.5)
        self.play(Write(ipt), run_time=0.35)
        self.wait(0.5)

        self.play(
            FadeOut(gt), FadeOut(geq), FadeOut(ip), FadeOut(ipt),
            FadeOut(header), run_time=0.3,
        )
        self.wait(0.15)

    # ─── PHASE 7: Summary ─────────────────────────────────────────
    def phase_7_summary(self):
        header = self.phase_header(7, "End-to-End Summary", "6 phases of 5G Initial Setup")
        self.add(header)
        self.wait(0.15)

        phases = [
            "Cell Search  \u2014  SSB sync, PSS/SSS, Zadoff-Chu correlation",
            "System Info  \u2014  MIB (PBCH) + SIB1 (PDSCH) on resource grid",
            "Random Access  \u2014  4-step RACH, timing advance calculation",
            "RRC Setup  \u2014  SRB1, state machine (IDLE / CONNECTED / INACTIVE)",
            "Registration  \u2014  5G AKA, KDF key hierarchy",
            "PDU Session  \u2014  Protocol stack, QoS flows, GTP-U tunneling",
        ]
        colors = [BLUE, PURPLE, YELLOW, GREEN, ORANGE, "#c77dff"]

        base_y = 1.8
        for i, (phase, color) in enumerate(zip(phases, colors)):
            dot = Dot(LEFT * 5 + UP * (base_y - i * 0.62), color=color, radius=0.07)
            num = Text(f"{i+1}", font_size=11, color=WHITE, weight=BOLD).move_to(dot.get_center())
            txt = Text(phase, font_size=14, color=WHITE)
            txt.next_to(dot, RIGHT, buff=0.2)
            self.play(FadeIn(dot), Write(num), Write(txt), run_time=0.2)

        done = Text("UE is now connected and ready for data!", font_size=24, color="#00ff88", weight=BOLD)
        done.shift(DOWN * 2.8)
        self.play(Write(done), run_time=0.5)
        self.wait(1.5)

    # ─── MAIN ──────────────────────────────────────────────────────
    def construct(self):
        # Clean background
        bg = FullScreenRectangle()
        bg.set_fill(color="#0a0a1a", opacity=1)
        bg.set_stroke(width=0)
        self.add(bg)

        self.phase_1_cell_search()
        self.phase_2_system_info()
        self.phase_3_rach()
        self.phase_4_rrc_setup()
        self.phase_5_registration()
        self.phase_6_pdu_session()
        self.phase_7_summary()
