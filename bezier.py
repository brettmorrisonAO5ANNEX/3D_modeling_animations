from manim import *
import numpy as np

U_PTS = 10
V_PTS = 10
#global set of control points shape = (U_PTS, V_PTS)
CONTROL_POINTS = np.full((U_PTS, V_PTS), None, dtype=object)

class Bezier(ThreeDScene):
    def create_control_point(self, axes, coords, id, u, v):
        #create point
        cp_dot = Sphere(radius=0.1, stroke_opacity=0).move_to(axes.c2p(coords[0], coords[1], coords[2]))
        cp_label = MathTex(fr"P_{id}", font_size=32).next_to(cp_dot, DOWN, buff=0.2)
        cp = VGroup(cp_dot, cp_label)

        #add point to set of global control points
        CONTROL_POINTS[u, v] = cp

    def construct(self):
        #generate axis 
        axes = ThreeDAxes()

        #1D
        self.create_control_point(axes, np.array((-2, 0, 0)), 0, 0, 0)
        self.create_control_point(axes, np.array((2, 0, 0)), 1, 0, 1)

        for u in range(U_PTS):
            for v in range(V_PTS):
                if CONTROL_POINTS[u, v] != None:
                    self.add(CONTROL_POINTS[u, v])

        control_polygon_1D = DashedLine(CONTROL_POINTS[0, 0][0].get_edge_center(RIGHT), 
                                  CONTROL_POINTS[0, 1][0].get_edge_center(LEFT),
                                  stroke_opacity=0.2,
                                  color=WHITE)
        
        self.play(Create(control_polygon_1D))

        t_var_0_tracker = Sphere(radius=0.05, color=RED).move_to(axes.c2p(0, 0, 0))
        tracker_label = MathTex(r"t_0", font_size=32).next_to(t_var_0_tracker, UP, buff=0.2)
        tracker_label.add_updater(lambda d: d.next_to(t_var_0_tracker, UP, buff=0.2))

        t_var_0_label = MathTex(r"t_0 =", font_size=32, color=RED)
        t_var_0_val = DecimalNumber(0, num_decimal_places=2, color=RED).next_to(t_var_0_label, RIGHT, buff=0.2)
        t_var_0_val.add_updater(lambda d: d.set_value(
            (
                float(axes.p2c(t_var_0_tracker.get_center())[0]) - 
                float(axes.p2c(CONTROL_POINTS[0, 0].get_center())[0])
            ) / (
                float(axes.p2c(CONTROL_POINTS[0, 1].get_center())[0]) - 
                float(axes.p2c(CONTROL_POINTS[0, 0].get_center())[0])
            )
        ))

        t_var_0 = VGroup(t_var_0_label, t_var_0_val)
        t_var_0.center()
        t_var_0.shift(DOWN)

        t_var_0_compl_label = MathTex(r"1 - t_0 =", font_size=32, color=GREEN)
        t_var_0_val_compl = DecimalNumber(0, num_decimal_places=2, color=GREEN).next_to(t_var_0_compl_label, RIGHT, buff=0.2)
        t_var_0_val_compl.add_updater(lambda d: d.set_value(
            1 - (
                float(axes.p2c(t_var_0_tracker.get_center())[0]) - 
                float(axes.p2c(CONTROL_POINTS[0, 0].get_center())[0])
            ) / (
                float(axes.p2c(CONTROL_POINTS[0, 1].get_center())[0]) - 
                float(axes.p2c(CONTROL_POINTS[0, 0].get_center())[0])
            )
        ))

        t_var_0_compl = VGroup(t_var_0_compl_label, t_var_0_val_compl)
        t_var_0_compl.center()
        t_var_0_compl.next_to(t_var_0, DOWN, aligned_edge=RIGHT, buff=0.2)

        t_0_line = Line(CONTROL_POINTS[0,0][0].get_edge_center(RIGHT), 
                        t_var_0_tracker.get_edge_center(LEFT), color=RED)
        t_0_line.add_updater(lambda d: d.put_start_and_end_on(
            CONTROL_POINTS[0,0][0].get_edge_center(RIGHT),
            t_var_0_tracker.get_edge_center(LEFT)))
        
        t_0_compl_line = Line(t_var_0_tracker.get_edge_center(RIGHT), 
                              CONTROL_POINTS[0,1][0].get_edge_center(LEFT), color=GREEN)
        t_0_compl_line.add_updater(lambda d: d.put_start_and_end_on(
            t_var_0_tracker.get_edge_center(RIGHT),
            CONTROL_POINTS[0,1][0].get_edge_center(LEFT)))

        self.play(FadeIn(t_var_0_tracker, tracker_label, t_var_0, t_var_0_compl, t_0_line, t_0_compl_line))
        self.play(
            t_var_0_tracker.animate.move_to(axes.c2p(1.5, 0, 0)), 
            run_time=2,                          
        )
        self.play(
            t_var_0_tracker.animate.move_to(axes.c2p(-1.5, 0, 0)), 
            run_time=2,                          
        )
        self.play(
            t_var_0_tracker.animate.move_to(axes.c2p(0, 0, 0)), 
            run_time=2,                          
        )

        self.wait()
        