from manim import *

"""
a class to represent a general bezier scene that will have
conrol points
"""

class BezierScene():
    """
    axes: the axes being used by the calling scene
    u_pts: the number of points in the u direction (rows)
    v_pts: the number of points in the v direction (cols)
    """
    def __init__(self, axes, u_pts, v_pts):
         self.axes = axes
         self.U_PTS = u_pts
         self.V_PTS = v_pts
         self.VIS_CONTROL_POINTS = np.full((self.U_PTS, self.V_PTS), None, dtype=object)
         self.ACT_CONTROL_POINTS = np.full((self.U_PTS, self.V_PTS), None, dtype=object)

    def create_control_point(self, coords, id, u, v):
            cp_dot = Sphere(radius=0.1).move_to(self.axes.c2p(coords[0], coords[1], coords[2]))
            cp_label = MathTex(fr"P_{id}", font_size=32).next_to(cp_dot, DOWN, buff=0.2)
            cp = VGroup(cp_dot, cp_label)

            #strictly visual control points
            self.VIS_CONTROL_POINTS[u, v] = cp

            #strictly mathematical control points: just coords
            self.ACT_CONTROL_POINTS[u, v] = self.axes.c2p(coords[0], coords[1], coords[2])

    def add_control_ponts_to_scene(self, scene):
        for u in range(self.U_PTS):
            for v in range(self.V_PTS):
                if self.VIS_CONTROL_POINTS[u, v] is not None:
                    scene.add(self.VIS_CONTROL_POINTS[u, v])