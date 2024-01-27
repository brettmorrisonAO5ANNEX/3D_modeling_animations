from manim import *
import numpy as np

#aassumes p1 to the left of p2 from normal perspective
class LIVis():
    """
    connects the two control points with a dashed line to represent the control polygon
    """
    def create_control_polygon(self):
        return DashedLine(self.p1.get_center(), 
                          self.p2.get_center(),
                          stroke_opacity=0.2, color=WHITE, buff=0.05)
    
    """
    creates a tracker sphere for the t_i value for visualizing the linear interpolaton b/w 
    control points
    """
    def create_tracker(self):
        p1_center = self.axes.p2c(self.p1.get_center())
        p2_center = self.axes.p2c(self.p2.get_center())
        #calculate coordinates for center
        x = np.minimum(p1_center[0], p2_center[0]) + np.abs((p2_center[0] - p1_center[0]) / 2)
        y = np.minimum(p1_center[1], p2_center[1]) + np.abs((p2_center[1] - p1_center[1]) / 2)
        z = np.minimum(p1_center[2], p2_center[2]) + np.abs((p2_center[2] - p1_center[2]) / 2)

        #return Sphere(radius=0.05, color=RED).move_to(self.axes.c2p(x, y, z))
        return Sphere(radius=0.05, color=RED).move_to(self.p1.get_center())
    
    def create_tracker_line(self, start, end, color):
        tracker_line = Line(start.get_center(), end.get_center(), color=color)
        tracker_line.add_updater(lambda d: d.become(Line(start.get_center(), end.get_center(), color=color)))
        
        return tracker_line
    
    def create_vis_components(self):
        self.control_polygon = self.create_control_polygon()
        self.tracker = self.create_tracker()
        self.t = self.create_tracker_line(self.p1, self.tracker, RED)
        self.t_compl = self.create_tracker_line(self.tracker, self.p2, GREEN)

    def __init__(self, p1, p2, axes):
        self.p1 = p1
        self.p2 = p2
        self.axes = axes
        self.create_vis_components()

    def animate_shift(self, bezier_curve):
        return MoveAlongPath(self.tracker, bezier_curve, rate_func=linear, run_time=3)