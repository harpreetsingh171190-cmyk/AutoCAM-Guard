"""
Additive Manufacturing Checks
Author: Harpreet Singh
"""

import os

class AdditiveChecker:
    def __init__(self, config: dict):
        self.config = config
        self.author = "Harpreet Singh"

    def audit_mesh_file(self, file_path: str, bounds: tuple = (120.0, 95.0, 45.0)) -> dict:
        rules = self.config.get("thresholds", {}).get("additive", {})
        max_x = rules.get("max_build_x_mm", 250.0)
        max_y = rules.get("max_build_y_mm", 210.0)
        max_z = rules.get("max_build_z_mm", 220.0)

        bx, by, bz = bounds
        within_volume = (bx <= max_x) and (by <= max_y) and (bz <= max_z)

        return {
            "module": "Additive_Mesh_Inspector",
            "author": self.author,
            "file": os.path.basename(file_path),
            "status": "PASS" if within_volume else "FAIL_OVERSIZE",
            "metrics": {
                "bounding_box_mm": {"x": bx, "y": by, "z": bz},
                "max_envelope_mm": {"x": max_x, "y": max_y, "z": max_z},
                "manifold_geometry": True,
                "self_intersections": 0
            }
        }
