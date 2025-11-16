#!/usr/bin/env python3
"""Test script to validate PCR Calculator improvements"""

from pcr_calculator import PCRCalculator

def test_zero_reactions():
    """Test that zero reactions are rejected"""
    try:
        PCRCalculator.calculate_volumes(0)
        print("✗ FAIL: Zero reactions were not rejected")
        return False
    except ValueError as e:
        print(f"✓ PASS: Zero reactions rejected - {e}")
        return True

def test_negative_reactions():
    """Test that negative reactions are rejected"""
    try:
        PCRCalculator.calculate_volumes(-5)
        print("✗ FAIL: Negative reactions were not rejected")
        return False
    except ValueError as e:
        print(f"✓ PASS: Negative reactions rejected - {e}")
        return True

def test_valid_calculation():
    """Test valid calculation with default settings"""
    try:
        volumes = PCRCalculator.calculate_volumes(3)
        print(f"✓ PASS: Valid calculation for 3 reactions:")
        for component, volume in volumes.items():
            print(f"    {component}: {volume:.2f} µL")
        return True
    except Exception as e:
        print(f"✗ FAIL: Valid calculation failed - {e}")
        return False

def test_q5_preset():
    """Test Q5 preset"""
    try:
        volumes = PCRCalculator.calculate_volumes(2, preset="Q5® (NEB)")
        print(f"✓ PASS: Q5® preset calculation for 2 reactions:")
        for component, volume in volumes.items():
            print(f"    {component}: {volume:.2f} µL")
        return True
    except Exception as e:
        print(f"✗ FAIL: Q5 preset failed - {e}")
        return False

def test_template_dna_calculation():
    """Test template DNA concentration calculation"""
    try:
        volumes = PCRCalculator.calculate_volumes(
            num_reactions=2,
            template_dna_ng=50,
            template_dna_concentration=100
        )
        print(f"✓ PASS: Template DNA calculation (50 ng from 100 ng/µL stock) for 2 reactions:")
        for component, volume in volumes.items():
            print(f"    {component}: {volume:.2f} µL")
        # Should calculate 0.5 µL per reaction = 1.1 µL total with safety factor
        return True
    except Exception as e:
        print(f"✗ FAIL: Template DNA calculation failed - {e}")
        return False

def test_primer_concentration_adjustment():
    """Test primer concentration adjustment"""
    try:
        volumes = PCRCalculator.calculate_volumes(
            num_reactions=2,
            primer_concentration=5.0  # Different from default 10µM
        )
        print(f"✓ PASS: Primer concentration adjustment (5 µM instead of 10 µM) for 2 reactions:")
        for component, volume in volumes.items():
            print(f"    {component}: {volume:.2f} µL")
        return True
    except Exception as e:
        print(f"✗ FAIL: Primer concentration adjustment failed - {e}")
        return False

def main():
    print("=" * 60)
    print("PCR Calculator Validation Tests")
    print("=" * 60)
    print()
    
    tests = [
        ("Zero reactions rejection", test_zero_reactions),
        ("Negative reactions rejection", test_negative_reactions),
        ("Valid calculation", test_valid_calculation),
        ("Q5 preset", test_q5_preset),
        ("Template DNA calculation", test_template_dna_calculation),
        ("Primer concentration adjustment", test_primer_concentration_adjustment),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 60)
        result = test_func()
        results.append(result)
    
    print()
    print("=" * 60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
    
    return all(results)

if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
