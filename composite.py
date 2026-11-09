import numpy as np
import json


"""
Composite laminate property calculator (UDLaminate).

This file defines the UDLaminate class, which uses Classical Laminate Theory
to calculate the in-plane, coupling, and bending stiffness of a layered
unidirectional composite laminate.

The calculation starts from the orthotropic engineering properties of a
single lamina (E1, E2, nu12, nu21, and G12). It constructs the reduced
stiffness matrix Q, transforms that matrix for each ply orientation to
obtain Qbar, and integrates the transformed stiffness contributions through
the laminate thickness to assemble the 6x6 ABD stiffness matrix.

The class then uses the extensional stiffness matrix A to calculate
equivalent in-plane laminate properties:
- E1 and E2: effective axial and transverse Young's moduli.
- nu12 and nu21: effective Poisson's ratios.
- G12: effective in-plane shear modulus.

It also calculates the mass of a boom cross-section and the total boom
mass using the cross-sectional area, material density, and boom length.
The export() method writes the calculated laminate properties and mass
values into the "material" section of the supplied JSON file.

Input:
- A dictionary loaded from boom_properties.json. It is expected to contain
  the composite layout (lamina properties, total thickness, number of layers,
  and each layer's thickness and orientation), plus the boom section and
  geometry properties needed for the mass calculations.

Execution:
- The script loads boom_properties.json.
- It creates a UDLaminate object, which calculates the ABD matrix and
  equivalent laminate properties.
- It exports the resulting material properties back into
  boom_properties.json.

The calculations assume the laminate data and ply definitions supplied in
the JSON file are consistent. The ABD formulation and transformed stiffness
equations are implemented in the methods below.
"""

