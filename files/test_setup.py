"""
Quick test to verify the simulation works
Run this before the full simulation to check everything is set up correctly
"""

import sys
import os

print("Testing Smart Microgrid Simulation Setup...")
print("=" * 60)

# Test imports
print("\n[1/4] Testing imports...")
try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from mesa import Model, Agent
    print("  ✓ All dependencies imported successfully")
except ImportError as e:
    print(f"  ✗ Import error: {e}")
    print("  → Run: pip install -r requirements.txt")
    sys.exit(1)

# Test project imports
print("\n[2/4] Testing project modules...")
try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from models.microgrid import MicrogridModel
    from agents.household import HouseholdAgent
    from utils.visualization import generate_summary_statistics
    from utils.electrical_analysis import generate_electrical_report
    print("  ✓ All project modules imported successfully")
except ImportError as e:
    print(f"  ✗ Import error: {e}")
    sys.exit(1)

# Test model creation
print("\n[3/4] Testing model creation...")
try:
    model = MicrogridModel(n_households=5, solar_penetration=0.6, battery_penetration=0.4, seed=42)
    print(f"  ✓ Created microgrid with {model.n_households} households")
    
    # Count agents
    n_solar = sum(1 for agent in model.schedule.agents if agent.solar_capacity > 0)
    n_battery = sum(1 for agent in model.schedule.agents if agent.battery_capacity > 0)
    print(f"    - {n_solar} households with solar")
    print(f"    - {n_battery} households with batteries")
except Exception as e:
    print(f"  ✗ Model creation error: {e}")
    sys.exit(1)

# Test simulation step
print("\n[4/4] Testing simulation execution...")
try:
    # Run a few steps
    for i in range(24):  # 1 day
        model.step()
    
    model_data = model.datacollector.get_model_vars_dataframe()
    agent_data = model.datacollector.get_agent_vars_dataframe()
    
    print(f"  ✓ Simulation ran for 24 hours")
    print(f"    - Collected {len(model_data)} timesteps")
    print(f"    - Tracked {len(agent_data)} agent observations")
    
    # Quick stats
    total_gen = model_data['Total Generation'].sum()
    total_con = model_data['Total Consumption'].sum()
    print(f"    - Total generation: {total_gen:.2f} kWh")
    print(f"    - Total consumption: {total_con:.2f} kWh")
    
except Exception as e:
    print(f"  ✗ Simulation error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("\nYou're ready to run the full simulation:")
print("  python run_simulation.py")
print("\nOr explore advanced scenarios:")
print("  python advanced_examples.py")
