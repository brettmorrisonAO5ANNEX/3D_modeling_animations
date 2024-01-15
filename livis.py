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

        return Sphere(radius=0.05, color=RED).move_to(self.axes.c2p(x, y, z))
    
    def create_tracker_line(self, start, end, color):
        tracker_line = Line(start.get_center(), end.get_center(), color=color)
        tracker_line.add_updater(lambda d: d.become(Line(start.get_center(), end.get_center(), color=color)))
        
        return tracker_line
    
    def create_vis_components(self):
        self.control_polygon = self.create_control_polygon()
        self.tracker = self.create_tracker()
        self.t = self.create_tracker_line(self.p1, self.tracker, RED)
        self.t_compl = self.create_tracker_line(self.tracker, self.p2, GREEN)

    """
    def create_direction_vector(self):
        start_center = self.axes.p2c(self.tracker.get_center())
        end_center = self.axes.p2c(self.p2.get_center())

        d_vec = np.array([[end_center[0] - start_center[0]],
                          [end_center[1] - start_center[1]],
                          [end_center[2] - start_center[2]]])
        
        span = np.linalg.norm(d_vec) 

        self.d_unit_vec =  d_vec / span
    
    def fetch_length(self):
        #vector from p1 -> p2 accounting for buffer to prevent point overlap
        p1_center = self.axes.p2c(self.p1.get_center())
        p2_center = self.axes.p2c(self.p2.get_center())
        span_vec = np.array([[p2_center[0] - p1_center[0]],
                             [p2_center[1] - p1_center[1]],
                             [p2_center[2] - p1_center[2]]])
        span_dist = np.linalg.norm(span_vec)

        self.length = span_dist - 0.002
    """
    
    """
    as the points move, update the direction unit vec and length
    which are used to position the tracker along the control
    polygon
    """
    """"
    def add_special_updaters(self):
        self.p1.add_updater(lambda d: self.create_direction_vector())
        self.p1.add_updater(lambda d: self.fetch_length())
    """
    """
    is_recursive_interpolation: set to true if the livis is for a recursive interpolation,
                                will result in adding an updater to length and direction vector
    """
    def __init__(self, p1, p2, axes):
        self.p1 = p1
        self.p2 = p2
        self.axes = axes
        self.create_vis_components()
        #self.create_direction_vector()
        #self.fetch_length()

        #add length and direction vector updaters
        #if is_recursive_interpolation:
        #    self.add_special_updaters()

    """
    sets the tracker to the proper location based on a global t value and
    length/direction vector between endpoints
    """
    """
    def animate_shift(self, t):
        #since t=0 starts the tracker at p1, we'll get the position to go to from p1
        p1_center = self.axes.p2c(self.p1.get_center())

        #t is a ratio of the points distance from p1 and the length
        t_dist = t*self.length
        offset_vec = t_dist*self.d_unit_vec

        new_loc = p1_center + (offset_vec[0]*RIGHT + offset_vec[1]*UP + offset_vec[2]*OUT)

        return self.tracker.animate.move_to(new_loc)
    """
    def animate_shift(self, bezier_curve):
        return MoveAlongPath(self.tracker, bezier_curve, rate_func=linear)