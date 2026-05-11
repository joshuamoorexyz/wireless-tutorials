from manim import *
import numpy as np

# ─── Refined color palette (Nord-inspired) ─────────────────────────
BG      = "#0d0d1a"   # very dark background
SURFACE = "#1a1a2e"   # card surface
WHITE   = "#eceff4"
GREY    = "#4c566a"
CYAN    = "#88c0d0"
TEAL    = "#8fbcbb"
RED     = "#bf616a"
ORANGE  = "#d08770"
GREEN   = "#a3be8c"
PURPLE  = "#b48ead"
YELLOW  = "#ebcb8b"
WARM    = "#d35f5f"

config.background_color = BG


class FiveGInitialSetup(Scene):
    def txt(self, text, fs=24, color=WHITE, weight=NORMAL, **kwargs):
        return Text(text, font_size=fs, color=color, weight=weight,
                    font="Helvetica Neue", **kwargs)

    def title_card(self, num, title, subtitle):
        self.clear()
        bg = FullScreenRectangle()
        bg.set_fill(color=BG, opacity=1)
        bg.set_stroke(width=0)
        self.add(bg)

        n = self.txt(str(num), 48, RED, BOLD).to_corner(UL, buff=0.4)
        t = self.txt(title, 36, WHITE, BOLD).next_to(n, RIGHT, buff=0.3).shift(UP * 0.05)
        ln = Line(t.get_left(), t.get_right(), color=RED, stroke_width=2).next_to(t, DOWN, buff=0.1)
        s = self.txt(subtitle, 18, CYAN).next_to(ln, DOWN, buff=0.1).align_to(t, LEFT)
        self.add(n, t, ln, s)

    def slide_in(self, mob, direction=RIGHT, buff=0.5):
        d = direction * (config.frame_width / 2 + buff)
        mob.shift(d)
        return mob

    def box(self, text, color=SURFACE, w=2, h=0.8, fs=18):
        r = RoundedRectangle(width=w, height=h, corner_radius=0.08,
                             fill_color=color, fill_opacity=0.85,
                             stroke_width=1, stroke_color=GREY)
        l = self.txt(text, fs, WHITE).move_to(r.get_center())
        return VGroup(r, l)

    def arrow(self, start, end, color=CYAN, sw=2):
        return Arrow(start, end, color=color, stroke_width=sw, buff=0.12,
                     max_tip_length_to_length_ratio=0.12)

    # ==================================================================
    # PHASE 1: CELL SEARCH
    # ==================================================================
    def phase_1_cell_search(self):
        # ── Concept 1: Tower + UE + Waves ──────────────────────────
        self.title_card(1, "Cell Search & Synchronization",
                        "The UE finds the network")

        tower_pole = Rectangle(width=0.12, height=2.2, fill_color="#3a3a5a",
                               fill_opacity=1, stroke_width=0)
        tower_pole.shift(RIGHT * 4 + DOWN * 0.2)
        tower_base = Rectangle(width=0.7, height=0.12, fill_color="#3a3a5a",
                               fill_opacity=1, stroke_width=0)
        tower_base.next_to(tower_pole, DOWN, buff=0)
        tower_ant = Polygon(
            tower_pole.get_top() + LEFT * 0.25,
            tower_pole.get_top() + RIGHT * 0.25,
            tower_pole.get_top() + UP * 0.45,
            stroke_width=0, fill_color=RED, fill_opacity=0.9,
        )
        tower = VGroup(tower_pole, tower_base, tower_ant)
        tower.next_to(self.txt("x"), DOWN, buff=1).shift(RIGHT * 2.5)
        self.play(DrawBorderThenFill(tower), run_time=0.6)

        gNB = self.txt("gNB", 16, RED).next_to(tower_ant, UP, buff=0.1)
        self.play(Write(gNB), run_time=0.3)

        ue_r = RoundedRectangle(width=1.0, height=0.65, corner_radius=0.1,
                                fill_color="#14325e", fill_opacity=1, stroke_width=0)
        ue_l = self.txt("UE", 18, WHITE).move_to(ue_r.get_center())
        ue = VGroup(ue_r, ue_l)
        ue.next_to(tower, LEFT, buff=3.5).shift(UP * 0.1)
        self.play(DrawBorderThenFill(ue), run_time=0.5)

        scanning = self.txt("Scanning NR frequency bands...", 18, YELLOW)
        scanning.next_to(ue, UP, buff=0.5)
        self.play(Write(scanning), run_time=0.4)

        dots = VGroup(*[
            Dot(scanning.get_right() + RIGHT * (i + 1) * 0.25, radius=0.04, color=YELLOW)
            for i in range(3)
        ])
        self.play(LaggedStart(*[FadeIn(d, scale=0) for d in dots], lag_ratio=0.15), run_time=0.4)
        self.wait(0.5)

        self.play(FadeOut(scanning), FadeOut(dots), run_time=0.2)

        ssb_label = self.txt("gNB transmits SS/PBCH Block (PSS + SSS)", 18, CYAN)
        ssb_label.next_to(tower_ant, UP, buff=0.7)
        self.play(Write(ssb_label), run_time=0.4)

        for _ in range(2):
            rings = VGroup()
            for r in [0.7, 1.5, 2.3, 3.1]:
                opacity = max(0, 1 - r * 0.25)
                c = Circle(radius=r, stroke_color=CYAN, stroke_width=1.5,
                           stroke_opacity=opacity)
                c.move_to(tower_ant.get_top() + UP * 0.2)
                rings.add(c)
            self.play(Create(rings), run_time=0.7)
            self.wait(0.15)
        self.wait(0.5)

        self.play(
            FadeOut(tower, shift=DOWN * 0.2),
            FadeOut(ue, shift=DOWN * 0.2),
            FadeOut(gNB, shift=DOWN * 0.2),
            FadeOut(ssb_label, shift=DOWN * 0.2),
            run_time=0.4,
        )

        # ── Concept 2: PSS Equation ────────────────────────────────
        self.title_card(1, "Primary Synchronization Signal (PSS)",
                        "Zadoff-Chu sequence for cell ID detection")

        pss_eq = self.txt("PSS sequence generation:", 28, WHITE)
        pss_eq.shift(UP * 2.0)
        self.play(Write(pss_eq), run_time=0.4)

        eq1 = self.txt("a_u(n) = exp( -j \u03C0 u n (n+1) / N_ZC )", 34, YELLOW)
        eq1.shift(UP * 0.8)
        self.play(Write(eq1), run_time=0.5)

        eq1a = self.txt("N_ZC = 127  (length-127 Zadoff-Chu)", 24, CYAN)
        eq1a.next_to(eq1, DOWN, buff=0.3)
        self.play(Write(eq1a), run_time=0.3)

        eq1b = self.txt("0 \u2264 n < N_ZC  |  u \u2208 {25, 29, 34}  (root indices)", 22, GREY)
        eq1b.next_to(eq1a, DOWN, buff=0.2)
        self.play(Write(eq1b), run_time=0.4)
        self.wait(0.4)

        explanation = VGroup(
            self.txt("\u2022 Each root index u produces a different sequence", 20, WHITE),
            self.txt("\u2022 UE correlates received signal against all 3 sequences", 20, WHITE),
            self.txt("\u2022 Peak correlation \u2192 detects PSS + identifies N_ID\u00B2", 20, YELLOW),
        )
        explanation.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        explanation.next_to(eq1b, DOWN, buff=0.4)
        for e in explanation:
            self.play(Write(e), run_time=0.35)
        self.wait(0.5)

        self.play(*[FadeOut(m, shift=DOWN * 0.2) for m in
                     [pss_eq, eq1, eq1a, eq1b] + list(explanation)],
                  run_time=0.3)

        # ── Concept 3: SSS Equation ────────────────────────────────
        self.title_card(1, "Secondary Synchronization Signal (SSS)",
                        "m-sequences for cell group ID")

        sss_title = self.txt("SSS uses two Gold-code m-sequences:", 28, WHITE)
        sss_title.shift(UP * 2.0)
        self.play(Write(sss_title), run_time=0.4)

        sss_eq = self.txt("d_SSS(n) = [1 - 2 x_0(n)] \u00D7 [1 - 2 x_1(n)]", 32, PURPLE)
        sss_eq.shift(UP * 0.8)
        self.play(Write(sss_eq), run_time=0.5)

        sss_d = self.txt("x_0 and x_1 are length-127 m-sequences with different shifts", 22, CYAN)
        sss_d.next_to(sss_eq, DOWN, buff=0.3)
        self.play(Write(sss_d), run_time=0.4)
        self.wait(0.3)

        cell_eq = self.txt("N_ID_cell = 3 \u00D7 N_ID\u00B9 + N_ID\u00B2", 36, YELLOW)
        cell_eq.shift(DOWN * 0.5)
        cell_d = self.txt("Full Physical Cell Identity  (0 \u2013 1007)", 22, GREY)
        cell_d.next_to(cell_eq, DOWN, buff=0.2)
        self.play(Write(cell_eq), Write(cell_d), run_time=0.6)
        self.wait(0.3)

        cell_breakdown = VGroup(
            self.txt("\u2022 N_ID\u00B2 = PSS index  (0, 1, 2)  \u2192 3 possible values", 20, WHITE),
            self.txt("\u2022 N_ID\u00B9 = SSS index  (0, 1, ..., 335)  \u2192 336 possible values", 20, WHITE),
            self.txt("\u2022 Total:  3 \u00D7 336 = 1008 unique Physical Cell IDs", 20, YELLOW),
        )
        cell_breakdown.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        cell_breakdown.next_to(cell_d, DOWN, buff=0.3)
        for e in cell_breakdown:
            self.play(Write(e), run_time=0.3)
        self.wait(0.5)

        self.play(*[FadeOut(m, shift=DOWN * 0.2) for m in
                     [sss_title, sss_eq, sss_d, cell_eq, cell_d] + list(cell_breakdown)],
                  run_time=0.3)

        # ── Concept 4: Correlation Plot ────────────────────────────
        self.title_card(1, "PSS Correlation at the UE",
                        "Detecting the strongest cell")

        axes = Axes(
            x_range=[-3, 3, 1], y_range=[0, 1.2, 0.2],
            x_length=8, y_length=3,
            axis_config={"color": GREY},
            x_axis_config={"label_direction": DOWN},
            y_axis_config={"label_direction": LEFT},
        ).shift(DOWN * 0.2)
        xl = self.txt("Subcarrier offset", 14, GREY).next_to(axes, DOWN, buff=0.15)
        yl = self.txt("Correlation", 14, GREY).next_to(axes, LEFT, buff=0.3).rotate(PI / 2)
        self.play(Create(axes), Write(xl), Write(yl), run_time=0.6)

        xs = np.linspace(-3, 3, 120)
        ys = 0.3 + 0.7 * np.exp(-((xs) ** 2) / 0.4) + 0.02 * np.random.randn(120)
        bars = VGroup(*[
            Line(axes.c2p(x, 0), axes.c2p(x, max(0.01, y)),
                 color=CYAN, stroke_width=3)
            for x, y in zip(xs, ys)
        ])
        self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.005), run_time=1.5)
        self.wait(0.3)

        peak = self.txt("Peak  \u2192  Strongest PSS detected", 22, YELLOW)
        peak.next_to(axes, UP, buff=0.3)
        self.play(Write(peak), run_time=0.4)

        peak_arrow = Arrow(peak.get_bottom(), axes.c2p(0, 0.98), color=YELLOW, stroke_width=2)
        self.play(Create(peak_arrow), run_time=0.3)
        self.wait(0.5)

        detail = VGroup(
            self.txt("\u2022 UE slides a window across the received signal", 18, WHITE),
            self.txt("\u2022 Computes cross-correlation with each PSS candidate", 18, WHITE),
            self.txt("\u2022 Peak location gives frame timing + frequency offset", 18, GREEN),
        )
        detail.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        detail.next_to(axes, DOWN, buff=0.4).shift(LEFT)
        for e in detail:
            self.play(Write(e), run_time=0.3)
        self.wait(0.8)

        self.play(*[FadeOut(m, shift=DOWN * 0.2) for m in
                     [axes, xl, yl, bars, peak, peak_arrow] + list(detail)],
                  run_time=0.3)

    # ==================================================================
    # PHASE 2: SYSTEM INFORMATION
    # ==================================================================
    def phase_2_system_info(self):
        # ── Concept 1: NR Resource Grid ────────────────────────────
        self.title_card(2, "System Information Acquisition",
                        "Reading MIB and SIB1")

        grid_title = self.txt("NR Time-Frequency Resource Grid", 22, WHITE)
        grid_title.shift(UP * 2.0)
        self.play(Write(grid_title), run_time=0.3)

        rows, cols = 12, 14
        cs = 0.16
        gap = 0.015
        ox = -cols * (cs + gap) / 2 - 1
        oy = rows * (cs + gap) / 2 + 0.3
        grid = VGroup()
        cm = {}
        for r in range(rows):
            for c in range(cols):
                x = ox + c * (cs + gap)
                y = oy - r * (cs + gap)
                color = "#14142e"
                if 4 <= c <= 11 and 2 <= r <= 9:
                    color = "#162e16"
                if 4 <= c <= 7 and 2 <= r <= 9:
                    color = "#1e3a1e"
                sq = Square(side_length=cs, fill_color=color, fill_opacity=0.9,
                            stroke_width=0.2, stroke_color="#2a2a4e")
                sq.move_to([x, y, 0])
                grid.add(sq)
                cm[(r, c)] = sq
        grid.shift(DOWN * 0.5)
        self.play(LaggedStart(*[FadeIn(s, scale=0.3) for s in grid],
                              lag_ratio=0.003), run_time=1)

        fa = Arrow(UP * 0.2, UP * 0.5, color=GREY, stroke_width=2).next_to(grid, LEFT, buff=0.12)
        fl = self.txt("Freq", 11, GREY).next_to(fa, LEFT, buff=0.03)
        ta = Arrow(LEFT * 0.2, RIGHT * 0.2, color=GREY, stroke_width=2).next_to(grid, DOWN, buff=0.06)
        tl = self.txt("Time (symbols)", 11, GREY).next_to(ta, DOWN, buff=0.02)
        self.play(Create(fa), Write(fl), Create(ta), Write(tl), run_time=0.3)

        pbch = VGroup(*[cm[(r, c)] for r in range(2, 10) for c in range(4, 8)])
        for sq in pbch:
            sq.set_fill("#3a2a5a", opacity=0.9)
        self.play(*[sq.animate.set_stroke(PURPLE, width=0.6) for sq in pbch], run_time=0.3)
        pbch_l = self.txt("PBCH  (MIB)", 16, PURPLE).next_to(grid, UP, buff=0.3).align_to(grid, LEFT)
        self.play(Write(pbch_l), run_time=0.3)

        sib1 = VGroup(*[cm[(r, c)] for r in range(2, 10) for c in range(8, 12)])
        for sq in sib1:
            sq.set_fill("#2a1a4a", opacity=0.9)
        self.play(*[sq.animate.set_stroke(CYAN, width=0.6) for sq in sib1], run_time=0.3)
        sib1_l = self.txt("PDSCH  (SIB1)", 16, CYAN).next_to(pbch_l, RIGHT, buff=0.6)
        self.play(Write(sib1_l), run_time=0.3)

        note = self.txt("SSB occupies symbols 4\u201311 in slot 0 of every half-frame", 18, GREY)
        note.next_to(grid, DOWN, buff=0.35)
        self.play(Write(note), run_time=0.4)
        self.wait(0.5)

        self.play(*[FadeOut(m, shift=DOWN * 0.15) for m in
                     [grid_title, grid, fa, fl, ta, tl, pbch_l, sib1_l, note]],
                  run_time=0.3)

        # ── Concept 2: MIB Bit Fields ──────────────────────────────
        self.title_card(2, "Master Information Block (MIB)",
                        "23 bits of essential cell parameters")

        mib_t = self.txt("MIB Fields", 24, WHITE)
        mib_t.shift(UP * 2.2)
        self.play(Write(mib_t), run_time=0.3)

        fields = [
            ("systemFrameNumber", "6 bits", "High bits of SFN (10-bit frame number)"),
            ("subCarrierSpacingCommon", "1 bit", "15 kHz or 30 kHz for SIB1, MSG2, MSG4"),
            ("ssb-SubcarrierOffset", "4 bits", "Frequency offset of SSB relative to CRB"),
            ("dmrs-TypeA-Position", "1 bit", "Position of DMRS in slot (symbol 2 or 3)"),
            ("pdcch-ConfigSIB1", "8 bits", "PDCCH search space + CORESET for SIB1"),
            ("reserved", "3 bits", "Reserved for future use"),
        ]
        fg = VGroup()
        for i, (name, bits, desc) in enumerate(fields):
            y = 1.3 - i * 0.42
            nr = RoundedRectangle(width=2.4, height=0.3, corner_radius=0.04,
                                   fill_color=PURPLE, fill_opacity=0.2,
                                   stroke_width=0.5, stroke_color=PURPLE)
            nr.shift(UP * y + LEFT * 1.5)
            nl = self.txt(name, 13, WHITE).move_to(nr.get_center()).shift(LEFT * 0.3)
            br = RoundedRectangle(width=0.55, height=0.3, corner_radius=0.04,
                                   fill_color=YELLOW, fill_opacity=0.2,
                                   stroke_width=0.5, stroke_color=YELLOW)
            br.next_to(nr, RIGHT, buff=0.03)
            bl = self.txt(bits, 10, YELLOW, BOLD).move_to(br.get_center())
            dl = self.txt(desc, 12, GREY)
            dl.next_to(nr, RIGHT, buff=0.7).align_to(nr, UP).shift(UP * 0.02)
            g = VGroup(nr, nl, br, bl, dl)
            fg.add(g)
            self.play(FadeIn(g, shift=LEFT * 0.1), run_time=0.2)
        self.wait(0.5)

        self.play(*[FadeOut(m, shift=RIGHT * 0.15) for m in [mib_t] + list(fg)],
                  run_time=0.3)

        # ── Concept 3: SIB1 Scheduling ─────────────────────────────
        self.title_card(2, "System Information Block 1 (SIB1)",
                        "Cell access parameters")

        sib1_t = self.txt("SIB1 provides:", 28, WHITE)
        sib1_t.shift(UP * 1.8)
        self.play(Write(sib1_t), run_time=0.3)

        items = [
            "PLMN identity list",
            "Tracking Area Code (TAC)",
            "Cell identity (gNB ID + cell ID)",
            "Cell barring status",
            "Scheduling info for all other SIBs (SI messages)",
        ]
        ig = VGroup()
        for i, item in enumerate(items):
            dot = Dot(LEFT * 4 + UP * (0.8 - i * 0.4), color=CYAN, radius=0.05)
            it = self.txt(item, 20, WHITE).next_to(dot, RIGHT, buff=0.2)
            ig.add(VGroup(dot, it))
            self.play(FadeIn(dot), Write(it), run_time=0.25)

        sched = self.txt("SIB1 period: 160 ms  |  SI-window length: 5 ms", 22, YELLOW)
        sched.shift(DOWN * 2.2)
        self.play(Write(sched), run_time=0.4)
        self.wait(0.8)

        self.play(*[FadeOut(m, shift=DOWN * 0.15) for m in
                     [sib1_t, sched] + list(ig)], run_time=0.3)

    # ==================================================================
    # PHASE 3: RANDOM ACCESS
    # ==================================================================
    def phase_3_rach(self):
        # ── Concept 1: PRACH Preamble ──────────────────────────────
        self.title_card(3, "Random Access Procedure",
                        "PRACH preamble generation")

        prach_t = self.txt("PRACH Preamble Sequence (also Zadoff-Chu)", 28, WHITE)
        prach_t.shift(UP * 1.8)
        self.play(Write(prach_t), run_time=0.4)

        prach_eq = self.txt("x_u(n) = exp( -j\u03C0 u n (n+1) / N_ZC )", 32, YELLOW)
        prach_eq.shift(UP * 0.7)
        self.play(Write(prach_eq), run_time=0.5)

        prach_d = VGroup(
            self.txt("N_ZC = 839  (FR1, sub-6 GHz)", 22, CYAN),
            self.txt("N_ZC = 139  (FR2, mmWave)", 22, CYAN),
            self.txt("Cyclic shift C_v creates multiple preambles per root", 22, GREY),
            self.txt("64 preambles per cell (derived from multiple roots)", 22, GREY),
        )
        prach_d.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        prach_d.next_to(prach_eq, DOWN, buff=0.3)
        for e in prach_d:
            self.play(Write(e), run_time=0.3)
        self.wait(0.5)

        self.play(*[FadeOut(m, shift=LEFT * 0.2) for m in
                     [prach_t, prach_eq] + list(prach_d)], run_time=0.3)

        # ── Concept 2: Preamble Waveform ───────────────────────────
        self.title_card(3, "Preamble in the Time Domain",
                        "Cyclic prefix + sequence")

        ax = Axes(
            x_range=[0, 10, 1], y_range=[-1.6, 1.6, 0.5],
            x_length=7, y_length=2.5,
            axis_config={"color": GREY},
        ).shift(DOWN * 0.2)
        self.play(Create(ax), run_time=0.4)

        cp_lbl = self.txt("Cyclic Prefix", 16, GREEN).next_to(ax, LEFT, buff=0.15).shift(DOWN * 0.7)
        seq_lbl = self.txt("Preamble Sequence", 16, YELLOW).next_to(ax, RIGHT, buff=0.1).shift(DOWN * 0.7)
        self.play(Write(cp_lbl), Write(seq_lbl), run_time=0.3)

        t_vals = np.linspace(0, 10, 300)
        wf = VGroup()
        for i, t in enumerate(t_vals[:-1]):
            a1 = 1.0 if t < 2 else (0.5 + 0.5 * np.sin(3 * (t - 2) * PI)) * np.exp(-0.08 * (t - 2))
            a2 = 1.0 if t_vals[i + 1] < 2 else (0.5 + 0.5 * np.sin(3 * (t_vals[i + 1] - 2) * PI)) * np.exp(-0.08 * (t_vals[i + 1] - 2))
            wf.add(Line(ax.c2p(t, a1), ax.c2p(t_vals[i + 1], a2), color=YELLOW, stroke_width=2))
        self.play(Create(wf), run_time=1.5)

        cp_highlight = Rectangle(
            width=ax.c2p(2, 0)[0] - ax.c2p(0, 0)[0],
            height=ax.c2p(0, 1.5)[1] - ax.c2p(0, -1.5)[1],
            fill_color=GREEN, fill_opacity=0.08, stroke_width=0,
        ).move_to(ax.c2p(1, 0))
        self.add(cp_highlight)
        self.wait(0.5)

        self.play(*[FadeOut(m, shift=DOWN * 0.15) for m in
                     [ax, cp_lbl, seq_lbl, wf, cp_highlight]], run_time=0.3)

        # ── Concept 3: Timing Advance ──────────────────────────────
        self.title_card(3, "Timing Advance (TA)",
                        "Compensating for propagation delay")

        ta_t = self.txt("The gNB measures round-trip delay:", 28, WHITE)
        ta_t.shift(UP * 1.8)
        self.play(Write(ta_t), run_time=0.4)

        ta_eq1 = self.txt("N_TA = (T_Rx - T_Tx) / 2", 34, GREEN)
        ta_eq1.shift(UP * 0.6)
        self.play(Write(ta_eq1), run_time=0.5)

        ta_d1 = self.txt("T_Rx = time gNB receives preamble", 20, WHITE)
        ta_d2 = self.txt("T_Tx = time UE sent preamble", 20, WHITE)
        dg = VGroup(ta_d1, ta_d2)
        dg.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        dg.next_to(ta_eq1, DOWN, buff=0.2).shift(LEFT * 0.5)
        for d in dg:
            self.play(Write(d), run_time=0.25)
        self.wait(0.3)

        ta_eq2 = self.txt("T_TA = (N_TA + N_TA_offset) \u00D7 T_c", 32, CYAN)
        ta_eq2.shift(DOWN * 0.8)
        ta_eq2_d = self.txt("T_c = 0.509 ns  (basic NR time unit)", 20, GREY)
        ta_eq2_d.next_to(ta_eq2, DOWN, buff=0.2)
        self.play(Write(ta_eq2), Write(ta_eq2_d), run_time=0.5)
        self.wait(0.3)

        ta_effect = VGroup(
            self.txt("\u2022 TA ensures UE uplink arrives in correct Rx window", 20, GREEN),
            self.txt("\u2022 gNB sends TA value in RAR (MSG2)", 20, GREEN),
            self.txt("\u2022 UE adjusts its uplink timing accordingly", 20, GREEN),
        )
        ta_effect.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        ta_effect.shift(DOWN * 1.8 + LEFT * 0.5)
        for e in ta_effect:
            self.play(Write(e), run_time=0.3)
        self.wait(0.5)

        self.play(*[FadeOut(m, shift=RIGHT * 0.15) for m in
                     [ta_t, ta_eq1, ta_eq2, ta_eq2_d, ta_d1, ta_d2] + list(ta_effect)],
                  run_time=0.3)

        # ── Concept 4: 4-Step Handshake ────────────────────────────
        self.title_card(3, "4-Step Random Access Handshake",
                        "MSG1 \u2192 MSG4")

        ue = self.box("UE", "#14325e", w=1.6, h=0.65, fs=17)
        ue.shift(LEFT * 4.5)
        gnb = self.box("gNB", "#16213e", w=1.6, h=0.65, fs=17)
        gnb.shift(RIGHT * 4.5)
        self.play(DrawBorderThenFill(ue), DrawBorderThenFill(gnb), run_time=0.5)

        msgs = [
            ("MSG1: PRACH Preamble", YELLOW, ue, gnb),
            ("MSG2: RAR (TA + UL grant)", GREEN, gnb, ue),
            ("MSG3: RRC Setup Request", YELLOW, ue, gnb),
            ("MSG4: Contention Resolution", GREEN, gnb, ue),
        ]

        yo = 0.7
        for text, color, sender, receiver in msgs:
            lbl = self.txt(text, 16, color, BOLD)
            lbl.next_to(sender, UP, buff=yo)
            self.play(Write(lbl), run_time=0.2)
            arr = self.arrow(sender.get_center(), receiver.get_center(), color)
            arr.shift(UP * (yo - 0.1))
            self.play(Create(arr), run_time=0.25)
            self.wait(0.25)
            yo += 0.5

        note = self.txt("After MSG4: Contention resolved \u2192 UE uniquely identified on the cell", 20, GREEN)
        note.shift(DOWN * 2.5)
        self.play(Write(note), run_time=0.4)
        self.wait(0.8)

        self.play(*[FadeOut(m, shift=DOWN * 0.15) for m in
                     [ue, gnb, note]], run_time=0.3)

    # ==================================================================
    # PHASE 4: RRC SETUP
    # ==================================================================
    def phase_4_rrc_setup(self):
        # ── Concept 1: State Machine ───────────────────────────────
        self.title_card(4, "RRC Connection Setup",
                        "RRC state machine and transitions")

        st = self.txt("RRC States in 5G", 26, WHITE)
        st.shift(UP * 2.0)
        self.play(Write(st), run_time=0.3)

        idle = self.box("RRC_IDLE", "#2a2a4e", w=1.8, h=0.7, fs=17)
        idle.shift(LEFT * 4.5)
        conn = self.box("RRC_CONNECTED", "#1e4a1e", w=1.8, h=0.7, fs=17)
        conn.shift(RIGHT * 4.5)
        inact = self.box("RRC_INACTIVE", "#4a2a4a", w=1.8, h=0.7, fs=17)
        inact.shift(DOWN * 1.5)

        self.play(DrawBorderThenFill(idle), DrawBorderThenFill(conn), run_time=0.4)

        a1 = self.arrow(idle.get_right(), conn.get_left(), YELLOW)
        a1l = self.txt("RRCSetup", 13, YELLOW, BOLD).next_to(a1, UP, buff=0.03)
        self.play(Create(a1), Write(a1l), run_time=0.35)

        a2 = Arrow(conn.get_left(), idle.get_right(), color=ORANGE, stroke_width=2,
                   buff=0.08, path_arc=-0.4, max_tip_length_to_length_ratio=0.12)
        a2l = self.txt("RRCRelease", 13, ORANGE, BOLD).next_to(a2, DOWN, buff=0.03)
        self.play(Create(a2), Write(a2l), run_time=0.35)
        self.play(DrawBorderThenFill(inact), run_time=0.25)

        a3 = self.arrow(conn.get_bottom(), inact.get_top(), PURPLE)
        a3l = self.txt("RRCInactive", 12, PURPLE).next_to(a3, RIGHT, buff=0.03)
        self.play(Create(a3), Write(a3l), run_time=0.3)

        a4 = self.arrow(inact.get_top(), conn.get_bottom(), GREEN)
        a4l = self.txt("RRCResume", 12, GREEN).next_to(a4, LEFT, buff=0.03)
        self.play(Create(a4), Write(a4l), run_time=0.3)

        descs = VGroup(
            self.txt("RRC_IDLE: no connection, DRX paging, small data via RACH", 15, GREY),
            self.txt("RRC_CONNECTED: full RRC context, data transfer", 15, GREY),
            self.txt("RRC_INACTIVE: suspended, retains UE context (new in 5G)", 15, GREY),
        )
        descs.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        descs.shift(DOWN * 2.8 + LEFT * 2)
        for d in descs:
            self.play(Write(d), run_time=0.25)
        self.wait(0.5)

        self.play(*[FadeOut(m, shift=DOWN * 0.15) for m in
                     [st, idle, conn, inact, a1, a2, a3, a4,
                      a1l, a2l, a3l, a4l] + list(descs)], run_time=0.3)

        # ── Concept 2: SRB1 Flow ──────────────────────────────────
        self.title_card(4, "Signaling Radio Bearer (SRB1)",
                        "Establishing the RRC signaling channel")

        srb_t = self.txt("SRB1 carries RRC + NAS messages between UE and gNB", 22, WHITE)
        srb_t.shift(UP * 2)
        self.play(Write(srb_t), run_time=0.4)

        ue = self.box("UE", "#14325e", w=1.6, h=0.65, fs=17)
        ue.shift(LEFT * 4)
        gnb = self.box("gNB", "#16213e", w=1.6, h=0.65, fs=17)
        gnb.shift(RIGHT * 4)
        self.play(DrawBorderThenFill(ue), DrawBorderThenFill(gnb), run_time=0.4)

        for text, color, sender, receiver in [
            ("RRCSetupRequest", YELLOW, ue, gnb),
            ("RRCSetup (SRB1 params)", CYAN, gnb, ue),
            ("RRCSetupComplete\n(+ NAS Registration Req.)", YELLOW, ue, gnb),
        ]:
            lbl = self.txt(text, 15, color, BOLD)
            lbl.next_to(sender, UP, buff=0.7)
            self.play(Write(lbl), run_time=0.25)
            arr = self.arrow(sender.get_center(), receiver.get_center(), color)
            arr.shift(UP * 0.6)
            self.play(Create(arr), run_time=0.25)
            self.wait(0.25)

        result = self.txt("SRB1 established  \u2192  NAS transport ready", 20, GREEN)
        result.shift(DOWN * 2.2)
        self.play(Write(result), run_time=0.4)
        self.wait(0.8)

        self.play(FadeOut(ue), FadeOut(gnb), FadeOut(srb_t), FadeOut(result), run_time=0.3)

    # ==================================================================
    # PHASE 5: REGISTRATION
    # ==================================================================
    def phase_5_registration(self):
        # ── Concept 1: Network Message Flow ────────────────────────
        self.title_card(5, "Registration & Authentication",
                        "UE \u2192 gNB \u2192 AMF \u2192 AUSF")

        flow_t = self.txt("Registration message flow through the 5G core", 22, WHITE)
        flow_t.shift(UP * 2.2)
        self.play(Write(flow_t), run_time=0.3)

        nodes_data = [
            ("UE", "#14325e", LEFT * 5.5),
            ("gNB", "#16213e", LEFT * 2.5),
            ("AMF", "#1a1a3e", RIGHT * 0.5),
            ("AUSF", "#2a1a3e", RIGHT * 3.5),
        ]
        nodes = {}
        for name, color, pos in nodes_data:
            b = self.box(name, color, w=1.3, h=0.55, fs=16)
            b.shift(pos + DOWN * 0.8)
            nodes[name] = b
            self.play(DrawBorderThenFill(b), run_time=0.3)

        steps = [
            ("Registration Request", YELLOW, "UE", "gNB"),
            ("Registration Request", YELLOW, "gNB", "AMF"),
            ("Auth Vector Request", ORANGE, "AMF", "AUSF"),
            ("Auth Vector Response", ORANGE, "AUSF", "AMF"),
            ("Auth Request\n(RAND + AUTN)", CYAN, "AMF", "gNB"),
            ("Auth Request\n(RAND + AUTN)", CYAN, "gNB", "UE"),
            ("Auth Response (RES)", YELLOW, "UE", "gNB"),
            ("Auth Response (RES)", YELLOW, "gNB", "AMF"),
            ("Security Mode", GREEN, "AMF", "gNB"),
            ("Security Mode", GREEN, "gNB", "UE"),
            ("Registration Accept", TEAL, "AMF", "gNB"),
            ("Registration Accept", TEAL, "gNB", "UE"),
        ]

        y = 0.5
        for text, color, s_name, r_name in steps:
            sender = nodes[s_name]
            receiver = nodes[r_name]
            lbl = self.txt(text, 11, color, BOLD, line_spacing=0.7)
            lbl.next_to(sender, UP, buff=y)
            self.play(Write(lbl), run_time=0.12)
            arr = self.arrow(sender.get_center(), receiver.get_center(), color, sw=1.2)
            self.play(Create(arr), run_time=0.12)
            y += 0.01

        self.wait(0.5)
        self.play(*[FadeOut(m, shift=DOWN * 0.1) for m in
                     [flow_t] + list(nodes.values())], run_time=0.3)

        # ── Concept 2: Key Hierarchy ──────────────────────────────
        self.title_card(5, "5G Authentication and Key Hierarchy",
                        "KDF chain from USIM to NAS keys")

        kh_t = self.txt("Key Derivation Process", 26, WHITE)
        kh_t.shift(UP * 2.2)
        self.play(Write(kh_t), run_time=0.3)

        def key_box(text, color, y, w=2.8):
            r = RoundedRectangle(width=w, height=0.5, corner_radius=0.05,
                                  fill_color=color, fill_opacity=0.25,
                                  stroke_width=1, stroke_color=color)
            r.shift(UP * y)
            l = self.txt(text, 16, WHITE, BOLD).move_to(r.get_center())
            return VGroup(r, l)

        keys = [
            ("K  (permanent key on USIM)", RED, 1.6),
            ("CK  ||  IK  (cipher + integrity)", PURPLE, 0.8),
            ("K_AUSF  (anchor key in AUSF)", CYAN, 0.0),
            ("K_SEAF  (security anchor in SEAF)", TEAL, -0.8),
            ("K_AMF  (AMF key)", ORANGE, -1.6),
            ("K_NASint + K_NASenc  (NAS security)", GREEN, -2.4),
        ]

        prev = None
        all_k = VGroup()
        for txt, color, y in keys:
            kb = key_box(txt, color, y)
            all_k.add(kb)
            self.play(FadeIn(kb, shift=RIGHT * 0.2), run_time=0.2)
            if prev is not None:
                a = Arrow(prev.get_bottom(), kb.get_top(), color=YELLOW,
                          stroke_width=1.5, buff=0.04)
                l = self.txt("KDF", 12, YELLOW).next_to(a, RIGHT, buff=0.03)
                all_k.add(a, l)
                self.play(Create(a), Write(l), run_time=0.2)
            prev = kb

        note = self.txt("Each KDF uses: subscriber SUPI, SN-name, freshness parameter (ABBA)", 18, GREY)
        note.shift(DOWN * 3 + LEFT * 1)
        self.play(Write(note), run_time=0.4)
        self.wait(0.8)

        self.play(FadeOut(kh_t), FadeOut(all_k), FadeOut(note), run_time=0.3)

    # ==================================================================
    # PHASE 6: PDU SESSION
    # ==================================================================
    def phase_6_pdu_session(self):
        # ── Concept 1: Protocol Stack ─────────────────────────────
        self.title_card(6, "PDU Session Establishment",
                        "User plane protocol stack")

        st = self.txt("5G User Plane Protocol Layers", 24, WHITE)
        st.shift(UP * 2.2)
        self.play(Write(st), run_time=0.3)

        layers = ["SDAP", "PDCP", "RLC", "MAC", "PHY"]
        colors = [RED, PURPLE, CYAN, TEAL, ORANGE]
        ue_stack = VGroup()
        gnb_stack = VGroup()
        for i, (layer, color) in enumerate(zip(layers, colors)):
            y = 1.2 - i * 0.38
            ur = RoundedRectangle(width=0.8, height=0.28, corner_radius=0.04,
                                   fill_color=color, fill_opacity=0.3,
                                   stroke_width=0.5, stroke_color=color)
            ur.shift(LEFT * 3 + UP * y)
            ul = self.txt(layer, 12, WHITE, BOLD).move_to(ur.get_center())
            ue_stack.add(VGroup(ur, ul))
            gr = RoundedRectangle(width=0.8, height=0.28, corner_radius=0.04,
                                   fill_color=color, fill_opacity=0.3,
                                   stroke_width=0.5, stroke_color=color)
            gr.shift(RIGHT * 3 + UP * y)
            gl = self.txt(layer, 12, WHITE, BOLD).move_to(gr.get_center())
            gnb_stack.add(VGroup(gr, gl))

        self.play(
            LaggedStart(*[DrawBorderThenFill(s) for s in ue_stack], lag_ratio=0.07),
            LaggedStart(*[DrawBorderThenFill(s) for s in gnb_stack], lag_ratio=0.07),
            run_time=0.8,
        )

        ue_l = self.txt("UE", 14, RED).next_to(ue_stack, LEFT, buff=0.12)
        gnb_l = self.txt("gNB / UPF", 14, RED).next_to(gnb_stack, RIGHT, buff=0.12)
        self.play(Write(ue_l), Write(gnb_l), run_time=0.3)

        for i in range(5):
            y = 1.2 - i * 0.38
            a = self.arrow(LEFT * 2.5 + UP * y, RIGHT * 2.5 + UP * y, YELLOW)
            self.play(Create(a), run_time=0.1)

        funcs = VGroup(
            self.txt("SDAP: QoS flow mapping", 14, GREY),
            self.txt("PDCP: ciphering, integrity, header compression", 14, GREY),
            self.txt("RLC: segmentation, ARQ retransmission", 14, GREY),
            self.txt("MAC: scheduling, HARQ, multiplexing", 14, GREY),
            self.txt("PHY: OFDM, coding, MIMO", 14, GREY),
        )
        funcs.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        funcs.shift(DOWN * 1.5 + LEFT * 0.5)
        for f in funcs:
            self.play(Write(f), run_time=0.2)
        self.wait(0.5)

        self.play(*[FadeOut(m, shift=LEFT * 0.15) for m in
                     [st, ue_stack, gnb_stack, ue_l, gnb_l] + list(funcs)],
                  run_time=0.3)

        # ── Concept 2: QoS Flow Mapping ────────────────────────────
        self.title_card(6, "QoS Flow to DRB Mapping",
                        "Quality of Service in 5G")

        qos_t = self.txt("Each PDU Session has one or more QoS flows", 24, WHITE)
        qos_t.shift(UP * 1.8)
        self.play(Write(qos_t), run_time=0.3)

        qos = RoundedRectangle(width=1.4, height=0.6, corner_radius=0.06,
                                fill_color=GREEN, fill_opacity=0.25,
                                stroke_width=1, stroke_color=GREEN)
        qos.shift(LEFT * 4 + DOWN * 0.2)
        qos_l = self.txt("QoS Flow", 16, WHITE, BOLD).move_to(qos.get_center())
        self.play(DrawBorderThenFill(VGroup(qos, qos_l)), run_time=0.3)

        drb = RoundedRectangle(width=1.4, height=0.6, corner_radius=0.06,
                                fill_color=ORANGE, fill_opacity=0.25,
                                stroke_width=1, stroke_color=ORANGE)
        drb.shift(RIGHT * 4 + DOWN * 0.2)
        drb_l = self.txt("DRB", 16, WHITE, BOLD).move_to(drb.get_center())
        self.play(DrawBorderThenFill(VGroup(drb, drb_l)), run_time=0.3)

        ma = self.arrow(qos.get_right(), drb.get_left(), GREEN)
        ma_l = self.txt("SDAP maps QoS flow \u2192 DRB", 18, GREEN).next_to(ma, UP, buff=0.03)
        self.play(Create(ma), Write(ma_l), run_time=0.4)

        qi = VGroup(
            self.txt("5QI (5G QoS Identifier): 1\u201385", 18, WHITE),
            self.txt("GBR: guaranteed bit rate (voice, video)", 18, GREY),
            self.txt("Non-GBR: best effort (web, email)", 18, GREY),
            self.txt("Delay-Critical GBR: ultra-low latency (URLLC)", 18, GREY),
        )
        qi.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        qi.shift(DOWN * 1.8 + LEFT * 1.5)
        for e in qi:
            self.play(Write(e), run_time=0.25)
        self.wait(0.8)

        self.play(*[FadeOut(m, shift=RIGHT * 0.15) for m in
                     [qos_t, qos, qos_l, drb, drb_l, ma, ma_l] + list(qi)],
                  run_time=0.3)

        # ── Concept 3: GTP Tunneling ──────────────────────────────
        self.title_card(6, "GTP-U Tunneling & IP Assignment",
                        "N3 / N9 interface encapsulation")

        gtp_t = self.txt("GPRS Tunneling Protocol (GTP-U)", 26, WHITE)
        gtp_t.shift(UP * 1.8)
        self.play(Write(gtp_t), run_time=0.3)

        gtp_eq = self.txt("GTP-U Header:  TEID (32 bit)  +  SeqNo  +  N-PDU", 28, ORANGE)
        gtp_eq.shift(UP * 0.3)
        self.play(Write(gtp_eq), run_time=0.5)

        teid_d = VGroup(
            self.txt("TEID = Tunnel Endpoint Identifier", 20, WHITE),
            self.txt("Uniquely identifies a tunnel on N3 (gNB\u2192UPF) or N9 (UPF\u2192UPF)", 20, GREY),
            self.txt("Allows multiple PDU sessions over a single transport bearer", 20, GREY),
        )
        teid_d.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        teid_d.next_to(gtp_eq, DOWN, buff=0.3)
        for e in teid_d:
            self.play(Write(e), run_time=0.25)
        self.wait(0.3)

        ip_box = RoundedRectangle(width=3.5, height=0.7, corner_radius=0.06,
                                   fill_color="#1a3e1a", fill_opacity=0.6,
                                   stroke_width=1, stroke_color=GREEN)
        ip_box.shift(DOWN * 1.3)
        ip_l = self.txt("UE IP: 10.10.0.x/32  (allocated by SMF/UPF)", 20, GREEN, BOLD)
        ip_l.move_to(ip_box.get_center())
        self.play(DrawBorderThenFill(VGroup(ip_box, ip_l)), run_time=0.4)

        ip_d = self.txt("PDU Session type:  IPv4  |  IPv6  |  IPv4v6  |  Ethernet  |  Unstructured", 20, GREY)
        ip_d.shift(DOWN * 2.3)
        self.play(Write(ip_d), run_time=0.4)
        self.wait(0.8)

        self.play(*[FadeOut(m, shift=DOWN * 0.15) for m in
                     [gtp_t, gtp_eq, ip_box, ip_l, ip_d] + list(teid_d)],
                  run_time=0.3)

    # ==================================================================
    # PHASE 7: SUMMARY
    # ==================================================================
    def phase_7_summary(self):
        self.title_card(7, "End-to-End Recap",
                        "6 phases of 5G initial setup")

        phases = [
            "1. Cell Search  \u2014  PSS/SSS, Zadoff-Chu correlation",
            "2. System Info  \u2014  MIB (PBCH) + SIB1 (PDSCH)",
            "3. Random Access  \u2014  4-step RACH, timing advance",
            "4. RRC Setup  \u2014  SRB1, state machine (IDLE/CONNECTED/INACTIVE)",
            "5. Registration  \u2014  5G AKA, KDF key hierarchy",
            "6. PDU Session  \u2014  Protocol stack, QoS, GTP-U tunneling",
        ]
        colors = [YELLOW, PURPLE, GREEN, CYAN, ORANGE, TEAL]

        base_y = 1.8
        for i, (phase, color) in enumerate(zip(phases, colors)):
            dot = Dot(LEFT * 5 + UP * (base_y - i * 0.55), color=color, radius=0.07)
            num = self.txt(str(i + 1), 11, WHITE, BOLD).move_to(dot.get_center())
            txt = self.txt(phase, 15, WHITE)
            txt.next_to(dot, RIGHT, buff=0.2)
            self.play(FadeIn(dot), Write(num), Write(txt), run_time=0.2)

        done = self.txt("UE is now connected and ready for data!", 26, GREEN, BOLD)
        done.shift(DOWN * 2.5)
        self.play(Write(done), run_time=0.6)
        self.wait(2)

        timing = self.txt("Complete procedure: typically < 500 ms on a live 5G SA network", 18, GREY)
        timing.next_to(done, DOWN, buff=0.2)
        self.play(Write(timing), run_time=0.4)
        self.wait(1.5)

    # ==================================================================
    # MAIN
    # ==================================================================
    def construct(self):
        bg = FullScreenRectangle()
        bg.set_fill(color=BG, opacity=1)
        bg.set_stroke(width=0)
        self.add(bg)

        self.phase_1_cell_search()
        self.phase_2_system_info()
        self.phase_3_rach()
        self.phase_4_rrc_setup()
        self.phase_5_registration()
        self.phase_6_pdu_session()
        self.phase_7_summary()
