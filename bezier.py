from manim import *
import numpy as np

U_PTS = 10
V_PTS = 10
#global set of control points shape = (U_PTS, V_PTS)
CONTROL_POINTS = np.full((U_PTS, V_PTS), None, dtype=object)

#aassumes p1 to the left of p2 from normal perspective
class LIVis():
    def create_control_polygon(self):
        return DashedLine(self.p1.get_center(), 
                          self.p2.get_center(),
                          stroke_opacity=0.2, color=WHITE, buff=0.05)
    
    def create_tracker(self):
        p1_center = self.axes.p2c(self.p1.get_center())
        p2_center = self.axes.p2c(self.p2.get_center())
        #calculate coordinates for center
        x = np.minimum(p1_center[0], p2_center[0]) + np.abs((p2_center[0] - p1_center[0]) / 2)
        y = np.minimum(p1_center[1], p2_center[1]) + np.abs((p2_center[1] - p1_center[1]) / 2)
        z = np.minimum(p1_center[2], p2_center[2]) + np.abs((p2_center[2] - p1_center[2]) / 2)

        return Sphere(radius=0.05, color=RED).move_to(self.axes.c2p(x, y, z))
    
    #sets the start coords of tracker line to be on the outside edge of the sphere
    #oriented properly towards the end point
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
    
    def create_tracker_line(self, start, end, color):
        #get correction factor for updater to place line at correct position
        CORRECTION_1 = self.fetch_correction(start, end)
        CORRECTION_2 = self.fetch_correction(end, start)

        tracker_line = Line(start.get_center() + CORRECTION_1, 
                            end.get_center() + CORRECTION_2, color=color, buff=0.05)
        
        tracker_line.add_updater(lambda d: d.put_start_and_end_on(
            start.get_center() + CORRECTION_1,
            end.get_center() + CORRECTION_2))
        
        return tracker_line
    
    def create_vis_components(self):
        self.control_polygon = self.create_control_polygon()
        self.tracker = self.create_tracker()
        self.t = self.create_tracker_line(self.p1, self.tracker, RED)
        self.t_compl = self.create_tracker_line(self.tracker, self.p2, GREEN)

    def create_direction_vector(self):
        start_adjusted = self.tracker.get_center()
        end_adjusted = self.p2.get_center()

        d_vec = np.array([[end_adjusted[0] - start_adjusted[0]],
                          [end_adjusted[1] - start_adjusted[1]],
                          [end_adjusted[2] - start_adjusted[2]]])
        
        #max span is the max length we can scale the unit vec by (to reach the end point)
        self.span = np.linalg.norm(d_vec) 

        return d_vec / self.span

    def __init__(self, p1, p2, axes):
        self.p1 = p1
        self.p2 = p2
        self.axes = axes
        self.create_vis_components()
        self.d_unit_vec = self.create_direction_vector()

    # -span <= scale_factor <= span
    #used to animate the progression of the tracker along the control polygon
    def animate_shift(self, scale_factor):
        return self.tracker.animate.shift(scale_factor*self.span * (self.d_unit_vec[0]*RIGHT +
                                                                    self.d_unit_vec[1]*UP +
                                                                    self.d_unit_vec[2]*OUT))

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
        self.create_control_point(axes, np.array((-2, 0, 0)), id=0, u=0, v=0)
        self.create_control_point(axes, np.array((2, 0, 0)), id=1, u=0, v=2)

        for u in range(U_PTS):
            for v in range(V_PTS):
                if CONTROL_POINTS[u, v] != None:
                    self.add(CONTROL_POINTS[u, v])

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

        """  
        self.play(FadeOut(oneD_LIVis.tracker, oneD_LIVis.t, oneD_LIVis.t_compl, tracker_label, t_var_0, t_var_0_compl))

        self.create_control_point(axes, np.array((0, 2, 0)), id=2, u=0, v=1)

        quad_1_vis = LIVis(p1=CONTROL_POINTS[0, 0][0], p2=CONTROL_POINTS[0, 1][0], axes=axes)
        quad_2_vis = LIVis(p1=CONTROL_POINTS[0, 1][0], p2=CONTROL_POINTS[0, 2][0], axes=axes)
        quad_3_vis = LIVis(p1=quad_1_vis.tracker, p2=quad_2_vis.tracker, axes=axes)

        self.play(FadeIn(CONTROL_POINTS[0,1]))
        self.play(
            FadeIn(quad_1_vis.tracker, quad_1_vis.t, quad_1_vis.t_compl),
            FadeIn(quad_2_vis.tracker, quad_2_vis.t, quad_2_vis.t_compl),
            FadeIn(quad_3_vis.tracker, quad_3_vis.t, quad_3_vis.t_compl)
        )

        self.wait()
        """