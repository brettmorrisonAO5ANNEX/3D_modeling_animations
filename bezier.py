from manim import *
import numpy as np
from livis import LIVis

U_PTS = 10
V_PTS = 10
#global set of control points shape = (U_PTS, V_PTS)
CONTROL_POINTS = np.full((U_PTS, V_PTS), None, dtype=object)

class BezierTest(ThreeDScene):
    def create_control_point(self, axes, coords, id, u, v):
        #create point
        cp_dot = Sphere(radius=0.1).move_to(axes.c2p(coords[0], coords[1], coords[2]))
        cp_label = MathTex(fr"P_{id}", font_size=32).next_to(cp_dot, DOWN, buff=0.2)
        cp = VGroup(cp_dot, cp_label)

        #add point to set of global control points
        CONTROL_POINTS[u, v] = cp

    def construct(self):
        #generate axis 
        axes = ThreeDAxes()

        #1D
        self.create_control_point(axes, np.array((-2, 0, 0)), id=0, u=0, v=0)
        self.create_control_point(axes, np.array((2, 0, 0)), id=1, u=0, v=2)
        self.create_control_point(axes, np.array((0, 2, 0)), id=2, u=0, v=1)

        for u in range(U_PTS):
            for v in range(V_PTS):
                if CONTROL_POINTS[u, v] != None:
                    self.add(CONTROL_POINTS[u, v])
        """
        #create a linear intrpolation visual for two control points
        oneD_LIVis = LIVis(p1=CONTROL_POINTS[0, 0][0], p2=CONTROL_POINTS[0, 2][0], axes=axes)
        
        self.play(Create(oneD_LIVis.control_polygon))

        #only show all the tracker labels and associated values for 1D and maybe 2D to prevent clutter (for now)
        tracker_label = MathTex(r"t_0", font_size=32).next_to(oneD_LIVis.tracker, UP, buff=0.2)
        tracker_label.add_updater(lambda d: d.next_to(oneD_LIVis.tracker, UP, buff=0.2))

        t_var_0_label = MathTex(r"t_0 =", font_size=32, color=RED)
        t_var_0_val = DecimalNumber(0, num_decimal_places=2, color=RED).next_to(t_var_0_label, RIGHT, buff=0.2)
        t_var_0_val.add_updater(lambda d: d.set_value(
            (
                float(axes.p2c(oneD_LIVis.tracker.get_center())[0]) - 
                float(axes.p2c(oneD_LIVis.p1.get_center())[0])
            ) / (
                float(axes.p2c(oneD_LIVis.p2.get_center())[0]) - 
                float(axes.p2c(oneD_LIVis.p1.get_center())[0])
            )
        ))

        t_var_0 = VGroup(t_var_0_label, t_var_0_val)
        t_var_0.center()
        t_var_0.shift(DOWN)

        t_var_0_compl_label = MathTex(r"1 - t_0 =", font_size=32, color=GREEN)
        t_var_0_val_compl = DecimalNumber(0, num_decimal_places=2, color=GREEN).next_to(t_var_0_compl_label, RIGHT, buff=0.2)
        t_var_0_val_compl.add_updater(lambda d: d.set_value(
            1 - (
                float(axes.p2c(oneD_LIVis.tracker.get_center())[0]) - 
                float(axes.p2c(oneD_LIVis.p1.get_center())[0])
            ) / (
                float(axes.p2c(oneD_LIVis.p2.get_center())[0]) - 
                float(axes.p2c(oneD_LIVis.p1.get_center())[0])
            )
        ))

        t_var_0_compl = VGroup(t_var_0_compl_label, t_var_0_val_compl)
        t_var_0_compl.center()
        t_var_0_compl.next_to(t_var_0, DOWN, aligned_edge=RIGHT, buff=0.2)

        self.play(FadeIn(oneD_LIVis.tracker, oneD_LIVis.t, oneD_LIVis.t_compl, tracker_label, t_var_0, t_var_0_compl))
        
        self.play(
            oneD_LIVis.animate_shift(1), 
            run_time=2,                          
        )
        self.play(
            oneD_LIVis.animate_shift(-2), 
            run_time=2,                          
        )
        self.play(
            oneD_LIVis.animate_shift(1), 
            run_time=2,                          
        )

        self.wait()

        self.play(FadeOut(oneD_LIVis.control_polygon, oneD_LIVis.tracker, oneD_LIVis.t, oneD_LIVis.t_compl),
                  FadeOut(tracker_label, t_var_0, t_var_0_compl))
        """

        quad_1_vis = LIVis(p1=CONTROL_POINTS[0, 0][0], p2=CONTROL_POINTS[0, 1][0], axes=axes)
        quad_2_vis = LIVis(p1=CONTROL_POINTS[0, 1][0], p2=CONTROL_POINTS[0, 2][0], axes=axes)
        quad_3_vis = LIVis(p1=quad_1_vis.tracker, p2=quad_2_vis.tracker, axes=axes)

        self.play(FadeIn(CONTROL_POINTS[0,1]))
        self.play(
            Create(quad_1_vis.control_polygon),
            Create(quad_2_vis.control_polygon)
        )
        self.wait()
        self.play(
            FadeIn(quad_1_vis.tracker, quad_1_vis.t, quad_1_vis.t_compl),
            FadeIn(quad_2_vis.tracker, quad_2_vis.t, quad_2_vis.t_compl),
            FadeIn(quad_3_vis.tracker, quad_3_vis.t, quad_3_vis.t_compl)
        )
        self.play(
            quad_1_vis.animate_shift(1),
            quad_2_vis.animate_shift(1),
            #quad_3_vis.animate_shift(1),
        )
        self.wait()
        self.play(
            quad_1_vis.animate_shift(-2),
            quad_2_vis.animate_shift(-2),
            #quad_3_vis.animate_shift(-2),
        )
        self.wait()
        self.play(
            quad_1_vis.animate_shift(1),
            quad_2_vis.animate_shift(1),
            #quad_3_vis.animate_shift(1),
        )
        self.wait()

        