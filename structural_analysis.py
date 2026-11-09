import numpy as np
import json

class StructuralAnalysis:
    def __init__ (self, boom_data, spool_data):
        self.data = boom_data
        self.E1 = self.data["material"]["E1"]
        self.E2 = self.data["material"]["E2"]
        self.G12 = self.data["material"]["G12"]
        self.t = self.data["geometry"]["FLANGE_THICKNESS"]
        self.r = self.data["geometry"]["FLANGE_MEAN_RADIUS"]
        self.r1 = self.data["geometry"]["FLANGE_INNER_RADIUS"]
        self.r2 = self.data["geometry"]["FLANGE_OUTER_RADIUS"]
        self.R = spool_data["geometry"]["HUB_RADIUS"]
        self.Ixxc = self.data["section_properties"]["BOOM_SECOND_MOMENT_OF_AREA_X"]
        self.Iyyc = self.data["section_properties"]["BOOM_SECOND_MOMENT_OF_AREA_Y"]
        self.yield_shear = self.data["structural_analysis"]["MATRIX_SHEAR_YIELD_STRESS"]
        self.phi = np.radians(self.data["structural_analysis"]["FIBER_MISALIGNMENT_ANGLE_DEG"])
        self.sigma_c_limit = self.data["structural_analysis"]["AXIAL_COMPRESSIVE_YIELD_STRESS"]
        self.scf = self.data["structural_analysis"]["SCF"]
        

    def flattening_tensile_strain (self):
        return self.t / (2 * self.r1)

    def flattening_compressive_strain (self):
        return self.t / (2 * self.r2)

    def coiling_strain (self):
        return self.t / (2 * (self.R + self.t / 2))

    def flattening_stress (self, strain):
        return self.E2 * strain

    def coiling_stress (self, strain):
        return self.E1 * strain

    def yield_shear_strain (self):
        return self.yield_shear / self.G12

    def microbuckling_compressive_stress (self):
        """
        Budiansky-Argon fiber microbuckling compressive strength
        sigma_c = G12 / (1 + phi / gamma_y)
        """
        gamma_y = self.yield_shear_strain()
        return self.G12 / (1 + self.phi/gamma_y)

    def max_allowed_stress (self):
        return min(self.microbuckling_compressive_stress(), self.sigma_c_limit)

    def safety_factor (self):
        return self.max_allowed_stress() / (self.scf * self.coiling_stress(self.coiling_strain()))

    def export (self, filename):
        with open(filename, "r") as f:
            existing_data = json.load(f)
        
        structural_analysis = {
            "MAX_DESIGN_STRAIN": existing_data["structural_analysis"]["MAX_DESIGN_STRAIN"],
            "DESIGN_SAFETY_FACTOR": existing_data["structural_analysis"]["DESIGN_SAFETY_FACTOR"],
            "ACTUAL_SAFETY_FACTOR": self.safety_factor(),
            "FIBER_MISALIGNMENT_ANGLE_DEG": existing_data["structural_analysis"]["FIBER_MISALIGNMENT_ANGLE_DEG"],
            "SCF": existing_data["structural_analysis"]["SCF"],
            "MATRIX_SHEAR_YIELD_STRESS": existing_data["structural_analysis"]["MATRIX_SHEAR_YIELD_STRESS"],
            "MATRIX_SHEAR_YIELD_STRAIN": self.yield_shear_strain(),
            "AXIAL_COMPRESSIVE_YIELD_STRESS": existing_data["structural_analysis"]["AXIAL_COMPRESSIVE_YIELD_STRESS"],
            "EI_AXIAL_X": self.E1 * self.Ixxc,
            "EI_AXIAL_Y": self.E1 * self.Iyyc,
            "GJ": self.data["material"]["G12"] * self.data["section_properties"]["BOOM_TORSIONAL_CONSTANT"],
            "FLATTENING_TENSILE_STRAIN": self.flattening_tensile_strain(),
            "FLATTENING_COMPRESSIVE_STRAIN": self.flattening_compressive_strain(),
            "FLATTENING_TENSILE_STRESS": self.flattening_stress(self.flattening_tensile_strain()),
            "FLATTENING_COMPRESSIVE_STRESS": self.flattening_stress(self.flattening_compressive_strain()),
            "COILING_MAX_STRAIN": self.coiling_strain(),
            "COILING_MAX_STRESS": self.coiling_stress(self.coiling_strain())
        }

        existing_data["structural_analysis"] = structural_analysis

        with open(filename, "w") as f:
            json.dump(existing_data, f, indent=4)



with open("boom_properties.json", "r") as f:
    with open("spool_properties.json", "r") as g:
        sa = StructuralAnalysis(json.load(f), json.load(g))

sa.export("boom_properties.json")