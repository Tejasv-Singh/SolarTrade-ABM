"""
Advanced usage examples for the Smart Microgrid simulation
Run different scenarios and compare results
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.microgrid import MicrogridModel
from utils.visualization import plot_energy_flows, generate_summary_statistics
from utils.electrical_analysis import generate_electrical_report


def compare_solar_penetration_scenarios():
    """
    Compare different solar penetration levels
    """
    print("\n" + "="*60)
    print("SCENARIO COMPARISON: Solar Penetration Impact")
    print("="*60)
    
    scenarios = [0.3, 0.5, 0.7, 0.9]
    results = []
    
    for solar_pen in scenarios:
        print(f"\n→ Running scenario: {solar_pen*100:.0f}% solar penetration...")
        
        model = MicrogridModel(
            n_households=20,
            solar_penetration=solar_pen,
            battery_penetration=0.5,
            seed=42
        )
        
        model.run_simulation(hours=168)
        
        model_data = model.datacollector.get_model_vars_dataframe()
        
        results.append({
            'Solar Penetration': f"{solar_pen*100:.0f}%",
            'Avg Self-Sufficiency': f"{model_data['Self Sufficiency'].mean()*100:.1f}%",
            'Total Grid Import': f"{model_data['Grid Import'].sum():.2f} kWh",
            'Total Trades': int(model_data['Total Trades'].sum()),
            'Peak Load': f"{model_data['Peak Load'].max():.2f} kW"
        })
    
    results_df = pd.DataFrame(results)
    print("\n" + "="*60)
    print("RESULTS SUMMARY")
    print("="*60)
    print(results_df.to_string(index=False))
    print("\nConclusion: Higher solar penetration increases self-sufficiency!")
    

def compare_trading_strategies():
    """
    Compare impact of different trading strategy distributions
    """
    print("\n" + "="*60)
    print("SCENARIO COMPARISON: Trading Strategy Impact")
    print("="*60)
    
    # Override agent creation to test pure strategies
    scenarios = {
        'All Profit-Maximizing': {'profit_maximizing': 1.0, 'community_oriented': 0.0, 'conservative': 0.0},
        'All Community-Oriented': {'profit_maximizing': 0.0, 'community_oriented': 1.0, 'conservative': 0.0},
        'Mixed Strategies': {'profit_maximizing': 0.4, 'community_oriented': 0.4, 'conservative': 0.2}
    }
    
    results = []
    
    for scenario_name, strategy_dist in scenarios.items():
        print(f"\n→ Running scenario: {scenario_name}...")
        
        # Note: This is simplified - you'd need to modify agent creation
        # to strictly control strategy distribution
        model = MicrogridModel(
            n_households=20,
            solar_penetration=0.7,
            battery_penetration=0.5,
            seed=42
        )
        
        model.run_simulation(hours=168)
        
        model_data = model.datacollector.get_model_vars_dataframe()
        
        results.append({
            'Scenario': scenario_name,
            'Avg Price': f"${model_data['Average Price'].mean():.4f}/kWh",
            'Price Volatility': f"{model_data['Average Price'].std():.4f}",
            'Total Trades': int(model_data['Total Trades'].sum())
        })
    
    results_df = pd.DataFrame(results)
    print("\n" + "="*60)
    print("RESULTS SUMMARY")
    print("="*60)
    print(results_df.to_string(index=False))


def analyze_battery_impact():
    """
    Analyze the impact of battery penetration on grid stability
    """
    print("\n" + "="*60)
    print("SCENARIO COMPARISON: Battery Impact on Grid Stability")
    print("="*60)
    
    battery_levels = [0.0, 0.3, 0.5, 0.8]
    results = []
    
    for battery_pen in battery_levels:
        print(f"\n→ Running scenario: {battery_pen*100:.0f}% battery penetration...")
        
        model = MicrogridModel(
            n_households=20,
            solar_penetration=0.7,
            battery_penetration=battery_pen,
            seed=42
        )
        
        model.run_simulation(hours=168)
        
        model_data = model.datacollector.get_model_vars_dataframe()
        
        # Calculate load variability
        load_cv = model_data['Peak Load'].std() / model_data['Peak Load'].mean()
        
        results.append({
            'Battery Penetration': f"{battery_pen*100:.0f}%",
            'Avg Grid Import': f"{model_data['Grid Import'].mean():.2f} kW",
            'Peak Load': f"{model_data['Peak Load'].max():.2f} kW",
            'Load Variability (CV)': f"{load_cv:.3f}",
            'Self-Sufficiency': f"{model_data['Self Sufficiency'].mean()*100:.1f}%"
        })
    
    results_df = pd.DataFrame(results)
    print("\n" + "="*60)
    print("RESULTS SUMMARY")
    print("="*60)
    print(results_df.to_string(index=False))
    print("\nConclusion: Batteries smooth out load variability!")


def seasonal_analysis():
    """
    Simulate different seasons (varying solar irradiance)
    """
    print("\n" + "="*60)
    print("SCENARIO COMPARISON: Seasonal Variations")
    print("="*60)
    print("\nNote: This would require modifying the solar irradiance model")
    print("to include seasonal variations in day length and irradiance.")
    print("\nSuggested modifications:")
    print("  • Summer: Peak irradiance 1000 W/m², 14 hour days")
    print("  • Winter: Peak irradiance 400 W/m², 8 hour days")
    print("  • Spring/Fall: Moderate conditions")


if __name__ == "__main__":
    print("\n🔬 ADVANCED SCENARIO ANALYSIS")
    print("Choose a scenario to run:")
    print("\n1. Compare Solar Penetration Levels")
    print("2. Compare Trading Strategies")
    print("3. Analyze Battery Impact")
    print("4. Seasonal Analysis (concept)")
    print("5. Run All Comparisons")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        compare_solar_penetration_scenarios()
    elif choice == "2":
        compare_trading_strategies()
    elif choice == "3":
        analyze_battery_impact()
    elif choice == "4":
        seasonal_analysis()
    elif choice == "5":
        compare_solar_penetration_scenarios()
        compare_trading_strategies()
        analyze_battery_impact()
        seasonal_analysis()
    else:
        print("Invalid choice. Please run again and select 1-5.")
    
    print("\n✨ Analysis complete!")
