from manim import *
import numpy as np
import math

class BezierSurface():
    """
    represents the basis funciton for a 2D Bezier curve with degree = n
    """
    def basis_func(self, i, n, t):
        polynomial_fact = math.factorial(n) / (math.factorial(i) * (math.factorial(n - i)))
        
        return polynomial_fact * t**i * (1 - t)**(n - i)
    
    """
    helper to calculate sum component
    """
    def bezier_sum_updater(self, i, j, u, v, axes_comp):
        return self.basis_func(i, self.n, u) * self.basis_func(j, self.m, v) * axes_comp
    
    """
    create a parametric representation of the bezier curve from
    the given control points
    """
    def create_parametric_eq(self, control_points):
        def parametric_curve(u, v):
            bezier_x = 0.0
            bezier_y = 0.0
            bezier_z = 0.0
            for i in range(self.n + 1):
                for j in range(self.m + 1):
                    bezier_x += self.bezier_sum_updater(i, j, u, v, control_points[i, j][0])
                    bezier_y += self.bezier_sum_updater(i, j, u, v, control_points[i, j][1])
                    bezier_z += self.bezier_sum_updater(i, j, u, v, control_points[i, j][2])
            
            return np.array([bezier_x, bezier_y, bezier_z])

        return parametric_curve
    
    """
    create a path object that represents the path 
    for a point to follow along the Bezier
    """
    def create_surface(self):
        return Surface(lambda u, v: self.parametric_eq(u, v),
                       u_range=(0, 1), 
                       v_range=(0, 1), 
                       color=WHITE)

    def __init__(self, control_points):
        self.n = control_points.shape[0] - 1
        self.m = control_points.shape[1] - 1
        self.parametric_eq = self.create_parametric_eq(control_points)
        self.surface = self.create_surface()

