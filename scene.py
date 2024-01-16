from manim import *
import numpy as np
from bezier_scene import BezierScene
from livis import LIVis
from bezier_surface import BezierSurface
from bezier_curve import BezierCurve

class QuadraticBezier(ThreeDScene):
    def construct(self):
        #generate axis 
        axes = ThreeDAxes()

        #create BezierScene obj to handle control points
        bezier_scene = BezierScene(axes=axes, u_pts=1, v_pts=3)

        #define control points
        bezier_scene.create_control_point(np.array((-2, 0, 0)), id=0, u=0, v=0)
        bezier_scene.create_control_point(np.array((0, 2, 0)), id=1, u=0, v=1)
        bezier_scene.create_control_point(np.array((2, 0, 0)), id=2, u=0, v=2)

        #add visual control points to scene
        bezier_scene.add_control_ponts_to_scene(scene=self)

        #test
        bezier_curve = BezierCurve(bezier_scene.ACT_CONTROL_POINTS)
        lin_interp_1 = BezierCurve(bezier_scene.ACT_CONTROL_POINTS[:, :2])
        lin_interp_2 = BezierCurve(bezier_scene.ACT_CONTROL_POINTS[:, -2:])

        quad_1_vis = LIVis(p1=bezier_scene.VIS_CONTROL_POINTS[0, 0][0], p2=bezier_scene.VIS_CONTROL_POINTS[0, 1][0], axes=axes)
        quad_2_vis = LIVis(p1=bezier_scene.VIS_CONTROL_POINTS[0, 1][0], p2=bezier_scene.VIS_CONTROL_POINTS[0, 2][0], axes=axes)
        quad_3_vis = LIVis(p1=quad_1_vis.tracker, p2=quad_2_vis.tracker, axes=axes)

        self.play(Create(quad_1_vis.control_polygon),
                  Create(quad_2_vis.control_polygon))
        self.wait()
        self.play(FadeIn(quad_1_vis.tracker, quad_1_vis.t, quad_1_vis.t_compl),
                  FadeIn(quad_2_vis.tracker, quad_2_vis.t, quad_2_vis.t_compl),
                  FadeIn(quad_3_vis.tracker, quad_3_vis.t, quad_3_vis.t_compl))
        self.play(quad_1_vis.animate_shift(lin_interp_1.path),
                  quad_2_vis.animate_shift(lin_interp_2.path), 
                  quad_3_vis.animate_shift(bezier_curve.path))
        self.wait()


        