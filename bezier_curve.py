from manim import *
import numpy as np
import math

class BezierCurve():
    """
    represents the basis funciton for a 2D Bezier curve with degree = n
    """
    def basis_func(self, i, n, t):
        polynomial_fact = math.factorial(n) / (math.factorial(i) * (math.factorial(n - i)))
        
        return polynomial_fact * (t**i) * (1 - t)**(n - i)
    
    """
    helper to calculate sum component
    """
    def bezier_sum_updater(self, i, t, axes_comp):
        return self.basis_func(i, self.n, t) * axes_comp
    
    """
    create a parametric representation of the bezier curve from
    the given control points
    """
    def create_parametric_eq(self, control_points):
        def parametric_curve(t):
            bezier_x = 0.0
            bezier_y = 0.0
            for i in range(self.n + 1):
                bezier_x += self.bezier_sum_updater(i, t, control_points[0, i][0])
                bezier_y += self.bezier_sum_updater(i, t, control_points[0, i][1])
            
            return np.array([bezier_x, bezier_y, 0])

        return parametric_curve
    
    """
    create a path object that represents the path 
    for a point to follow along the Bezier
    """
    def create_path(self):
        return ParametricFunction(self.parametric_eq,
                                  t_range=(0, 1), 
                                  color=WHITE)

    def __init__(self, control_points):
        self.n = control_points.shape[1] - 1
        self.parametric_eq = self.create_parametric_eq(control_points)
        self.path = self.create_path()