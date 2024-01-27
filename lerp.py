from manim import *

"""
a class to abstract away the creation of linear interpolation (lerp) visualizations
"""
class Lerp():
    """
    creates physical start and endpoints -> may need a method to 
    add all relevant components automatically to shorten code 
    in main scene.py
    """
    #def create_points(self, p0, p1):
        #self.start = Sphere(self.axes.p2c(p0), radius=0.1, color=RED)
        #self.end = Sphere(self.axes.p2c(p1), radius=0.1, color=RED)

    """
    creates the control polygon between two given points ->
    can be created for any lerp, but is really only relavant 
    if the start and end points are true control points and 
    not trackers (in the case of recursive lerps)
    """
    def create_control_polygon(self, control_color):
        return always_redraw(lambda: DashedLine(self.start.get_center(), 
                                                self.end.get_center(), 
                                                color=control_color, buff=0.05))

    """
    creates a tracker that will follow along the lerp path based on 
    the value of t_label
    """
    def create_tracker(self):
        return always_redraw(lambda: Sphere([a*(1-self.t_label.value.get_value())+b*self.t_label.value.get_value() 
                                             for a, b in zip(self.start.get_center(), self.end.get_center())], radius=0.05))
    
    """
    creates the colored lines between the tracker and endpoints
    """
    def create_tracker_lines(self):
        self.tracker_line_1 = always_redraw(lambda: Line(self.start.get_center(), self.tracker.get_center(), color=GREEN))
        self.tracker_line_2 = always_redraw(lambda: Line(self.tracker.get_center(), self.end.get_center(), color=RED))

    """
    a method to create the control polygon as well as the
    tracker and its associate line segments
    """
    def create_vis_comps(self, control_color):
        self.control_polygon = self.create_control_polygon(control_color)
        self.tracker = self.create_tracker()
        self.create_tracker_lines()

    """
    p0: lerp start point
    p1: lerp end point
    """
    def __init__(self, axes, p0, p1, t_label, control_color=WHITE):
        self.axes = axes
        #self.create_points(p0, p1)
        self.start = p0
        self.end = p1
        self.t_label = t_label
        self.create_vis_comps(control_color)

    """
    a method to quickly add all default components to the scene
    """
    def add_lerp_to_scene(self, scene):
        scene.add(self.tracker, self.control_polygon)