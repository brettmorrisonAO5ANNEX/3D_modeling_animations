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
    
    """
    start: the 'origin' of the tracker line
    end: the 'destination' of the tracker line

    uses the orientation vector between start, end to determine how to adjust
    """
    """
    def fetch_correction(self, start, end):
        start_center = self.axes.p2c(start.get_center())
        end_center = self.axes.p2c(end.get_center())

        #define direction vector between start and end
        d_vec = np.array([[end_center[0] - start_center[0]],
                          [end_center[1] - start_center[1]],
                          [end_center[2] - start_center[2]]])
        
        #normalize d_vec
        mag = np.linalg.norm(d_vec)

        d_vec_norm = d_vec / mag
        
        #adjust d_vec_norm to length = radius of start point
        rad = start.radius
        d_vec_rad_norm = d_vec_norm * rad

        #fetch coords of d_vec_rad_norm AKA the correction factors in the x, y, z directions
        correction_x = d_vec_rad_norm[0]
        correction_y = d_vec_rad_norm[1]
        correction_z = d_vec_rad_norm[2]
        
        return correction_x*RIGHT + correction_y*UP + correction_z*OUT
    """
    
    def create_tracker_line(self, start, end, color):
        tracker_line = Line(start.get_center(), end.get_center(), color=color)
        tracker_line.add_updater(lambda d: d.put_start_and_end_on(start.get_center(), end.get_center()))
        
        return tracker_line
    
    def create_vis_components(self):
        self.control_polygon = self.create_control_polygon()
        self.tracker = self.create_tracker()
        self.t = self.create_tracker_line(self.p1, self.tracker, RED)
        self.t_compl = self.create_tracker_line(self.tracker, self.p2, GREEN)

    def create_direction_vector(self):
        start_center = self.tracker.get_center()
        end_center = self.p2.get_center()

        d_vec = np.array([[end_center[0] - start_center[0]],
                          [end_center[1] - start_center[1]],
                          [end_center[2] - start_center[2]]])
        
        span = np.linalg.norm(d_vec) 

        #max_span is slightly shorter than span to prevent point overlap
        self.max_span = span - 0.001

        return d_vec / span

    def __init__(self, p1, p2, axes):
        self.p1 = p1
        self.p2 = p2
        self.axes = axes
        self.create_vis_components()
        self.d_unit_vec = self.create_direction_vector()

    # -span <= scale_factor <= span
    #used to animate the progression of the tracker along the control polygon
    def animate_shift(self, scale_factor):
        return self.tracker.animate.shift(scale_factor*self.max_span * (self.d_unit_vec[0]*RIGHT +
                                                                        self.d_unit_vec[1]*UP +
                                                                        self.d_unit_vec[2]*OUT))