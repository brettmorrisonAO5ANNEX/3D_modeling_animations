from manim import *
from lerp import Lerp

class LinearBezier(ThreeDScene):
    def construct(self):
        #create axes
        axes = ThreeDAxes()

        #setup t label
        t = 0.0
        t_label = Variable(t, Text("t"), num_decimal_places=2)
        t_label.shift(DOWN + LEFT)
        t_tracker = t_label.tracker

        #create control points
        """
        note: create an array of control points where:
              -> control_points[u,v] = physical sphere at coords of cp
        """
        CP_0 = Sphere(axes.p2c((-2, 0, 0)), radius=0.1)
        CP_1 = Sphere(axes.p2c((-2.5, 2, 0)), radius=0.1)
        CP_2 = Sphere(axes.p2c((2.5, 2, 0)), radius=0.1)
        CP_3 = Sphere(axes.p2c((2, 0, 0)), radius=0.1)

        #add control points
        self.add(CP_0, CP_1, CP_2, CP_3)

        #creat lerp element
        lerp_0 = Lerp(axes=axes, p0=CP_0, p1=CP_1, t_label=t_label)
        lerp_1 = Lerp(axes=axes, p0=CP_1, p1=CP_2, t_label=t_label)
        lerp_2 = Lerp(axes=axes, p0=CP_2, p1=CP_3, t_label=t_label)
        rec_lerp0 = Lerp(axes=axes, p0=lerp_0.tracker, p1=lerp_1.tracker, t_label=t_label)
        rec_lerp1 = Lerp(axes=axes, p0=lerp_1.tracker, p1=lerp_2.tracker, t_label=t_label)
        final_lerp = Lerp(axes=axes, p0=rec_lerp0.tracker, p1=rec_lerp1.tracker, t_label=t_label)

        #visualize the final Bezier curve
        bezier = TracedPath(final_lerp.tracker.get_center, stroke_width=4, stroke_color=YELLOW)
        self.add(bezier)
        self.add(t_label)

        #add lerp components
        lerp_0.add_lerp_to_scene(scene=self)
        lerp_1.add_lerp_to_scene(scene=self)
        lerp_2.add_lerp_to_scene(scene=self)
        rec_lerp0.add_lerp_to_scene(scene=self)
        rec_lerp1.add_lerp_to_scene(scene=self)
        final_lerp.add_lerp_to_scene(scene=self)

        #shift t
        self.play(t_tracker.animate.set_value(1), run_time=5)
        self.wait()
        #self.play(t_tracker.animate.set_value(0))
        #self.wait()
        #self.play(t_tracker.animate.set_value(0.5))
        #self.wait()