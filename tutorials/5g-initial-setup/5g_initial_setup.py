from manim import *
import numpy as np

# ─── Palette ───────────────────────────────────────────────────────
BG      = "#0b0b18"
WHITE   = "#eceff4"
GREY    = "#4c566a"
CYAN    = "#88c0d0"
RED     = "#bf616a"
ORANGE  = "#d08770"
GREEN   = "#a3be8c"
PURPLE  = "#b48ead"
YELLOW  = "#ebcb8b"
TEAL    = "#8fbcbb"
WARM    = "#d35f5f"
DIM     = "#2e3440"

# Phase accent colors
P_COLORS = [YELLOW, PURPLE, GREEN, CYAN, ORANGE, TEAL, "#88c0d0"]

config.background_color = BG
config.frame_rate = 30


class FiveGInitialSetup(Scene):
    def txt(self, text, fs=24, color=WHITE, weight=NORMAL, **kw):
        return Text(text, font_size=fs, color=color, weight=weight,
                    font="Helvetica Neue", **kw)

    def box(self, text, color="#1a1a2e", w=1.8, h=0.7, fs=17):
        r = RoundedRectangle(width=w, height=h, corner_radius=0.06,
                             fill_color=color, fill_opacity=0.8,
                             stroke_width=0.5, stroke_color=GREY)
        l = self.txt(text, fs, WHITE).move_to(r.get_center())
        return VGroup(r, l)

    def arr(self, start, end, color=CYAN, sw=2):
        return Arrow(start, end, color=color, stroke_width=sw, buff=0.1,
                     max_tip_length_to_length_ratio=0.1)

    # ─── Transition helper ────────────────────────────────────────
    def replace(self, old, new, direction=DOWN, rt=0.5):
        """Fade old out in direction, add new, fade new in from opposite."""
        ops = []
        if old is not None:
            ops += [FadeOut(old, shift=direction * 0.3)]
        if new is not None:
            new.shift(-direction * 0.3)
            ops += [FadeIn(new, shift=direction * 0.3)]
        self.play(*ops, run_time=rt)

    def slide(self, old_mobs, new, direction=LEFT, rt=0.55):
        """Fade list of old mobs out, new in, with directional shift."""
        anims = [FadeOut(m, shift=direction * 0.4) for m in old_mobs]
        if new is not None:
            new.shift(-direction * 0.4)
            anims.append(FadeIn(new, shift=direction * 0.4))
        self.play(*anims, run_time=rt)

    # ─── Phase title ──────────────────────────────────────────────
    def phase_card(self, num, title, accent, icon=""):
        self.clear()
        bg = FullScreenRectangle()
        bg.set_fill(color=BG, opacity=1)
        bg.set_stroke(width=0)
        self.add(bg)

        n = self.txt(str(num), 48, accent, BOLD).to_corner(UL, buff=0.35)
        t = self.txt(title, 34, WHITE, BOLD).next_to(n, RIGHT, buff=0.3).shift(UP * 0.05)
        ln = Line(t.get_left(), t.get_right(), color=accent, stroke_width=2.5).next_to(t, DOWN, buff=0.08)
        return VGroup(n, t, ln)

    # ═══════════════════════════════════════════════════════════════
    # PHASE 1 — 4 concepts
    # ═══════════════════════════════════════════════════════════════
    def phase_1_cell_search(self):
        accent = P_COLORS[0]
        prev = self.phase_card(1, "Cell Search & Synchronization", accent)
        self.add(prev)
        self.wait(0.2)

        # ── 1a: Tower → UE signal ─────────────────────────────────
        tower_pole = Rectangle(width=0.10, height=2.0, fill_color="#3a3a5a", fill_opacity=1, stroke_width=0)
        tower_base = Rectangle(width=0.6, height=0.10, fill_color="#3a3a5a", fill_opacity=1, stroke_width=0)
        tower_ant = Polygon(LEFT * 0.2, RIGHT * 0.2, UP * 0.4, stroke_width=0, fill_color=RED, fill_opacity=0.9)
        tower = VGroup(tower_pole, tower_base, tower_ant)
        tower.arrange(DOWN, buff=0)
        tower.shift(RIGHT * 3.5 + UP * 0.3)
        gnb_l = self.txt("gNB", 16, RED).next_to(tower_ant, UP, buff=0.08)
        tower_group = VGroup(tower, gnb_l)
        tower_group.shift(UP * 0.5)
        self.play(DrawBorderThenFill(tower), Write(gnb_l), run_time=0.5)

        ue_b = RoundedRectangle(width=0.9, height=0.6, corner_radius=0.08, fill_color="#14325e", fill_opacity=1, stroke_width=0)
        ue_l = self.txt("UE", 16, WHITE).move_to(ue_b.get_center())
        ue = VGroup(ue_b, ue_l)
        ue.shift(LEFT * 3.5 + UP * 0.8)
        self.play(DrawBorderThenFill(ue), run_time=0.4)

        # Animated wave from tower → UE
        wave_line = Line(tower_ant.get_top() + UP * 0.15, ue.get_right() + RIGHT * 0.3, color=accent, stroke_width=2, stroke_opacity=0)
        dot = Dot(tower_ant.get_top() + UP * 0.15, color=accent, radius=0.05)
        wave_label = self.txt("SS/PBCH (PSS + SSS)", 16, CYAN)
        wave_label.next_to(wave_line, UP, buff=0.15)
        self.play(Write(wave_label), run_time=0.3)

        # Animate dot traveling from gNB to UE with trailing sine wave
        sine_wave = VGroup()
        for step in range(30):
            t = step / 30
            pos = interpolate(tower_ant.get_top() + UP * 0.15, ue.get_right() + RIGHT * 0.3, t)
            if step > 5:
                # Build trailing wave
                trail = ParametricFunction(
                    lambda s, tt=t: np.array([
                        interpolate(tower_ant.get_top()[0] + 0.1, pos[0], s),
                        interpolate(tower_ant.get_top()[1], pos[1], s) + 0.15 * np.sin(tt * 8 * PI - s * 6 * PI),
                        0,
                    ]),
                    t_range=[0, 1],
                    color=accent, stroke_width=2, stroke_opacity=0.7,
                )
                self.play(
                    dot.animate.move_to(pos),
                    run_time=0.04,
                )
                if step % 3 == 0:
                    self.add(trail)
            else:
                self.play(dot.animate.move_to(pos), run_time=0.04)

        self.play(FadeOut(dot), run_time=0.15)
        self.wait(0.3)

        scanning = self.txt("UE correlates received signal against known PSS sequences", 17, WHITE)
        scanning.shift(DOWN * 2)
        self.play(Write(scanning), run_time=0.35)
        self.wait(0.4)

        # ── Smooth slide to 1b: PSS Equation ──────────────────────
        new_h = self.phase_card(1, "Primary Synchronization Signal (PSS)", accent)
        self.slide([prev, tower_group, ue, wave_label, scanning], new_h, LEFT, 0.5)
        prev = new_h

        pss_title = self.txt("Zadoff-Chu sequence for cell ID detection", 20, accent)
        pss_title.shift(UP * 2)
        self.play(Write(pss_title), run_time=0.3)

        eq = self.txt("a_u(n) = exp( -j\u03C0 u n (n+1) / N_ZC )", 34, YELLOW)
        eq.shift(UP * 0.8)
        self.play(Write(eq), run_time=0.5)

        details = VGroup(
            self.txt("N_ZC = 127   |   0 \u2264 n < N_ZC", 22, CYAN),
            self.txt("Root indices: u \u2208 {25, 29, 34}  (3 sequences)", 20, WHITE),
            self.txt("UE picks the strongest correlation peak \u2192 N_ID\u00B2 = {0, 1, 2}", 20, accent),
        )
        details.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        details.next_to(eq, DOWN, buff=0.35)
        for d in details:
            self.play(Write(d), run_time=0.3)
            self.wait(0.15)

        self.wait(0.3)

        # ── Slide to 1c: SSS ──────────────────────────────────────
        new_h = self.phase_card(1, "Secondary Synchronization Signal (SSS)", accent)
        self.slide([prev, pss_title, eq, *details], new_h, LEFT, 0.5)
        prev = new_h

        sss_t = self.txt("Gold-code m-sequences for cell group ID", 20, accent)
        sss_t.shift(UP * 2)
        self.play(Write(sss_t), run_time=0.3)

        sss_eq = self.txt("d_SSS(n) = [1 - 2x\u2080(n)] \u00D7 [1 - 2x\u2081(n)]", 30, PURPLE)
        sss_eq.shift(UP * 0.5)
        self.play(Write(sss_eq), run_time=0.5)

        sss_note = self.txt("x\u2080, x\u2081: length-127 m-sequences with distinct polynomial shifts", 20, GREY)
        sss_note.next_to(sss_eq, DOWN, buff=0.25)
        self.play(Write(sss_note), run_time=0.35)

        cell_id = self.txt("N_ID_cell = 3 \u00D7 N_ID\u00B9 + N_ID\u00B2", 34, accent)
        cell_id.shift(DOWN * 0.5)
        cell_d = self.txt("N_ID\u00B9 = {0..335} (336 SSS sequences)  \u2192  3 \u00D7 336 = 1008 unique PCIs", 18, WHITE)
        cell_d.next_to(cell_id, DOWN, buff=0.2)
        self.play(Write(cell_id), Write(cell_d), run_time=0.5)

        # Show PCI breakdown visually
        pci_viz = VGroup(
            self.txt("PSS: 3 possibilities  \u00D7  SSS: 336 possibilities  =  1008 Cell IDs", 18, accent),
        )
        pci_viz.next_to(cell_d, DOWN, buff=0.3)
        self.play(Write(pci_viz), run_time=0.3)
        self.wait(0.4)

        # ── Slide to 1d: Correlation ──────────────────────────────
        new_h = self.phase_card(1, "Correlation Peak Detection", accent)
        self.slide([prev, sss_t, sss_eq, sss_note, cell_id, cell_d, pci_viz], new_h, LEFT, 0.5)
        prev = new_h

        axes = Axes(
            x_range=[-3, 3, 1], y_range=[0, 1.2, 0.2],
            x_length=8, y_length=3,
            axis_config={"color": DIM},
        ).shift(DOWN * 0.1)
        xl = self.txt("Subcarrier offset (frequency domain)", 14, GREY).next_to(axes, DOWN, buff=0.1)
        yl = self.txt("Correlation", 14, GREY).next_to(axes, LEFT, buff=0.3).rotate(PI / 2)
        self.play(Create(axes), Write(xl), Write(yl), run_time=0.5)

        xs = np.linspace(-3, 3, 140)
        ys = 0.3 + 0.7 * np.exp(-(xs ** 2) / 0.35) + 0.015 * np.random.randn(140)
        bars = VGroup(*[
            Line(axes.c2p(x, 0), axes.c2p(x, max(0.01, y)), color=accent, stroke_width=3)
            for x, y in zip(xs, ys)
        ])
        self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.004), run_time=1.2)

        # Flash the peak
        peak_pt = axes.c2p(0, 0.98)
        flash = Flash(peak_pt, color=accent, line_length=0.3, flash_radius=0.2, time_width=0.5)
        self.play(flash)
        peak_l = self.txt("Peak detected  \u2192  Cell ID + timing acquired", 18, accent)
        peak_l.next_to(axes, UP, buff=0.25)
        self.play(Write(peak_l), run_time=0.4)
        self.wait(0.5)

        self.play(FadeOut(peak_l), FadeOut(axes), FadeOut(xl), FadeOut(yl), FadeOut(bars),
                  FadeOut(prev), run_time=0.35)

    # ═══════════════════════════════════════════════════════════════
    # PHASE 2 — 3 concepts
    # ═══════════════════════════════════════════════════════════════
    def phase_2_system_info(self):
        accent = P_COLORS[1]
        prev = self.phase_card(2, "System Information Acquisition", accent)
        self.add(prev)
        self.wait(0.2)

        # ── 2a: Resource Grid ─────────────────────────────────────
        grid_t = self.txt("NR Time-Frequency Resource Grid", 20, WHITE)
        grid_t.shift(UP * 2.2)
        self.play(Write(grid_t), run_time=0.25)

        rows, cols = 12, 14
        cs = 0.15
        gap = 0.012
        ox = -cols * (cs + gap) / 2 - 1
        oy = rows * (cs + gap) / 2 + 0.5
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
                sq = Square(side_length=cs, fill_color=color, fill_opacity=0.9, stroke_width=0.15, stroke_color="#2a2a4e")
                sq.move_to([x, y, 0])
                grid.add(sq)
                cm[(r, c)] = sq
        grid.shift(DOWN * 0.3)
        self.play(LaggedStart(*[FadeIn(s, scale=0.2) for s in grid], lag_ratio=0.003), run_time=1)

        fa = Arrow(UP * 0.15, UP * 0.4, color=GREY, stroke_width=2).next_to(grid, LEFT, buff=0.1)
        fl = self.txt("Freq", 10, GREY).next_to(fa, LEFT, buff=0.03)
        ta = Arrow(LEFT * 0.15, RIGHT * 0.15, color=GREY, stroke_width=2).next_to(grid, DOWN, buff=0.05)
        tl = self.txt("Time (symbols)", 10, GREY).next_to(ta, DOWN, buff=0.02)
        self.play(Create(fa), Write(fl), Create(ta), Write(tl), run_time=0.25)

        # Highlight PBCH
        pbch = VGroup(*[cm[(r, c)] for r in range(2, 10) for c in range(4, 8)])
        for sq in pbch:
            sq.set_fill("#3a2a5a", opacity=0.9)
        self.play(*[sq.animate.set_stroke(accent, width=0.5) for sq in pbch], run_time=0.3)
        pbch_l = self.txt("PBCH (MIB)", 15, accent).next_to(grid, UP, buff=0.3).align_to(grid, LEFT)
        self.play(Write(pbch_l), run_time=0.25)

        # Highlight SIB1
        sib1 = VGroup(*[cm[(r, c)] for r in range(2, 10) for c in range(8, 12)])
        for sq in sib1:
            sq.set_fill("#2a1a4a", opacity=0.9)
        self.play(*[sq.animate.set_stroke(CYAN, width=0.5) for sq in sib1], run_time=0.3)
        sib1_l = self.txt("PDSCH (SIB1)", 15, CYAN).next_to(pbch_l, RIGHT, buff=0.5)
        self.play(Write(sib1_l), run_time=0.25)

        note = self.txt("SSB occupies symbols 4\u201311 of slot 0 in every half-frame (20 ms period)", 17, GREY)
        note.next_to(grid, DOWN, buff=0.3)
        self.play(Write(note), run_time=0.3)
        self.wait(0.4)

        self.play(FadeOut(grid_t), FadeOut(grid), FadeOut(fa), FadeOut(fl),
                  FadeOut(ta), FadeOut(tl), FadeOut(pbch_l), FadeOut(sib1_l),
                  FadeOut(note), FadeOut(prev), run_time=0.3)

        # ── 2b: MIB Fields (just add directly onto clean) ──────────
        prev = self.phase_card(2, "Master Information Block (MIB)", accent)
        self.add(prev)
        self.wait(0.15)

        mib_t = self.txt("23 bits of cell-access parameters on PBCH", 20, WHITE)
        mib_t.shift(UP * 2)
        self.play(Write(mib_t), run_time=0.25)

        fields = [
            ("systemFrameNumber", "6 bits", "Upper bits of the 10-bit SFN"),
            ("subCarrierSpacingCommon", "1 bit", "15 kHz (0) or 30 kHz (1) for SIB1/RAR/MSG4"),
            ("ssb-SubcarrierOffset", "4 bits", "SSB \u00D7 15 kHz offset from common RB 0"),
            ("dmrs-TypeA-Position", "1 bit", "DMRS symbol position in slot (2 or 3)"),
            ("pdcch-ConfigSIB1", "8 bits", "CORESET #0 + search space for SIB1 scheduling"),
            ("reserved", "3 bits", "Spare bits"),
        ]
        fg = VGroup()
        for i, (name, bits, desc) in enumerate(fields):
            y = 1.3 - i * 0.45
            nr = RoundedRectangle(width=2.2, height=0.3, corner_radius=0.04, fill_color=accent, fill_opacity=0.15, stroke_width=0.5, stroke_color=accent)
            nr.shift(UP * y + LEFT * 0.5)
            nl = self.txt(name, 12, WHITE).move_to(nr.get_center()).shift(LEFT * 0.2)
            br = RoundedRectangle(width=0.5, height=0.3, corner_radius=0.04, fill_color=accent, fill_opacity=0.3, stroke_width=0.5, stroke_color=accent)
            br.next_to(nr, RIGHT, buff=0.02)
            bl = self.txt(bits, 9, accent, BOLD).move_to(br.get_center())
            dl = self.txt(desc, 11, GREY)
            dl.next_to(nr, RIGHT, buff=0.65).align_to(nr, UP)
            g = VGroup(nr, nl, br, bl, dl)
            fg.add(g)
            self.play(FadeIn(g, shift=LEFT * 0.1), run_time=0.18)
        self.wait(0.4)

        self.play(*[FadeOut(m, shift=RIGHT * 0.15) for m in [prev, mib_t] + list(fg)], run_time=0.3)

        # ── 2c: SIB1 ──────────────────────────────────────────────
        prev = self.phase_card(2, "System Information Block 1 (SIB1)", accent)
        self.add(prev)
        self.wait(0.15)

        sib_t = self.txt("SIB1 carries essential cell access parameters", 20, WHITE)
        sib_t.shift(UP * 2)
        self.play(Write(sib_t), run_time=0.25)

        items = [
            "PLMN identity (MCC + MNC)",
            "Tracking Area Code (TAC)",
            "Cell identity (gNB ID + local cell ID)",
            "Cell barring status (barred / not barred)",
            "SI scheduling: periodicity, SI-window length",
            "SIB type mapping (which SIBs are broadcast)",
        ]
        ig = VGroup()
        for i, item in enumerate(items):
            dot = Dot(LEFT * 4 + UP * (0.9 - i * 0.38), color=accent, radius=0.04)
            it = self.txt(item, 18, WHITE).next_to(dot, RIGHT, buff=0.2)
            ig.add(VGroup(dot, it))
            self.play(FadeIn(dot), Write(it), run_time=0.2)

        sched = self.txt("SIB1 period: 160 ms  |  SI-window: 5 ms  |  Transport: PDSCH", 18, accent)
        sched.shift(DOWN * 2.2)
        self.play(Write(sched), run_time=0.35)
        self.wait(0.5)

        self.play(*[FadeOut(m, shift=DOWN * 0.15) for m in [prev, sib_t, sched] + list(ig)], run_time=0.3)

    # ═══════════════════════════════════════════════════════════════
    # PHASE 3 — 4 concepts
    # ═══════════════════════════════════════════════════════════════
    def phase_3_rach(self):
        accent = P_COLORS[2]
        prev = self.phase_card(3, "Random Access Procedure", accent)
        self.add(prev)
        self.wait(0.2)

        # ── 3a: Preamble Math ─────────────────────────────────────
        prach_t = self.txt("PRACH Preamble: another Zadoff-Chu sequence", 20, WHITE)
        prach_t.shift(UP * 2)
        self.play(Write(prach_t), run_time=0.25)

        eq = self.txt("x_u(n) = exp( -j\u03C0 u n (n+1) / N_ZC )", 32, accent)
        eq.shift(UP * 0.8)
        self.play(Write(eq), run_time=0.4)

        det = VGroup(
            self.txt("N_ZC = 839 (FR1, sub-6 GHz)  |  N_ZC = 139 (FR2, mmWave)", 20, CYAN),
            self.txt("Cyclic shift C_v generates multiple preambles from one root", 18, WHITE),
            self.txt("64 preambles per cell: combine multiple roots + cyclic shifts", 18, accent),
        )
        det.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        det.next_to(eq, DOWN, buff=0.25)
        for d in det:
            self.play(Write(d), run_time=0.3)
        self.wait(0.4)

        self.play(*[FadeOut(m, shift=LEFT * 0.15) for m in [prev, prach_t, eq] + list(det)], run_time=0.3)

        # ── 3b: Preamble Waveform ─────────────────────────────────
        prev = self.phase_card(3, "Preamble in the Time Domain", accent)
        self.add(prev)
        self.wait(0.15)

        ax = Axes(x_range=[0, 10, 1], y_range=[-1.6, 1.6, 0.5], x_length=7, y_length=2.5, axis_config={"color": DIM})
        ax.shift(DOWN * 0.1)
        self.play(Create(ax), run_time=0.35)

        cp_l = self.txt("Cyclic Prefix", 15, GREEN).next_to(ax, LEFT, buff=0.15).shift(DOWN * 0.7)
        seq_l = self.txt("Preamble Sequence", 15, accent).next_to(ax, RIGHT, buff=0.1).shift(DOWN * 0.7)
        self.play(Write(cp_l), Write(seq_l), run_time=0.25)

        t_vals = np.linspace(0, 10, 300)
        wf = VGroup()
        for i, t in enumerate(t_vals[:-1]):
            a1 = 1.0 if t < 2 else (0.5 + 0.5 * np.sin(3 * (t - 2) * PI)) * np.exp(-0.08 * (t - 2))
            a2 = 1.0 if t_vals[i + 1] < 2 else (0.5 + 0.5 * np.sin(3 * (t_vals[i + 1] - 2) * PI)) * np.exp(-0.08 * (t_vals[i + 1] - 2))
            wf.add(Line(ax.c2p(t, a1), ax.c2p(t_vals[i + 1], a2), color=accent, stroke_width=2))
        self.play(Create(wf), run_time=1.2)

        cp_hl = Rectangle(width=ax.c2p(2, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, 1.5)[1] - ax.c2p(0, -1.5)[1], fill_color=GREEN, fill_opacity=0.06, stroke_width=0).move_to(ax.c2p(1, 0))
        self.add(cp_hl)
        self.wait(0.4)

        self.play(*[FadeOut(m, shift=DOWN * 0.15) for m in [prev, ax, cp_l, seq_l, wf, cp_hl]], run_time=0.3)

        # ── 3c: Timing Advance ────────────────────────────────────
        prev = self.phase_card(3, "Timing Advance (TA)", accent)
        self.add(prev)
        self.wait(0.15)

        ta_t = self.txt("Compensating for the round-trip propagation delay", 20, WHITE)
        ta_t.shift(UP * 1.8)
        self.play(Write(ta_t), run_time=0.25)

        # Visual: two arrows showing propagation
        ue_dot = Dot(LEFT * 4.5 + DOWN * 0.2, color=WHITE, radius=0.08)
        gnb_dot = Dot(RIGHT * 4.5 + DOWN * 0.2, color=RED, radius=0.08)
        ue_lab = self.txt("UE", 14, WHITE).next_to(ue_dot, DOWN, buff=0.1)
        gnb_lab = self.txt("gNB", 14, RED).next_to(gnb_dot, DOWN, buff=0.1)
        self.play(FadeIn(ue_dot), FadeIn(gnb_dot), Write(ue_lab), Write(gnb_lab), run_time=0.3)

        a_fwd = Arrow(ue_dot.get_center(), gnb_dot.get_center(), color=accent, stroke_width=2, buff=0.15)
        a_bwd = Arrow(gnb_dot.get_center(), ue_dot.get_center(), color=GREEN, stroke_width=2, buff=0.15)
        a_bwd.shift(DOWN * 0.3)
        a_fwd_lab = self.txt("Uplink (preamble)", 14, accent).next_to(a_fwd, UP, buff=0.05)
        a_bwd_lab = self.txt("RAR (TA value)", 14, GREEN).next_to(a_bwd, DOWN, buff=0.05)
        self.play(Create(a_fwd), Write(a_fwd_lab), run_time=0.3)
        self.wait(0.15)
        self.play(Create(a_bwd), Write(a_bwd_lab), run_time=0.3)
        self.wait(0.2)

        self.play(FadeOut(ue_dot), FadeOut(gnb_dot), FadeOut(ue_lab), FadeOut(gnb_lab),
                  FadeOut(a_fwd), FadeOut(a_bwd), FadeOut(a_fwd_lab), FadeOut(a_bwd_lab), run_time=0.2)

        eq1 = self.txt("N_TA = (T_Rx - T_Tx) / 2", 32, GREEN)
        eq1.shift(UP * 0.3)
        self.play(Write(eq1), run_time=0.4)
        eq1_d = self.txt("T_Rx = reception time at gNB,  T_Tx = transmission time at UE", 17, GREY)
        eq1_d.next_to(eq1, DOWN, buff=0.15)
        self.play(Write(eq1_d), run_time=0.25)
        self.wait(0.2)

        eq2 = self.txt("T_TA = (N_TA + N_TA_offset) \u00D7 T_c", 30, CYAN)
        eq2.shift(DOWN * 0.8)
        eq2_d = self.txt("T_c = 0.509 ns (basic NR time unit),  N_TA_offset depends on duplex mode", 17, GREY)
        eq2_d.next_to(eq2, DOWN, buff=0.15)
        self.play(Write(eq2), Write(eq2_d), run_time=0.45)
        self.wait(0.3)

        summary = VGroup(
            self.txt("\u2022 gNB measures delay from preamble arrival", 18, WHITE),
            self.txt("\u2022 Sends TA value in Random Access Response (MSG2)", 18, WHITE),
            self.txt("\u2022 UE advances its UL timing so gNB receives within CP window", 18, accent),
        )
        summary.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        summary.shift(DOWN * 1.8 + LEFT * 0.3)
        for s in summary:
            self.play(Write(s), run_time=0.25)
        self.wait(0.5)

        self.play(*[FadeOut(m, shift=RIGHT * 0.15) for m in [prev, ta_t, eq1, eq1_d, eq2, eq2_d] + list(summary)], run_time=0.3)

        # ── 3d: 4-Step Handshake ──────────────────────────────────
        prev = self.phase_card(3, "4-Step Random Access Handshake", accent)
        self.add(prev)
        self.wait(0.15)

        ue = self.box("UE", "#14325e", w=1.5, h=0.6, fs=16).shift(LEFT * 4.5)
        gnb = self.box("gNB", "#16213e", w=1.5, h=0.6, fs=16).shift(RIGHT * 4.5)
        self.play(DrawBorderThenFill(ue), DrawBorderThenFill(gnb), run_time=0.4)

        msgs = [
            ("MSG1: PRACH Preamble", accent, ue, gnb),
            ("MSG2: RAR (TA + UL Grant)", GREEN, gnb, ue),
            ("MSG3: RRC Setup Request", accent, ue, gnb),
            ("MSG4: Contention Resolution", GREEN, gnb, ue),
        ]
        yo = 0.7
        for text, color, sender, receiver in msgs:
            lbl = self.txt(text, 15, color, BOLD)
            lbl.next_to(sender, UP, buff=yo)
            self.play(Write(lbl), run_time=0.18)
            a = self.arr(sender.get_center(), receiver.get_center(), color)
            a.shift(UP * (yo - 0.08))
            self.play(Create(a), run_time=0.22)
            self.wait(0.2)
            yo += 0.45

        note = self.txt("Contention resolved  \u2192  UE uniquely identified on the cell", 18, GREEN)
        note.shift(DOWN * 2.5)
        self.play(Write(note), run_time=0.35)
        self.wait(0.6)

        self.play(FadeOut(ue), FadeOut(gnb), FadeOut(prev), FadeOut(note), run_time=0.3)

    # ═══════════════════════════════════════════════════════════════
    # PHASE 4 — 2 concepts
    # ═══════════════════════════════════════════════════════════════
    def phase_4_rrc_setup(self):
        accent = P_COLORS[3]
        prev = self.phase_card(4, "RRC Connection Setup", accent)
        self.add(prev)
        self.wait(0.2)

        # ── 4a: State Machine ─────────────────────────────────────
        st = self.txt("5G RRC States and Transitions", 22, WHITE)
        st.shift(UP * 2)
        self.play(Write(st), run_time=0.25)

        idle = self.box("RRC_IDLE", "#2a2a4e", w=1.7, h=0.65, fs=16).shift(LEFT * 4.5)
        conn = self.box("RRC_CONNECTED", "#1e4a1e", w=1.7, h=0.65, fs=16).shift(RIGHT * 4.5)
        inact = self.box("RRC_INACTIVE", "#4a2a4a", w=1.7, h=0.65, fs=16).shift(DOWN * 1.5)

        self.play(DrawBorderThenFill(idle), DrawBorderThenFill(conn), run_time=0.35)

        a1 = self.arr(idle.get_right(), conn.get_left(), accent)
        a1l = self.txt("RRCSetup", 12, accent, BOLD).next_to(a1, UP, buff=0.03)
        self.play(Create(a1), Write(a1l), run_time=0.3)
        a2 = Arrow(conn.get_left(), idle.get_right(), color=ORANGE, stroke_width=2, buff=0.08, path_arc=-0.35)
        a2l = self.txt("RRCRelease", 12, ORANGE, BOLD).next_to(a2, DOWN, buff=0.03)
        self.play(Create(a2), Write(a2l), run_time=0.3)

        self.play(DrawBorderThenFill(inact), run_time=0.2)
        a3 = self.arr(conn.get_bottom(), inact.get_top(), PURPLE)
        a3l = self.txt("RRCInactive", 11, PURPLE).next_to(a3, RIGHT, buff=0.03)
        a4 = self.arr(inact.get_top(), conn.get_bottom(), GREEN)
        a4l = self.txt("RRCResume", 11, GREEN).next_to(a4, LEFT, buff=0.03)
        self.play(Create(a3), Write(a3l), Create(a4), Write(a4l), run_time=0.4)

        # Animate state dot moving between states
        dot = Dot(idle.get_center(), color=accent, radius=0.08)
        self.play(FadeIn(dot), run_time=0.15)
        self.play(dot.animate.move_to(conn.get_center()), run_time=0.6)
        self.wait(0.15)
        self.play(dot.animate.move_to(inact.get_center()), run_time=0.5)
        self.wait(0.15)
        self.play(dot.animate.move_to(conn.get_center()), run_time=0.5)
        self.wait(0.2)

        descs = VGroup(
            self.txt("RRC_IDLE: no connection, DRX paging, small-data RACH", 14, GREY),
            self.txt("RRC_CONNECTED: full RRC context, active data transfer", 14, GREY),
            self.txt("RRC_INACTIVE: 5G-specific, retained context, fast resume", 14, GREY),
        )
        descs.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        descs.shift(DOWN * 2.8 + LEFT * 1.5)
        for d in descs:
            self.play(Write(d), run_time=0.2)
        self.wait(0.4)

        self.play(*[FadeOut(m, shift=DOWN * 0.12) for m in
                     [prev, st, idle, conn, inact, a1, a2, a3, a4,
                      a1l, a2l, a3l, a4l, dot] + list(descs)], run_time=0.3)

        # ── 4b: SRB1 Flow ─────────────────────────────────────────
        prev = self.phase_card(4, "Signaling Radio Bearer (SRB1)", accent)
        self.add(prev)
        self.wait(0.15)

        srb_t = self.txt("SRB1 carries all RRC + NAS signaling", 20, WHITE)
        srb_t.shift(UP * 2)
        self.play(Write(srb_t), run_time=0.25)

        ue = self.box("UE", "#14325e", w=1.5, h=0.6, fs=16).shift(LEFT * 4)
        gnb = self.box("gNB", "#16213e", w=1.5, h=0.6, fs=16).shift(RIGHT * 4)
        self.play(DrawBorderThenFill(ue), DrawBorderThenFill(gnb), run_time=0.35)

        for text, color, sender, receiver in [
            ("RRCSetupRequest", accent, ue, gnb),
            ("RRCSetup (SRB1 config)", CYAN, gnb, ue),
            ("RRCSetupComplete + NAS Reg.", accent, ue, gnb),
        ]:
            lbl = self.txt(text, 14, color, BOLD)
            lbl.next_to(sender, UP, buff=0.7)
            self.play(Write(lbl), run_time=0.2)
            a = self.arr(sender.get_center(), receiver.get_center(), color)
            a.shift(UP * 0.6)
            self.play(Create(a), run_time=0.22)
            self.wait(0.2)

        result = self.txt("SRB1 established  \u2192  bidirectional NAS transport ready", 18, GREEN)
        result.shift(DOWN * 2.2)
        self.play(Write(result), run_time=0.35)
        self.wait(0.5)

        self.play(FadeOut(ue), FadeOut(gnb), FadeOut(prev), FadeOut(srb_t), FadeOut(result), run_time=0.3)

    # ═══════════════════════════════════════════════════════════════
    # PHASE 5 — 2 concepts
    # ═══════════════════════════════════════════════════════════════
    def phase_5_registration(self):
        accent = P_COLORS[4]
        prev = self.phase_card(5, "Registration & Authentication", accent)
        self.add(prev)
        self.wait(0.2)

        # ── 5a: Network Flow ──────────────────────────────────────
        flow_t = self.txt("Registration message flow through the 5G core", 20, WHITE)
        flow_t.shift(UP * 2.2)
        self.play(Write(flow_t), run_time=0.25)

        nd = [
            ("UE", "#14325e", LEFT * 5.5),
            ("gNB", "#16213e", LEFT * 2.5),
            ("AMF", "#1a1a3e", RIGHT * 0.5),
            ("AUSF", "#2a1a3e", RIGHT * 3.5),
        ]
        nodes = {}
        for name, color, pos in nd:
            b = self.box(name, color, w=1.2, h=0.5, fs=15)
            b.shift(pos + DOWN * 0.8)
            nodes[name] = b
            self.play(DrawBorderThenFill(b), run_time=0.2)

        steps = [
            ("Registration Request", accent, "UE", "gNB"),
            ("Registration Request", accent, "gNB", "AMF"),
            ("Auth Vector Request", ORANGE, "AMF", "AUSF"),
            ("Auth Vector Response", ORANGE, "AUSF", "AMF"),
            ("Auth Req (RAND+AUTN)", CYAN, "AMF", "gNB"),
            ("Auth Req (RAND+AUTN)", CYAN, "gNB", "UE"),
            ("Auth Response (RES)", accent, "UE", "gNB"),
            ("Auth Response (RES)", accent, "gNB", "AMF"),
            ("Security Mode Cmd", GREEN, "AMF", "gNB"),
            ("Security Mode Cmd", GREEN, "gNB", "UE"),
            ("Registration Accept", TEAL, "AMF", "gNB"),
            ("Registration Accept", TEAL, "gNB", "UE"),
        ]

        y = 0.5
        for text, color, s_name, r_name in steps:
            lbl = self.txt(text, 10, color, BOLD)
            lbl.next_to(nodes[s_name], UP, buff=y)
            self.play(Write(lbl), run_time=0.1)
            a = self.arr(nodes[s_name].get_center(), nodes[r_name].get_center(), color, sw=1.2)
            self.play(Create(a), run_time=0.1)
            y += 0.01
        self.wait(0.4)

        self.play(*[FadeOut(m, shift=DOWN * 0.1) for m in [prev, flow_t] + list(nodes.values())], run_time=0.3)

        # ── 5b: Key Hierarchy ─────────────────────────────────────
        prev = self.phase_card(5, "5G Key Hierarchy (KDF Chain)", accent)
        self.add(prev)
        self.wait(0.15)

        kh_t = self.txt("K \u2192 CK||IK \u2192 K_AUSF \u2192 K_SEAF \u2192 K_AMF \u2192 K_NAS", 20, WHITE)
        kh_t.shift(UP * 2.2)
        self.play(Write(kh_t), run_time=0.3)

        def key_box(text, color, y, w=2.8):
            r = RoundedRectangle(width=w, height=0.45, corner_radius=0.04, fill_color=color, fill_opacity=0.2, stroke_width=0.8, stroke_color=color)
            r.shift(UP * y)
            l = self.txt(text, 15, WHITE, BOLD).move_to(r.get_center())
            return VGroup(r, l)

        keys = [
            ("K  (permanent on USIM)", RED, 1.6),
            ("CK  ||  IK", PURPLE, 0.8),
            ("K_AUSF  (anchor)", CYAN, 0.0),
            ("K_SEAF  (security anchor)", TEAL, -0.8),
            ("K_AMF", ORANGE, -1.6),
            ("K_NASint  +  K_NASenc", GREEN, -2.4),
        ]

        all_k = VGroup()
        prev_box = None
        for txt, color, y in keys:
            kb = key_box(txt, color, y)
            all_k.add(kb)
            self.play(FadeIn(kb, shift=RIGHT * 0.15), run_time=0.18)
            if prev_box is not None:
                a = Arrow(prev_box.get_bottom(), kb.get_top(), color=accent, stroke_width=1.5, buff=0.04)
                l = self.txt("KDF", 11, accent).next_to(a, RIGHT, buff=0.03)
                all_k.add(a, l)
                self.play(Create(a), Write(l), run_time=0.18)
            prev_box = kb

        note = self.txt("KDF inputs: SUPI, SN-name, freshness parameter ABBA, algorithm type", 16, GREY)
        note.shift(DOWN * 3 + LEFT * 1)
        self.play(Write(note), run_time=0.35)
        self.wait(0.6)

        self.play(FadeOut(kh_t), FadeOut(all_k), FadeOut(note), FadeOut(prev), run_time=0.3)

    # ═══════════════════════════════════════════════════════════════
    # PHASE 6 — 3 concepts
    # ═══════════════════════════════════════════════════════════════
    def phase_6_pdu_session(self):
        accent = P_COLORS[5]
        prev = self.phase_card(6, "PDU Session Establishment", accent)
        self.add(prev)
        self.wait(0.2)

        # ── 6a: Protocol Stack ────────────────────────────────────
        st = self.txt("5G User Plane Protocol Stack", 22, WHITE)
        st.shift(UP * 2.2)
        self.play(Write(st), run_time=0.25)

        layers = ["SDAP", "PDCP", "RLC", "MAC", "PHY"]
        colors = [RED, PURPLE, CYAN, TEAL, ORANGE]
        ue_stack = VGroup()
        gnb_stack = VGroup()
        for i, (layer, color) in enumerate(zip(layers, colors)):
            y = 1.2 - i * 0.38
            ur = RoundedRectangle(width=0.75, height=0.26, corner_radius=0.03, fill_color=color, fill_opacity=0.25, stroke_width=0.5, stroke_color=color)
            ur.shift(LEFT * 3 + UP * y)
            ul = self.txt(layer, 11, WHITE, BOLD).move_to(ur.get_center())
            ue_stack.add(VGroup(ur, ul))
            gr = RoundedRectangle(width=0.75, height=0.26, corner_radius=0.03, fill_color=color, fill_opacity=0.25, stroke_width=0.5, stroke_color=color)
            gr.shift(RIGHT * 3 + UP * y)
            gl = self.txt(layer, 11, WHITE, BOLD).move_to(gr.get_center())
            gnb_stack.add(VGroup(gr, gl))

        self.play(
            LaggedStart(*[DrawBorderThenFill(s) for s in ue_stack], lag_ratio=0.06),
            LaggedStart(*[DrawBorderThenFill(s) for s in gnb_stack], lag_ratio=0.06),
            run_time=0.7,
        )

        ue_l = self.txt("UE", 13, accent).next_to(ue_stack, LEFT, buff=0.1)
        gnb_l = self.txt("gNB/UPF", 13, accent).next_to(gnb_stack, RIGHT, buff=0.1)
        self.play(Write(ue_l), Write(gnb_l), run_time=0.2)

        # Draw peer arrows + animate a data unit flowing
        arrows = VGroup()
        for i in range(5):
            y = 1.2 - i * 0.38
            a = self.arr(LEFT * 2.5 + UP * y, RIGHT * 2.5 + UP * y, accent)
            arrows.add(a)
            self.play(Create(a), run_time=0.08)
        self.wait(0.15)

        # Animate data unit
        pkt = RoundedRectangle(width=0.2, height=0.08, corner_radius=0.02, fill_color=accent, fill_opacity=0.9, stroke_width=0)
        pkt.shift(LEFT * 2.5 + UP * 1.2)
        self.play(pkt.animate.shift(RIGHT * 5), run_time=0.6)
        self.wait(0.1)
        pkt2 = RoundedRectangle(width=0.2, height=0.08, corner_radius=0.02, fill_color=accent, fill_opacity=0.9, stroke_width=0)
        pkt2.shift(RIGHT * 2.5 + UP * 1.2)
        self.play(pkt2.animate.shift(LEFT * 5), run_time=0.6)

        self.wait(0.2)

        funcs = VGroup(
            self.txt("SDAP: QoS flow \u2192 DRB mapping", 13, GREY),
            self.txt("PDCP: ciphering, integrity protection, header compression", 13, GREY),
            self.txt("RLC: segmentation, ARQ retransmission", 13, GREY),
            self.txt("MAC: scheduling, HARQ, logical channel prioritization", 13, GREY),
            self.txt("PHY: OFDM, channel coding, MIMO processing", 13, GREY),
        )
        funcs.arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        funcs.shift(DOWN * 1.5 + LEFT * 0.3)
        for f in funcs:
            self.play(Write(f), run_time=0.18)
        self.wait(0.4)

        self.play(*[FadeOut(m, shift=LEFT * 0.12) for m in
                     [prev, st, ue_stack, gnb_stack, ue_l, gnb_l, pkt, pkt2] + list(arrows) + list(funcs)],
                  run_time=0.3)

        # ── 6b: QoS Mapping ───────────────────────────────────────
        prev = self.phase_card(6, "QoS Flow to DRB Mapping", accent)
        self.add(prev)
        self.wait(0.15)

        qos_t = self.txt("Each PDU session can have multiple QoS flows", 20, WHITE)
        qos_t.shift(UP * 2)
        self.play(Write(qos_t), run_time=0.25)

        qos = RoundedRectangle(width=1.3, height=0.55, corner_radius=0.05, fill_color=GREEN, fill_opacity=0.2, stroke_width=0.8, stroke_color=GREEN)
        qos.shift(LEFT * 4 + DOWN * 0.2)
        qos_l = self.txt("QoS Flow", 15, WHITE, BOLD).move_to(qos.get_center())
        self.play(DrawBorderThenFill(VGroup(qos, qos_l)), run_time=0.25)

        drb = RoundedRectangle(width=1.3, height=0.55, corner_radius=0.05, fill_color=ORANGE, fill_opacity=0.2, stroke_width=0.8, stroke_color=ORANGE)
        drb.shift(RIGHT * 4 + DOWN * 0.2)
        drb_l = self.txt("DRB", 15, WHITE, BOLD).move_to(drb.get_center())
        self.play(DrawBorderThenFill(VGroup(drb, drb_l)), run_time=0.25)

        ma = self.arr(qos.get_right(), drb.get_left(), accent)
        ma_l = self.txt("SDAP mapping", 16, accent).next_to(ma, UP, buff=0.03)
        self.play(Create(ma), Write(ma_l), run_time=0.35)

        qi = VGroup(
            self.txt("5QI = 5G QoS Identifier (1\u201385)", 17, WHITE),
            self.txt("GBR: guaranteed bit rate for voice, live video", 16, GREY),
            self.txt("Non-GBR: best effort for web, email, messaging", 16, GREY),
            self.txt("Delay-Critical GBR: URLLC (< 1 ms latency)", 16, GREY),
        )
        qi.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        qi.shift(DOWN * 1.7 + LEFT * 1.3)
        for e in qi:
            self.play(Write(e), run_time=0.22)
        self.wait(0.5)

        self.play(*[FadeOut(m, shift=RIGHT * 0.12) for m in
                     [prev, qos_t, qos, qos_l, drb, drb_l, ma, ma_l] + list(qi)],
                  run_time=0.3)

        # ── 6c: GTP Tunneling ─────────────────────────────────────
        prev = self.phase_card(6, "GTP-U Tunneling", accent)
        self.add(prev)
        self.wait(0.15)

        gtp_t = self.txt("GPRS Tunneling Protocol (GTP-U) on N3/N9", 22, WHITE)
        gtp_t.shift(UP * 1.8)
        self.play(Write(gtp_t), run_time=0.25)

        gtp_eq = self.txt("GTP-U Header:  TEID (32-bit)  +  SeqNo  +  N-PDU  +  Extension", 26, ORANGE)
        gtp_eq.shift(UP * 0.5)
        self.play(Write(gtp_eq), run_time=0.4)

        gtp_d = VGroup(
            self.txt("TEID uniquely identifies a tunnel endpoint", 18, WHITE),
            self.txt("Maps to PDU session + QoS flow on N3 (gNB\u2192UPF) or N9 (UPF\u2192UPF)", 17, GREY),
            self.txt("Multiple PDU sessions multiplexed over a single transport bearer", 17, GREY),
        )
        gtp_d.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        gtp_d.next_to(gtp_eq, DOWN, buff=0.25)
        for d in gtp_d:
            self.play(Write(d), run_time=0.22)
        self.wait(0.3)

        ip_b = RoundedRectangle(width=3.2, height=0.6, corner_radius=0.05, fill_color="#1a3e1a", fill_opacity=0.5, stroke_width=0.8, stroke_color=GREEN)
        ip_b.shift(DOWN * 1.3)
        ip_l = self.txt("UE IP: 10.10.0.x/32  (SMF/UPF allocates)", 18, GREEN, BOLD).move_to(ip_b.get_center())
        self.play(DrawBorderThenFill(VGroup(ip_b, ip_l)), run_time=0.35)

        ip_d = self.txt("Session types: IPv4 / IPv6 / IPv4v6 / Ethernet / Unstructured", 17, GREY)
        ip_d.shift(DOWN * 2.3)
        self.play(Write(ip_d), run_time=0.3)
        self.wait(0.5)

        self.play(*[FadeOut(m, shift=DOWN * 0.12) for m in
                     [prev, gtp_t, gtp_eq, ip_b, ip_l, ip_d] + list(gtp_d)],
                  run_time=0.3)

    # ═══════════════════════════════════════════════════════════════
    # PHASE 7: SUMMARY
    # ═══════════════════════════════════════════════════════════════
    def phase_7_summary(self):
        accent = P_COLORS[6]
        prev = self.phase_card(7, "End-to-End Recap", accent)
        self.add(prev)
        self.wait(0.2)

        phases = [
            "1. Cell Search  \u2014  PSS/SSS, Zadoff-Chu, correlation",
            "2. System Info  \u2014  MIB (PBCH) + SIB1 (PDSCH)",
            "3. Random Access  \u2014  4-step RACH, timing advance",
            "4. RRC Setup  \u2014  SRB1, IDLE/CONNECTED/INACTIVE",
            "5. Registration  \u2014  5G AKA, KDF key hierarchy",
            "6. PDU Session  \u2014  Stack, QoS, GTP-U tunneling",
        ]
        colors = [YELLOW, PURPLE, GREEN, CYAN, ORANGE, TEAL]

        base_y = 1.8
        g = VGroup()
        for i, (phase, color) in enumerate(zip(phases, colors)):
            dot = Dot(LEFT * 5 + UP * (base_y - i * 0.55), color=color, radius=0.06)
            num = self.txt(str(i + 1), 10, WHITE, BOLD).move_to(dot.get_center())
            txt = self.txt(phase, 14, WHITE)
            txt.next_to(dot, RIGHT, buff=0.2)
            row = VGroup(dot, num, txt)
            g.add(row)
            self.play(FadeIn(dot), Write(num), Write(txt), run_time=0.18)

        done = self.txt("UE is now connected and ready for data!", 24, GREEN, BOLD)
        done.shift(DOWN * 2.3)
        self.play(Write(done), run_time=0.5)

        timing = self.txt("Entire procedure typically completes in < 500 ms on a live 5G SA network", 16, GREY)
        timing.next_to(done, DOWN, buff=0.15)
        self.play(Write(timing), run_time=0.35)
        self.wait(2)

    # ═══════════════════════════════════════════════════════════════
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
