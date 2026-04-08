"""
Visualization utilities for Smart Microgrid simulation
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional


def plot_energy_flows(model_data: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """
    Plot energy generation, consumption, and grid interaction over time
    
    Args:
        model_data: DataFrame with model-level data
        save_path: Optional path to save the figure
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Microgrid Energy Flows', fontsize=16, fontweight='bold')
    
    # Plot 1: Generation vs Consumption
    ax1 = axes[0, 0]
    ax1.plot(model_data.index, model_data['Total Generation'], 
             label='Solar Generation', color='orange', linewidth=2)
    ax1.plot(model_data.index, model_data['Total Consumption'], 
             label='Consumption', color='blue', linewidth=2)
    ax1.fill_between(model_data.index, model_data['Total Generation'], 
                      alpha=0.3, color='orange')
    ax1.set_xlabel('Hour')
    ax1.set_ylabel('Power (kW)')
    ax1.set_title('Generation vs Consumption')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Grid Interaction
    ax2 = axes[0, 1]
    ax2.plot(model_data.index, model_data['Grid Import'], 
             label='Grid Import', color='red', linewidth=2)
    ax2.plot(model_data.index, model_data['Grid Export'], 
             label='Grid Export', color='green', linewidth=2)
    ax2.set_xlabel('Hour')
    ax2.set_ylabel('Power (kW)')
    ax2.set_title('Grid Import/Export')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Battery Storage
    ax3 = axes[1, 0]
    ax3.plot(model_data.index, model_data['Total Battery Storage'], 
             color='purple', linewidth=2)
    ax3.fill_between(model_data.index, model_data['Total Battery Storage'], 
                      alpha=0.3, color='purple')
    ax3.set_xlabel('Hour')
    ax3.set_ylabel('Energy (kWh)')
    ax3.set_title('Total Battery Storage')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Self-Sufficiency Ratio
    ax4 = axes[1, 1]
    ax4.plot(model_data.index, model_data['Self Sufficiency'] * 100, 
             color='green', linewidth=2)
    ax4.axhline(y=100, color='gray', linestyle='--', alpha=0.5, label='100% Self-Sufficient')
    ax4.fill_between(model_data.index, model_data['Self Sufficiency'] * 100, 
                      alpha=0.3, color='green')
    ax4.set_xlabel('Hour')
    ax4.set_ylabel('Self-Sufficiency (%)')
    ax4.set_title('Community Self-Sufficiency')
    ax4.set_ylim([0, max(120, model_data['Self Sufficiency'].max() * 105)])
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_trading_analysis(model_data: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """
    Plot trading activity and price dynamics
    
    Args:
        model_data: DataFrame with model-level data
        save_path: Optional path to save the figure
    """
    fig, axes = plt.subplots(2, 1, figsize=(15, 8))
    fig.suptitle('Peer-to-Peer Trading Analysis', fontsize=16, fontweight='bold')
    
    # Plot 1: Number of trades over time
    ax1 = axes[0]
    ax1.bar(model_data.index, model_data['Total Trades'], color='steelblue', alpha=0.7)
    ax1.set_xlabel('Hour')
    ax1.set_ylabel('Number of Trades')
    ax1.set_title('Trading Activity Over Time')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Plot 2: Average energy price
    ax2 = axes[1]
    ax2.plot(model_data.index, model_data['Average Price'], 
             color='darkgreen', linewidth=2)
    ax2.fill_between(model_data.index, model_data['Average Price'], 
                      alpha=0.3, color='green')
    ax2.set_xlabel('Hour')
    ax2.set_ylabel('Price ($/kWh)')
    ax2.set_title('Average Energy Price')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_household_comparison(agent_data: pd.DataFrame, n_households: int = 5, 
                               save_path: Optional[str] = None) -> None:
    """
    Compare individual household behaviors
    
    Args:
        agent_data: DataFrame with agent-level data
        n_households: Number of households to display
        save_path: Optional path to save the figure
    """
    # Select random households
    unique_agents = agent_data['AgentID'].unique()
    selected_agents = np.random.choice(unique_agents, 
                                       size=min(n_households, len(unique_agents)), 
                                       replace=False)
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle(f'Individual Household Comparison (Sample of {n_households})', 
                 fontsize=16, fontweight='bold')
    
    colors = plt.cm.Set3(np.linspace(0, 1, n_households))
    
    # Plot 1: Solar Generation
    ax1 = axes[0, 0]
    for i, agent_id in enumerate(selected_agents):
        agent_subset = agent_data[agent_data['AgentID'] == agent_id]
        ax1.plot(agent_subset.index, agent_subset['Solar Generated'], 
                label=f'HH {agent_id}', color=colors[i], linewidth=1.5)
    ax1.set_xlabel('Hour')
    ax1.set_ylabel('Power (kW)')
    ax1.set_title('Solar Generation by Household')
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Energy Consumption
    ax2 = axes[0, 1]
    for i, agent_id in enumerate(selected_agents):
        agent_subset = agent_data[agent_data['AgentID'] == agent_id]
        ax2.plot(agent_subset.index, agent_subset['Energy Consumed'], 
                label=f'HH {agent_id}', color=colors[i], linewidth=1.5)
    ax2.set_xlabel('Hour')
    ax2.set_ylabel('Power (kW)')
    ax2.set_title('Energy Consumption by Household')
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Battery State of Charge
    ax3 = axes[1, 0]
    for i, agent_id in enumerate(selected_agents):
        agent_subset = agent_data[agent_data['AgentID'] == agent_id]
        ax3.plot(agent_subset.index, agent_subset['Battery SOC'], 
                label=f'HH {agent_id}', color=colors[i], linewidth=1.5)
    ax3.set_xlabel('Hour')
    ax3.set_ylabel('Energy (kWh)')
    ax3.set_title('Battery State of Charge')
    ax3.legend(fontsize=8)
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Net Revenue (Revenue - Cost)
    ax4 = axes[1, 1]
    for i, agent_id in enumerate(selected_agents):
        agent_subset = agent_data[agent_data['AgentID'] == agent_id]
        net_revenue = agent_subset['Revenue'] - agent_subset['Cost']
        ax4.plot(agent_subset.index, net_revenue.cumsum(), 
                label=f'HH {agent_id}', color=colors[i], linewidth=1.5)
    ax4.set_xlabel('Hour')
    ax4.set_ylabel('Cumulative Net Revenue ($)')
    ax4.set_title('Cumulative Net Revenue by Household')
    ax4.legend(fontsize=8)
    ax4.grid(True, alpha=0.3)
    ax4.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_load_duration_curve(model_data: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """
    Plot load duration curve showing peak vs base load
    
    Args:
        model_data: DataFrame with model-level data
        save_path: Optional path to save the figure
    """
    plt.figure(figsize=(10, 6))
    
    # Sort peak load in descending order
    sorted_loads = np.sort(model_data['Peak Load'].values)[::-1]
    
    plt.plot(range(len(sorted_loads)), sorted_loads, color='darkred', linewidth=2)
    plt.fill_between(range(len(sorted_loads)), sorted_loads, alpha=0.3, color='red')
    
    plt.xlabel('Hours (Sorted by Load)', fontsize=12)
    plt.ylabel('Peak Load (kW)', fontsize=12)
    plt.title('Load Duration Curve', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Add statistics
    mean_load = sorted_loads.mean()
    max_load = sorted_loads.max()
    plt.axhline(y=mean_load, color='blue', linestyle='--', 
                label=f'Mean Load: {mean_load:.2f} kW', alpha=0.7)
    plt.axhline(y=max_load, color='red', linestyle='--', 
                label=f'Peak Load: {max_load:.2f} kW', alpha=0.7)
    
    plt.legend()
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def generate_summary_statistics(model_data: pd.DataFrame, agent_data: pd.DataFrame) -> pd.DataFrame:
    """
    Generate summary statistics for the simulation
    
    Args:
        model_data: DataFrame with model-level data
        agent_data: DataFrame with agent-level data
        
    Returns:
        DataFrame with summary statistics
    """
    stats = {
        'Metric': [],
        'Value': [],
        'Unit': []
    }
    
    # Energy metrics
    total_generation = model_data['Total Generation'].sum()
    total_consumption = model_data['Total Consumption'].sum()
    total_grid_import = model_data['Grid Import'].sum()
    total_grid_export = model_data['Grid Export'].sum()
    
    stats['Metric'].extend([
        'Total Solar Generation',
        'Total Consumption',
        'Total Grid Import',
        'Total Grid Export',
        'Average Self-Sufficiency',
        'Peak Load',
        'Average Price'
    ])
    
    stats['Value'].extend([
        f"{total_generation:.2f}",
        f"{total_consumption:.2f}",
        f"{total_grid_import:.2f}",
        f"{total_grid_export:.2f}",
        f"{model_data['Self Sufficiency'].mean() * 100:.2f}",
        f"{model_data['Peak Load'].max():.2f}",
        f"{model_data['Average Price'].mean():.4f}"
    ])
    
    stats['Unit'].extend([
        'kWh',
        'kWh',
        'kWh',
        'kWh',
        '%',
        'kW',
        '$/kWh'
    ])
    
    # Trading metrics
    total_trades = model_data['Total Trades'].sum()
    
    stats['Metric'].append('Total P2P Trades')
    stats['Value'].append(f"{total_trades:.0f}")
    stats['Unit'].append('trades')
    
    # Economic metrics
    if not agent_data.empty:
        total_revenue = agent_data.groupby('AgentID')['Revenue'].sum().sum()
        total_cost = agent_data.groupby('AgentID')['Cost'].sum().sum()
        
        stats['Metric'].extend([
            'Total Community Revenue',
            'Total Community Cost',
            'Net Community Benefit'
        ])
        
        stats['Value'].extend([
            f"{total_revenue:.2f}",
            f"{total_cost:.2f}",
            f"{total_revenue - total_cost:.2f}"
        ])
        
        stats['Unit'].extend(['$', '$', '$'])
    
    return pd.DataFrame(stats)


def create_comprehensive_report(model_data: pd.DataFrame, agent_data: pd.DataFrame, 
                                output_dir: str = './results') -> None:
    """
    Create a comprehensive analysis report with all visualizations
    
    Args:
        model_data: DataFrame with model-level data
        agent_data: DataFrame with agent-level data
        output_dir: Directory to save outputs
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating comprehensive microgrid analysis report...")
    
    # Generate all plots
    print("  → Creating energy flow plots...")
    plot_energy_flows(model_data, save_path=f'{output_dir}/energy_flows.png')
    
    print("  → Creating trading analysis...")
    plot_trading_analysis(model_data, save_path=f'{output_dir}/trading_analysis.png')
    
    print("  → Creating household comparison...")
    plot_household_comparison(agent_data, n_households=5, 
                              save_path=f'{output_dir}/household_comparison.png')
    
    print("  → Creating load duration curve...")
    plot_load_duration_curve(model_data, save_path=f'{output_dir}/load_duration_curve.png')
    
    # Generate summary statistics
    print("  → Generating summary statistics...")
    summary_stats = generate_summary_statistics(model_data, agent_data)
    summary_stats.to_csv(f'{output_dir}/summary_statistics.csv', index=False)
    
    # Save raw data
    print("  → Saving raw data...")
    model_data.to_csv(f'{output_dir}/model_data.csv')
    agent_data.to_csv(f'{output_dir}/agent_data.csv')
    
    print(f"\n✓ Report generated successfully in '{output_dir}/' directory")
    print("\nSummary Statistics:")
    print(summary_stats.to_string(index=False))
