"""
CNC Preflight Inspection
Author: Harpreet Singh
"""

class CNCPreflight:
    def __init__(self, config: dict):
        self.config = config
        self.author = "Harpreet Singh"

    def audit_gcode(self, gcode_text: str) -> dict:
        rules = self.config.get("thresholds", {}).get("cnc", {})
        allowed_wcs = rules.get("allowed_wcs", ["G54", "G55", "G56", "G57", "G58", "G59"])
        max_rpm = rules.get("max_spindle_rpm", 12000)

        has_wcs = any(wcs in gcode_text for wcs in allowed_wcs)
        has_tool = "T" in gcode_text and "M6" in gcode_text
        has_spindle = "S" in gcode_text and ("M3" in gcode_text or "M03" in gcode_text)
        has_motion = "G0" in gcode_text or "G00" in gcode_text or "G1" in gcode_text or "G01" in gcode_text

        passed = has_wcs and has_tool and has_spindle and has_motion
        return {
            "module": "CNC_Preflight_Agent",
            "author": self.author,
            "status": "APPROVED" if passed else "REJECTED",
            "safety_verdict": {
                "work_coordinate_system_present": has_wcs,
                "tool_call_verified": has_tool,
                "spindle_rpm_safe": has_spindle,
                "feed_motion_commanded": has_motion
            }
        }
