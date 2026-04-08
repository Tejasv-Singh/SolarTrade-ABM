"""
Electrical Engineering Analysis Utilities
Calculate grid stability, power quality, and efficiency metrics
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple


def calculate_voltage_drop(power: float, distance: float, voltage: float = 230, 
                           conductor_resistance: float = 0.164) -> float:
    """
    Calculate voltage drop in distribution line
    
    Args:
        power: Power transmitted (kW)
        distance: Distance (km)
        voltage: Nominal voltage (V)
        conductor_resistance: Resistance per km (ohm/km) - default for 16mm² Cu
        
    Returns:
        Voltage drop (V)
    """
    current = (power * 1000) / voltage  # Convert kW to W, calculate current
    voltage_drop = current * conductor_resistance * distance
    return voltage_drop


def calculate_power_losses(power: float, distance: float, voltage: float = 230,
                           conductor_resistance: float = 0.164) -> float:
    """
    Calculate I²R losses in distribution line
    
    Args:
        power: Power transmitted (kW)
        distance: Distance (km)
        voltage: Nominal voltage (V)
        conductor_resistance: Resistance per km (ohm/km)
        
    Returns:
        Power loss (kW)
    """
    current = (power * 1000) / voltage
    resistance = conductor_resistance * distance
    power_loss = (current ** 2) * resistance / 1000  # Convert to kW
    return power_loss


def calculate_power_factor(active_power: float, reactive_power: float) -> float:
    """
    Calculate power factor
    
    Args:
        active_power: Real power (kW)
        reactive_power: Reactive power (kVAR)
        
    Returns:
        Power factor (0-1)
    """
    apparent_power = np.sqrt(active_power**2 + reactive_power**2)
    if apparent_power == 0:
        return 1.0
    return active_power / apparent_power


def calculate_load_factor(average_load: float, peak_load: float) -> float:
    """
    Calculate load factor (utilization efficiency)
    
    Args:
        average_load: Average load (kW)
        peak_load: Peak load (kW)
        
    Returns:
        Load factor (0-1)
    """
    if peak_load == 0:
        return 0.0
    return average_load / peak_load


def calculate_capacity_factor(actual_generation: float, rated_capacity: float, 
                              hours: float) -> float:
    """
    Calculate capacity factor for solar generation
    
    Args:
        actual_generation: Actual energy generated (kWh)
        rated_capacity: Rated capacity (kW)
        hours: Time period (hours)
        
    Returns:
        Capacity factor (0-1)
    """
    potential_generation = rated_capacity * hours
    if potential_generation == 0:
        return 0.0
    return actual_generation / potential_generation


def analyze_grid_stability(model_data: pd.DataFrame, agent_data: pd.DataFrame) -> Dict:
    """
    Analyze grid stability metrics
    
    Args:
        model_data: Model-level time series data
        agent_data: Agent-level time series data
        
    Returns:
        Dictionary with stability metrics
    """
    stability_metrics = {}
    
    # Load factor
    avg_load = model_data['Peak Load'].mean()
    peak_load = model_data['Peak Load'].max()
    stability_metrics['load_factor'] = calculate_load_factor(avg_load, peak_load)
    
    # Load variability (coefficient of variation)
    stability_metrics['load_cv'] = model_data['Peak Load'].std() / model_data['Peak Load'].mean()
    
    # Generation-demand mismatch
    mismatch = abs(model_data['Total Generation'] - model_data['Total Consumption'])
    stability_metrics['avg_mismatch_kw'] = mismatch.mean()
    stability_metrics['max_mismatch_kw'] = mismatch.max()
    
    # Grid dependency
    total_consumption = model_data['Total Consumption'].sum()
    total_grid_import = model_data['Grid Import'].sum()
    stability_metrics['grid_dependency'] = total_grid_import / total_consumption if total_consumption > 0 else 0
    
    # Ramping rate (kW/hour) - measure of how fast load changes
    load_changes = model_data['Peak Load'].diff().abs()
    stability_metrics['avg_ramp_rate'] = load_changes.mean()
    stability_metrics['max_ramp_rate'] = load_changes.max()
    
    return stability_metrics


def analyze_solar_performance(agent_data: pd.DataFrame) -> Dict:
    """
    Analyze solar generation performance
    
    Args:
        agent_data: Agent-level time series data
        
    Returns:
        Dictionary with solar performance metrics
    """
    solar_metrics = {}
    
    # Filter agents with solar
    solar_agents = agent_data[agent_data['Solar Generated'] > 0]['AgentID'].unique()
    
    if len(solar_agents) > 0:
        # Total generation
        total_gen = agent_data[agent_data['AgentID'].isin(solar_agents)]['Solar Generated'].sum()
        solar_metrics['total_generation_kwh'] = total_gen
        
        # Average generation per solar household
        solar_metrics['avg_generation_per_household_kwh'] = total_gen / len(solar_agents)
        
        # Peak generation hour
        hourly_gen = agent_data.groupby(agent_data.index)['Solar Generated'].sum()
        solar_metrics['peak_generation_hour'] = hourly_gen.idxmax()
        solar_metrics['peak_generation_kw'] = hourly_gen.max()
        
        # Capacity factor (assuming ~5kW average capacity and looking at a week)
        # This is approximate as we don't have exact capacity in the data
        hours = len(agent_data) / len(agent_data['AgentID'].unique())
        solar_metrics['estimated_capacity_factor'] = total_gen / (5.0 * len(solar_agents) * hours)
        
    return solar_metrics


def analyze_battery_performance(agent_data: pd.DataFrame) -> Dict:
    """
    Analyze battery storage performance
    
    Args:
        agent_data: Agent-level time series data
        
    Returns:
        Dictionary with battery performance metrics
    """
    battery_metrics = {}
    
    # Filter agents with batteries
    battery_agents = agent_data[agent_data['Battery SOC'] > 0]['AgentID'].unique()
    
    if len(battery_agents) > 0:
        battery_data = agent_data[agent_data['AgentID'].isin(battery_agents)]
        
        # Average state of charge
        battery_metrics['avg_soc_kwh'] = battery_data['Battery SOC'].mean()
        
        # SOC range (utilization)
        battery_metrics['min_soc_kwh'] = battery_data['Battery SOC'].min()
        battery_metrics['max_soc_kwh'] = battery_data['Battery SOC'].max()
        battery_metrics['soc_range_kwh'] = battery_metrics['max_soc_kwh'] - battery_metrics['min_soc_kwh']
        
        # Cycling activity (count SOC changes > 1 kWh)
        for agent_id in battery_agents:
            agent_battery = battery_data[battery_data['AgentID'] == agent_id]['Battery SOC']
            soc_changes = agent_battery.diff().abs()
            battery_metrics[f'agent_{agent_id}_cycles'] = (soc_changes > 1.0).sum()
        
        # Average battery utilization
        avg_utilization = battery_data.groupby('AgentID')['Battery SOC'].std().mean()
        battery_metrics['avg_utilization_std'] = avg_utilization
        
    return battery_metrics


def calculate_economic_metrics(agent_data: pd.DataFrame) -> Dict:
    """
    Calculate economic performance metrics
    
    Args:
        agent_data: Agent-level time series data
        
    Returns:
        Dictionary with economic metrics
    """
    economic_metrics = {}
    
    # Group by agent to get totals
    agent_totals = agent_data.groupby('AgentID').agg({
        'Revenue': 'sum',
        'Cost': 'sum',
        'Solar Generated': 'sum',
        'Energy Consumed': 'sum'
    })
    
    # Net revenue
    agent_totals['Net Revenue'] = agent_totals['Revenue'] - agent_totals['Cost']
    
    economic_metrics['total_revenue'] = agent_totals['Revenue'].sum()
    economic_metrics['total_cost'] = agent_totals['Cost'].sum()
    economic_metrics['total_net_revenue'] = agent_totals['Net Revenue'].sum()
    
    economic_metrics['avg_household_revenue'] = agent_totals['Revenue'].mean()
    economic_metrics['avg_household_cost'] = agent_totals['Cost'].mean()
    economic_metrics['avg_household_net_revenue'] = agent_totals['Net Revenue'].mean()
    
    # Profitability distribution
    profitable_households = (agent_totals['Net Revenue'] > 0).sum()
    economic_metrics['profitable_households_pct'] = (profitable_households / len(agent_totals)) * 100
    
    # Levelized cost of energy (LCOE) approximation
    total_generation = agent_totals['Solar Generated'].sum()
    if total_generation > 0:
        # Simplified LCOE (not accounting for capital costs, just operational)
        economic_metrics['operational_lcoe'] = economic_metrics['total_cost'] / total_generation
    
    return economic_metrics


def generate_electrical_report(model_data: pd.DataFrame, agent_data: pd.DataFrame) -> pd.DataFrame:
    """
    Generate comprehensive electrical engineering report
    
    Args:
        model_data: Model-level time series data
        agent_data: Agent-level time series data
        
    Returns:
        DataFrame with all electrical metrics
    """
    all_metrics = {}
    
    # Grid stability
    stability = analyze_grid_stability(model_data, agent_data)
    all_metrics.update({f'Stability_{k}': v for k, v in stability.items()})
    
    # Solar performance
    solar = analyze_solar_performance(agent_data)
    all_metrics.update({f'Solar_{k}': v for k, v in solar.items()})
    
    # Battery performance
    battery = analyze_battery_performance(agent_data)
    all_metrics.update({f'Battery_{k}': v for k, v in battery.items()})
    
    # Economic metrics
    economic = calculate_economic_metrics(agent_data)
    all_metrics.update({f'Economic_{k}': v for k, v in economic.items()})
    
    # Convert to DataFrame
    metrics_df = pd.DataFrame([all_metrics]).T
    metrics_df.columns = ['Value']
    metrics_df.index.name = 'Metric'
    
    return metrics_df


def calculate_emission_savings(grid_import_kwh: float, grid_export_kwh: float,
                               grid_emission_factor: float = 0.5) -> Dict:
    """
    Calculate CO2 emission savings from microgrid
    
    Args:
        grid_import_kwh: Total energy imported from grid (kWh)
        grid_export_kwh: Total energy exported to grid (kWh)
        grid_emission_factor: Grid emission factor (kg CO2/kWh)
        
    Returns:
        Dictionary with emission metrics
    """
    emissions = {}
    
    # Emissions from grid import
    emissions['import_emissions_kg'] = grid_import_kwh * grid_emission_factor
    
    # Avoided emissions from export (displacing grid generation)
    emissions['avoided_emissions_kg'] = grid_export_kwh * grid_emission_factor
    
    # Net emissions
    emissions['net_emissions_kg'] = emissions['import_emissions_kg'] - emissions['avoided_emissions_kg']
    
    # Equivalent trees (1 tree absorbs ~21 kg CO2/year)
    emissions['equivalent_trees'] = abs(emissions['net_emissions_kg']) / 21
    
    return emissions