class UDLaminate:
    def __init__(self, data):
        # Store the input data, build the laminate ABD matrix, and derive effective properties.
        self.data = data
        self.composite_stiffness = self.ABD_matrix_calculator()
        self.composite_properties()

    def Q_matrix_calculator (self, E1, E2, nu12, nu21, G12):
        # Build the reduced stiffness matrix Q for one orthotropic lamina in its material axes.
        Q = np.zeros((3, 3))
        Q[0][0] = -E1 / (nu12*nu21 - 1)
        Q[0][1] = (-nu12*E2) / (nu12*nu21 - 1)
        Q[0][2] = 0
        Q[1][0] = (-nu21*E1) / (nu12*nu21 - 1)
        Q[1][1] = -E2 / (nu12*nu21 - 1)
        Q[1][2] = 0
        Q[2][0] = 0
        Q[2][1] = 0
        Q[2][2] = G12
        return Q

    def Qbar_matrix_calculator (self, Q, theta):
        # Transform Q into the laminate/global axes for a ply oriented at theta degrees.
        Qbar = np.zeros((3, 3))
        m = np.cos(np.radians(theta))
        n = np.sin(np.radians(theta))
        Qbar[0][0] = Q[0][0]*m**4 + 2*(Q[0][1] + 2*Q[2][2])*(m**2)*(n**2) + Q[1][1]*n**4
        Qbar[0][1] = (Q[0][0] + Q[1][1] - 4*Q[2][2])*(m**2)*(n**2) + Q[0][1]*(m**4 + n**4)
        Qbar[0][2] = (Q[0][0] - Q[0][1] - 2*Q[2][2])*(m**3)*(n) + (Q[0][1] - Q[1][1] + 2*Q[2][2])*(m)*(n**3)
        Qbar[1][0] = Qbar[0][1]
        Qbar[1][1] = Q[0][0]*n**4 + 2*(Q[0][1] + 2*Q[2][2])*(m**2)*(n**2) + Q[1][1]*m**4
        Qbar[1][2] = (Q[0][1] - Q[1][1] + 2*Q[2][2])*(m**3)*(n) + (Q[0][0] - Q[0][1] - 2*Q[2][2])*(m)*(n**3)
        Qbar[2][0] = Qbar[0][2]
        Qbar[2][1] = Qbar[1][2]
        Qbar[2][2] = (Q[0][0] + Q[1][1] - 2*Q[0][1] - 2*Q[2][2])*(m**2)*(n**2) + Q[2][2]*(m**4 + n**4)
        return Qbar

    def ABD_matrix_calculator (self):
        # Integrate each ply's transformed stiffness through the thickness to assemble A, B, and D.
        A = np.zeros((3, 3))
        B = np.zeros((3, 3))
        D = np.zeros((3, 3))
        composite_stiffness = np.zeros((6, 6))

        thickness = self.data["composite_layout"]["total_thickness"]
        numlayers = self.data["composite_layout"]["num_layers"]
        E1 = self.data["composite_layout"]["E1"]
        E2 = self.data["composite_layout"]["E2"]
        nu12 = self.data["composite_layout"]["nu12"]
        nu21 = self.data["composite_layout"]["nu21"]
        G12 = self.data["composite_layout"]["G12"]
        
        z_tillnow = -thickness / 2

        for k in range(1, numlayers + 1):
            # Extract layer properties from data
            layer_thickness = self.data["composite_layout"]["layer" + str(k)]["thickness"]
            theta = self.data["composite_layout"]["layer" + str(k)]["theta"]
            
            Q = self.Q_matrix_calculator(E1, E2, nu12, nu21, G12)
            Qbar = self.Qbar_matrix_calculator(Q, theta)

            for i in range(3):
                for j in range(3):
                    A[i][j] = A[i][j] + Qbar[i][j] * layer_thickness
                    B[i][j] = B[i][j] + 0.5 * Qbar[i][j] * ((z_tillnow + layer_thickness)**2 - z_tillnow**2)
                    D[i][j] = D[i][j] + (1/3) * Qbar[i][j] * ((z_tillnow + layer_thickness)**3 - z_tillnow**3)

            z_tillnow = z_tillnow + layer_thickness

        composite_stiffness[0:3, 0:3] = A
        composite_stiffness[0:3, 3:6] = B
        composite_stiffness[3:6, 0:3] = B
        composite_stiffness[3:6, 3:6] = D
        return composite_stiffness

    def composite_properties (self):
        # Invert A to obtain effective in-plane laminate moduli and Poisson's ratios.
        A = self.composite_stiffness[0:3, 0:3]
        S = np.linalg.inv(A)
        self.E1 = 1 / (S[0][0] * self.data["composite_layout"]["total_thickness"])
        self.E2 = 1 / (S[1][1] * self.data["composite_layout"]["total_thickness"])
        self.nu12 = -S[0][1] / S[0][0]
        self.nu21 = -S[1][0] / S[1][1]
        self.G12 = 1 / (S[2][2] * self.data["composite_layout"]["total_thickness"])

    def section_mass (self):
        # Calculate mass per unit boom length from cross-sectional area and composite density.
        return self.data["section_properties"]["BOOM_CROSS_SECTIONAL_AREA"] * self.data["composite_layout"]["Density"]

    def total_mass (self):
        # Multiply the section mass per unit length by the total boom length.
        return self.section_mass() * self.data["geometry"]["BOOM_LENGTH"]

    def export (self, filename):
        """
        Exports the laminate properties to a JSON file.
        """

        with open(filename, "r") as f:
            existing_data = json.load(f)
        
        laminate_properties = {
            "DENSITY": existing_data["composite_layout"]["Density"],
            "E1": self.E1,
            "E2": self.E2,
            "nu12": self.nu12,
            "nu21": self.nu21,
            "G12": self.G12,
            "SECTION_MASS": self.section_mass(),
            "TOTAL_MASS": self.total_mass()
        }

        existing_data["material"] = laminate_properties

        with open(filename, "w") as f:
            json.dump(existing_data, f, indent=4)


# Creates an instance of the UDLaminate class to run calculations and
# update the material parameters.

with open("boom_properties.json", "r") as f:
    laminate = UDLaminate(json.load(f))

laminate.export("boom_properties.json")