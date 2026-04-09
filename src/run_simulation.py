"""
Main simulation runner for Smart Microgrid
Run this script to execute the simulation and generate analysis
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.microgrid import MicrogridModel
from utils.visualization import create_comprehensive_report
from utils.electrical_analysis import generate_electrical_report, calculate_emission_savings
import pandas as pd


def run_simulation(
    n_households: int = 20,
    simulation_hours: int = 168,  # 1 week
    solar_penetration: float = 0.7,
    battery_penetration: float = 0.5,
    output_dir: str = './results',
    seed: int = 42
):
    """
    Run the complete microgrid simulation
    
    Args:
        n_households: Number of households in the microgrid
        simulation_hours: Number of hours to simulate
        solar_penetration: Fraction of households with solar (0-1)
        battery_penetration: Fraction of households with batteries (0-1)
        output_dir: Directory to save results
        seed: Random seed for reproducibility
    """
    
    print("=" * 60)
    print("SMART MICROGRID SIMULATION")
    print("=" * 60)
    print(f"\nConfiguration:")
    print(f"  • Households: {n_households}")
    print(f"  • Simulation Duration: {simulation_hours} hours ({simulation_hours/24:.1f} days)")
    print(f"  • Solar Penetration: {solar_penetration*100:.0f}%")
    print(f"  • Battery Penetration: {battery_penetration*100:.0f}%")
    print(f"  • Random Seed: {seed}")
    print("\n" + "-" * 60)
    
    # Create model
    print("\n[1/4] Initializing microgrid model...")
    model = MicrogridModel(
        n_households=n_households,
        solar_penetration=solar_penetration,
        battery_penetration=battery_penetration,
        seed=seed
    )
    
    # Count households with solar and batteries
    n_solar = sum(1 for agent in model.schedule.agents if agent.solar_capacity > 0)
    n_battery = sum(1 for agent in model.schedule.agents if agent.battery_capacity > 0)
    print(f"  ✓ Created {n_households} households")
    print(f"    - {n_solar} with solar panels ({n_solar/n_households*100:.1f}%)")
    print(f"    - {n_battery} with batteries ({n_battery/n_households*100:.1f}%)")
    
    # Run simulation
    print(f"\n[2/4] Running simulation for {simulation_hours} hours...")
    print("  ⏳ This may take a minute...")
    
    for hour in range(simulation_hours):
        model.step()
        if (hour + 1) % 24 == 0:
            print(f"  → Day {(hour + 1) // 24} complete")
    
    print("  ✓ Simulation complete!")
    
    # Extract data
    print("\n[3/4] Extracting and processing data...")
    model_data = model.datacollector.get_model_vars_dataframe().reset_index()
    agent_data = model.datacollector.get_agent_vars_dataframe().reset_index()
    
    print(f"  ✓ Collected {len(model_data)} timesteps of data")
    print(f"  ✓ Tracked {len(agent_data)} agent observations")
    
    # Generate reports
    print(f"\n[4/4] Generating analysis reports...")
    create_comprehensive_report(model_data, agent_data, output_dir=output_dir)
    
    # Generate electrical engineering report
    print("\n  → Calculating electrical metrics...")
    ee_report = generate_electrical_report(model_data, agent_data)
    ee_report.to_csv(f'{output_dir}/electrical_metrics.csv')
    
    # Calculate emission savings
    print("  → Calculating emission savings...")
    total_import = model_data['Grid Import'].sum()
    total_export = model_data['Grid Export'].sum()
    emissions = calculate_emission_savings(total_import, total_export)
    
    emissions_df = pd.DataFrame([emissions]).T
    emissions_df.columns = ['Value']
    emissions_df.to_csv(f'{output_dir}/emission_savings.csv')
    
    print("\n" + "=" * 60)
    print("SIMULATION COMPLETE!")
    print("=" * 60)
    
    # Print key results
    print("\n📊 KEY RESULTS:")
    print("-" * 60)
    
    total_generation = model_data['Total Generation'].sum()
    total_consumption = model_data['Total Consumption'].sum()
    avg_self_sufficiency = model_data['Self Sufficiency'].mean() * 100
    total_trades = model_data['Total Trades'].sum()
    
    print(f"\nEnergy Flows:")
    print(f"  • Total Solar Generation: {total_generation:.2f} kWh")
    print(f"  • Total Consumption: {total_consumption:.2f} kWh")
    print(f"  • Grid Import: {total_import:.2f} kWh")
    print(f"  • Grid Export: {total_export:.2f} kWh")
    print(f"  • Average Self-Sufficiency: {avg_self_sufficiency:.1f}%")
    
    print(f"\nTrading Activity:")
    print(f"  • Total P2P Trades: {int(total_trades)}")
    print(f"  • Average Trades per Hour: {total_trades/simulation_hours:.1f}")
    
    print(f"\nEnvironmental Impact:")
    print(f"  • Net CO2 Emissions: {emissions['net_emissions_kg']:.2f} kg")
    print(f"  • Equivalent to {emissions['equivalent_trees']:.1f} trees/year")
    
    print(f"\n📁 All results saved to: {output_dir}/")
    print("\nGenerated files:")
    print("  • energy_flows.png")
    print("  • trading_analysis.png")
    print("  • household_comparison.png")
    print("  • load_duration_curve.png")
    print("  • summary_statistics.csv")
    print("  • electrical_metrics.csv")
    print("  • emission_savings.csv")
    print("  • model_data.csv")
    print("  • agent_data.csv")
    
    print("\n" + "=" * 60)
    
    return model, model_data, agent_data


if __name__ == "__main__":
    # Run with default parameters
    model, model_data, agent_data = run_simulation(
        n_households=20,
        simulation_hours=168,  # 1 week
        solar_penetration=0.7,
        battery_penetration=0.5,
        output_dir='./results',
        seed=42
    )
    
    print("\n✨ You can now explore the results in the ./results/ directory!")
    print("💡 Tip: Modify the parameters in run_simulation() to test different scenarios")
