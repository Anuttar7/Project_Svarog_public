import numpy as np
import json

"""
TRAC boom and spool geometry calculator.

This file defines the BoomGeometry class, which reads the boom and spool
geometry inputs from JSON data and calculates the boom's cross-sectional
properties and its packaged/coiled dimensions.

The class uses the supplied geometry to calculate:
- Cross-sectional area of the curved flange and bonded web.
- The boom centroid coordinates (x and y).
- Second moments of area about the centroidal x- and y-axes.
- Saint-Venant torsional constant.
- Flattened boom height.
- Number of turns required to coil the boom around the spool.

The export_boom() method writes the calculated boom geometry and section
properties into the "geometry" and "section_properties" sections of the
specified boom JSON file. The export_spool() method updates the spool JSON
file with the calculated number of coils and the resulting outer coiled
radius.

At the end of the script, the boom and spool JSON files are loaded, a
BoomGeometry object is created, and both JSON files are updated.

Input files:
- boom_properties.json: boom dimensions and existing boom properties.
- spool_properties.json: spool hub radius and existing spool properties.

The calculations assume the cross-section is symmetric about the y-axis,
so the x-coordinate of the centroid is zero. The section-property equations
are implemented directly in the methods below; their derivation is not
included in this file.
"""


class BoomGeometry:
    def __init__(self, boom_data, spool_data):
        """
        Extracting relevant data from the properties files (JSON).
        """

        self.w = boom_data["geometry"]["BONDED_WEB_LENGTH"]
        self.r1 = boom_data["geometry"]["FLANGE_INNER_RADIUS"]
        self.r2 = boom_data["geometry"]["FLANGE_OUTER_RADIUS"]
        self.t = boom_data["geometry"]["FLANGE_THICKNESS"]
        self.theta = np.radians(boom_data["geometry"]["FLANGE_SUBTENDED_ANGLE_DEG"])  # Convert angle to radians
        self.L = boom_data["geometry"]["BOOM_LENGTH"]
        self.r = (self.r1 + self.r2) / 2
        self.R = spool_data["geometry"]["HUB_RADIUS"]
        

    def section_area (self):
        """
        Calculates the cross-sectional area of the boom.
        """

        # Calculate the area of the flange
        A_flange = 2 * self.theta * (self.r2**2 - self.r1**2) / 2

        # Calculate the area of the web
        A_web = self.w * 2 * self.t

        # Total cross-sectional area
        A_total = A_flange + A_web

        return A_total


    def centroid_yc (self):
        """
        Calculates the centroid y-coordinate of the boom.
        Formula given in the Latex document
        """
        yc = ((2*self.t*self.w)*(self.w/2) + ((2*self.theta*self.r*self.t)*self.w + (2/3)*(self.r2**3 - self.r1**3)*(1 - np.cos(self.theta)))) / (2*self.theta*self.r*self.t + 2*self.t*self.w)
        return yc

    
    def centroid_xc (self):
        """
        Calculates the centroid x-coordinate of the boom.
        """
        return 0.0  # Due to symmetry


    def Ixxc (self):
        """
        Calculates the second moment of area (Ixx) of the boom about the centroid.
        Formula given in the Latex document.
        """
        yc = self.centroid_yc();
        Ixc = (2*self.t/3)*((self.w-yc)**3 + yc**3) + (1/8)*(self.r2**4 - self.r1**4)*(2*self.theta - np.sin(2*self.theta)) + (4/3)*(self.w - yc)*(self.r2**3 - self.r1**3)*(1 - np.cos(self.theta)) + ((self.w - yc)**2)*(self.r2**2 - self.r1**2)*self.theta
        return Ixc


    def Iyyc (self):
        """
        Calculates the second moment of area (Iyy) of the boom about the centroid.
        Formula given in Latex document.
        """
        Iyc = (2/3)*self.w*(self.t**3) + (1/8)*(self.r2**4 - self.r1**4)*(6*self.theta - 8*np.sin(self.theta) + np.sin(2*self.theta))
        return Iyc


    def J (self):
        """
        Calculates the Saint Venant Torsional Constant (J) of the boom.
        """
        s = self.r * self.theta
        Jval = (1/3) * (2*s*(self.t**3) + self.w*(2*self.t)**3)
        return Jval


    def flattened_height (self):
        """
        Calculates the flattened height of the boom.
        """

        h_flattened = self.w + self.r * self.theta
        return h_flattened

    def num_coils (self):
        """
        Calculates the number of wraps the boom goes around the spool in the packaged/undeployed configuration.
        """
        num = (-self.R + np.sqrt(self.R**2 + (2*self.L*self.t)/np.pi))/(2*self.t)
        return num

    def export_boom (self, filename):
        """
        Exports the boom properties to a JSON file.
        """

        with open(filename, "r") as f:
            existing_data = json.load(f)

        geometry = {
            "BONDED_WEB_LENGTH": self.w,
            "FLANGE_MEAN_RADIUS": self.r,
            "FLANGE_INNER_RADIUS": self.r1,
            "FLANGE_OUTER_RADIUS": self.r2,
            "FLANGE_THICKNESS": self.t,
            "FLANGE_SUBTENDED_ANGLE_DEG": existing_data["geometry"]["FLANGE_SUBTENDED_ANGLE_DEG"],
            "FLANGE_MEAN_ARCLENGTH": self.r * self.theta,
            "BOOM_FLATTENED_HEIGHT": self.flattened_height(),
            "BOOM_FLATTENED_WIDTH": 2 * self.t,
            "BOOM_LENGTH": existing_data["geometry"]["BOOM_LENGTH"]
        }

        section_properties = {
            "BOOM_CROSS_SECTIONAL_AREA": self.section_area(),
            "BOOM_CENTROID_X": self.centroid_xc(),
            "BOOM_CENTROID_Y": self.centroid_yc(),
            "BOOM_SECOND_MOMENT_OF_AREA_X": self.Ixxc(),
            "BOOM_SECOND_MOMENT_OF_AREA_Y": self.Iyyc(),
            "BOOM_TORSIONAL_CONSTANT": self.J()
        }

        existing_data["geometry"] = geometry
        existing_data["section_properties"] = section_properties

        with open(filename, "w") as f:
            json.dump(existing_data, f, indent=4)


    def export_spool (self, filename):
        """
        Exports the spool properties to a JSON file.
        """

        with open(filename, "r") as f:
            existing_data = json.load(f)

        geometry = {
            "HUB_RADIUS": existing_data["geometry"]["HUB_RADIUS"],
            "NUM_COILS_OF_BOOM": self.num_coils(),
            "HUB_COILED_RADIUS": np.ceil(self.num_coils()) * (2 * self.t) + self.R
        }

        existing_data["geometry"] = geometry

        with open(filename, "w") as f:
            json.dump(existing_data, f, indent=4)
        


# Substantiating the class to run the calculations and update the JSON.

with open("boom_properties.json", "r") as f:
    with open("spool_properties.json", "r") as g:
        boom = BoomGeometry(json.load(f), json.load(g))

boom.export_boom("boom_properties.json")
boom.export_spool("spool_properties.json")
