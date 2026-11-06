"""
AutoCAM-Guard: Unified Manufacturing Verification & Routing Engine
Author: Harpreet Singh
"""

import os
import json
from pathlib import Path
from .cad_validator import CADValidator
from .cnc_preflight import CNCPreflight
from .additive_check import AdditiveChecker
from .laser_analyzer import LaserAnalyzer

class AutoCAMGuardEngine:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "..", "config", "rules.json")
        self.config_path = config_path
        self.config = self._load_config()
        self.author = "Harpreet Singh"
        self.cad_validator = CADValidator(self.config)
        self.cnc_checker = CNCPreflight(self.config)
        self.additive_checker = AdditiveChecker(self.config)
        self.laser_analyzer = LaserAnalyzer(self.config)

    def _load_config(self) -> dict:
        if not os.path.exists(self.config_path):
            return {
                "thresholds": {
                    "cnc": {"max_spindle_rpm": 12000, "safe_retract_height_mm": 5.0, "allowed_wcs": ["G54", "G55", "G56"]},
                    "additive": {"max_build_x_mm": 250.0, "max_build_y_mm": 210.0, "max_build_z_mm": 220.0},
                    "laser": {"allow_open_vectors": False}
                }
            }
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def run_full_audit(self, file_path: str, process_type: str = "auto") -> dict:
        ext = Path(file_path).suffix.lower()
        if process_type == "auto":
            if ext in [".nc", ".gcode", ".tap"]:
                process_type = "cnc"
            elif ext in [".stl", ".3mf"]:
                process_type = "additive"
            elif ext in [".dxf", ".svg"]:
                process_type = "laser"
            else:
                process_type = "cad"

        if process_type == "cnc":
            with open(file_path, "r", errors="ignore") as f:
                content = f.read()
            return self.cnc_checker.audit_gcode(content)
        elif process_type == "additive":
            return self.additive_checker.audit_mesh_file(file_path)
        elif process_type == "laser":
            return self.laser_analyzer.audit_vector_file(file_path)
        else:
            return self.cad_validator.audit_step(file_path)

if __name__ == "__main__":
    engine = AutoCAMGuardEngine()
    print(f"[*] Initialized AutoCAM-Guard Engine | Lead Developer: {engine.author}")
    demo_gcode = "G21 G90\nG54\nT1 M6\nS8000 M3\nG00 X10.0 Y10.0 Z5.0\nG01 Z-2.0 F500\nM5\nM30"
    res = engine.cnc_checker.audit_gcode(demo_gcode)
    print(json.dumps(res, indent=2))
