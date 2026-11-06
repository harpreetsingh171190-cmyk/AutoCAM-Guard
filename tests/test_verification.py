"""
Unit Tests for AutoCAM-Guard Engine
Author: Harpreet Singh
"""

from core.engine import AutoCAMGuardEngine

def test_cnc_verification_pass():
    engine = AutoCAMGuardEngine()
    good_gcode = "G21 G90\nG54\nT1 M6\nS8000 M3\nG00 X0 Y0 Z5\nG01 Z-1 F300"
    res = engine.cnc_checker.audit_gcode(good_gcode)
    assert res["status"] == "APPROVED"
    assert res["safety_verdict"]["work_coordinate_system_present"] is True

def test_cnc_verification_fail():
    engine = AutoCAMGuardEngine()
    bad_gcode = "G21 G90\nG01 X10 Y10 F500"
    res = engine.cnc_checker.audit_gcode(bad_gcode)
    assert res["status"] == "REJECTED"

def test_additive_oversize():
    engine = AutoCAMGuardEngine()
    res = engine.additive_checker.audit_mesh_file("test.stl", bounds=(300.0, 200.0, 100.0))
    assert res["status"] == "FAIL_OVERSIZE"

if __name__ == "__main__":
    test_cnc_verification_pass()
    test_cnc_verification_fail()
    test_additive_oversize()
    print("All unit tests passed successfully!")
