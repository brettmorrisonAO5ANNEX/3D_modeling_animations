from manim import *
import numpy as np
from old_classes.bezier_scene import BezierScene
from old_classes.livis import LIVis
from old_classes.bezier_surface import BezierSurface
from old_classes.bezier_curve import BezierCurve

class GenericBezier(ThreeDScene):
    def construct(self):
        #1. define an axes
        #2. define a BezierScene
        #3. define control points
        #4. add control points to scene
        #5. define curves
        #6. define linear interpolation visualizers
        #7. animate as desired
        return

class QuadraticBezier(ThreeDScene):
    def construct(self):
        #1. generate axis 
        axes = ThreeDAxes()

        #2. define a BezierScene
        bezier_scene = BezierScene(axes=axes, u_pts=1, v_pts=3)

        #3. define control points
        bezier_scene.create_control_point(np.array((-2, 0, 0)), id=0, u=0, v=0)
        bezier_scene.create_control_point(np.array((0, 2, 0)), id=1, u=0, v=1)
        bezier_scene.create_control_point(np.array((2, 0, 0)), id=2, u=0, v=2)

        #4. add control points to scene
        bezier_scene.add_control_ponts_to_scene(scene=self)

        #5. define the curves (all intermediate Bezier as well as final)
        #TODO: add another class specifically for interpolations along conrol polygons
        quadratic_bezier = BezierCurve(bezier_scene.ACT_CONTROL_POINTS)
        lin_interp_1 = BezierCurve(bezier_scene.ACT_CONTROL_POINTS[:, :2])
        lin_interp_2 = BezierCurve(bezier_scene.ACT_CONTROL_POINTS[:, -2:])

        #6. define the linear interpolation visualizers
        quad_1_vis = LIVis(p1=bezier_scene.VIS_CONTROL_POINTS[0, 0][0], p2=bezier_scene.VIS_CONTROL_POINTS[0, 1][0], axes=axes)
        quad_2_vis = LIVis(p1=bezier_scene.VIS_CONTROL_POINTS[0, 1][0], p2=bezier_scene.VIS_CONTROL_POINTS[0, 2][0], axes=axes)
        quad_3_vis = LIVis(p1=quad_1_vis.tracker, p2=quad_2_vis.tracker, axes=axes)

        #7. animate as desired
        self.play(Create(quad_1_vis.control_polygon),
                  Create(quad_2_vis.control_polygon))
        self.wait()
        self.play(FadeIn(quad_1_vis.tracker, quad_1_vis.t, quad_1_vis.t_compl),
                  FadeIn(quad_2_vis.tracker, quad_2_vis.t, quad_2_vis.t_compl),
                  FadeIn(quad_3_vis.tracker, quad_3_vis.t, quad_3_vis.t_compl))
        self.play(quad_1_vis.animate_shift(lin_interp_1.path),
                  quad_2_vis.animate_shift(lin_interp_2.path), 
                  quad_3_vis.animate_shift(quadratic_bezier.path))
        self.wait()

class CubicBezier(ThreeDScene):
    def construct(self):
        #1. define an axes
        axes = ThreeDAxes()

        #2. define a BezierScene
        bezier_scene = BezierScene(axes=axes, u_pts=1, v_pts=4)

        #3. define control points
        bezier_scene.create_control_point(np.array((-3, 0, 0)), id=0, u=0, v=0)
        bezier_scene.create_control_point(np.array((-2, 2, 0)), id=1, u=0, v=1)
        bezier_scene.create_control_point(np.array((2, 2, 0)), id=2, u=0, v=2)
        bezier_scene.create_control_point(np.array((3, 0, 0)), id=3, u=0, v=3)

        #4. add control points to scene
        bezier_scene.add_control_ponts_to_scene(scene=self)

        #5. define curves
        control_polygon_1 = BezierCurve(bezier_scene.ACT_CONTROL_POINTS[:, :2])
        control_polygon_2 = BezierCurve(bezier_scene.ACT_CONTROL_POINTS[:, 1:3])
        congrol_polygon_3 = BezierCurve(bezier_scene.ACT_CONTROL_POINTS[:, -2:])
        quadratic_bezier_1 = BezierCurve(bezier_scene.ACT_CONTROL_POINTS[:, :3])
        quadratic_bezier_2 = BezierCurve(bezier_scene.ACT_CONTROL_POINTS[:, 1:4])
        cubic_bezier = BezierCurve(bezier_scene.ACT_CONTROL_POINTS)

        #6. define linear interpolation visualizers
        cp_1_livis = LIVis(p1=bezier_scene.VIS_CONTROL_POINTS[0, 0][0], p2=bezier_scene.VIS_CONTROL_POINTS[0, 1][0], axes=axes)
        cp_2_livis = LIVis(p1=bezier_scene.VIS_CONTROL_POINTS[0, 1][0], p2=bezier_scene.VIS_CONTROL_POINTS[0, 2][0], axes=axes)
        cp_3_livis = LIVis(p1=bezier_scene.VIS_CONTROL_POINTS[0, 2][0], p2=bezier_scene.VIS_CONTROL_POINTS[0, 3][0], axes=axes)
        rec_livis_1 = LIVis(p1=cp_1_livis.tracker, p2=cp_2_livis.tracker, axes=axes)
        rec_livis_2 = LIVis(p1=cp_2_livis.tracker, p2=cp_3_livis.tracker, axes=axes)
        final_livis = LIVis(p1=rec_livis_1.tracker, p2=rec_livis_2.tracker, axes=axes)

        #7. animate as desired
        self.play(Create(cp_1_livis.control_polygon),
                  Create(cp_2_livis.control_polygon), 
                  Create(cp_3_livis.control_polygon))
        self.wait()
        self.add(quadratic_bezier_1.path,
                 quadratic_bezier_2.path,
                 cubic_bezier.path)
        self.wait()
        
        #TODO: add helper to LIVis for fading in a livis object
        self.play(FadeIn(cp_1_livis.tracker, cp_1_livis.t, cp_1_livis.t_compl),
                  FadeIn(cp_2_livis.tracker, cp_2_livis.t, cp_2_livis.t_compl),
                  FadeIn(cp_3_livis.tracker, cp_3_livis.t, cp_3_livis.t_compl),
                  FadeIn(rec_livis_1.tracker, rec_livis_1.t, rec_livis_1.t_compl),
                  FadeIn(rec_livis_2.tracker, rec_livis_2.t, rec_livis_2.t_compl),
                  FadeIn(final_livis.tracker, final_livis.t, final_livis.t_compl))
        self.play(cp_1_livis.animate_shift(control_polygon_1.path),
                  cp_2_livis.animate_shift(control_polygon_2.path),
                  cp_3_livis.animate_shift(congrol_polygon_3.path),
                  rec_livis_1.animate_shift(quadratic_bezier_1.path),
                  rec_livis_2.animate_shift(quadratic_bezier_2.path),
                  final_livis.animate_shift(cubic_bezier.path))
        self.wait()
        



        