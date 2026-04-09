"""
Smart Microgrid Model
Main simulation model managing the microgrid network
"""

import numpy as np
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from typing import List, Dict
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.household import HouseholdAgent


class MicrogridModel(Model):
    """
    A model representing a smart microgrid with multiple households
    """
    
    def __init__(
        self,
        n_households: int = 20,
        solar_penetration: float = 0.7,  # Percentage with solar
        battery_penetration: float = 0.5,  # Percentage with batteries
        seed: int = None
    ):
        super().__init__()
        
        if seed is not None:
            np.random.seed(seed)
        
        self.n_households = n_households
        self.schedule = RandomActivation(self)
        
        # Time tracking
        self.current_hour = 0
        self.current_day = 0
        self.day_type = "weekday"
        
        # Grid parameters
        self.grid_voltage = 230  # Volts
        self.grid_frequency = 50  # Hz
        self.distribution_loss_rate = 0.05  # 5% loss per km
        
        # Market parameters
        self.average_price = 0.15  # $/kWh
        
        # Create households
        self._create_households(solar_penetration, battery_penetration)
        
        # Data collection
        self.datacollector = DataCollector(
            model_reporters={
                "Total Generation": self.get_total_generation,
                "Total Consumption": self.get_total_consumption,
                "Total Battery Storage": self.get_total_battery_storage,
                "Grid Import": self.get_total_grid_import,
                "Grid Export": self.get_total_grid_export,
                "Average Price": self.get_average_price,
                "Total Trades": self.get_total_trades,
                "Self Sufficiency": self.get_self_sufficiency,
                "Peak Load": self.get_peak_load,
            },
            agent_reporters={
                "Solar Generated": "solar_generated",
                "Energy Consumed": "energy_consumed",
                "Battery SOC": "battery_soc",
                "Energy Price": "energy_price",
                "Revenue": "revenue",
                "Cost": "cost",
            }
        )
        
    def _create_households(self, solar_penetration: float, battery_penetration: float) -> None:
        """Create household agents with varying characteristics"""
        
        for i in range(self.n_households):
            # Determine if household has solar
            has_solar = np.random.random() < solar_penetration
            solar_capacity = np.random.uniform(3.0, 8.0) if has_solar else 0.0
            
            # Determine if household has battery
            has_battery = np.random.random() < battery_penetration
            battery_capacity = np.random.uniform(5.0, 15.0) if has_battery else 0.0
            
            # Consumption profile
            profile_type = np.random.choice(
                ["residential", "high_consumption", "low_consumption"],
                p=[0.7, 0.15, 0.15]
            )
            
            # Trading strategy
            strategy = np.random.choice(
                ["profit_maximizing", "community_oriented", "conservative"],
                p=[0.4, 0.4, 0.2]
            )
            
            household = HouseholdAgent(
                unique_id=i,
                model=self,
                solar_capacity=solar_capacity,
                battery_capacity=battery_capacity,
                consumption_profile=profile_type,
                trading_strategy=strategy
            )
            
            self.schedule.add(household)
    
    def get_solar_irradiance(self, hour: int) -> float:
        """
        Calculate solar irradiance based on hour of day
        
        Args:
            hour: Hour of day (0-23)
            
        Returns:
            Irradiance in W/m²
        """
        # Simple model: sine wave between sunrise and sunset
        if hour < 6 or hour > 18:
            return 0.0
        
        # Peak irradiance at solar noon (12:00)
        # Max irradiance ~1000 W/m² on clear day
        peak_irradiance = 1000
        solar_hour = hour - 6  # Hours since sunrise
        
        # Sine curve for irradiance
        irradiance = peak_irradiance * np.sin((solar_hour / 12) * np.pi)
        
        # Add some randomness for clouds (±20%)
        cloud_factor = np.random.uniform(0.8, 1.0)
        
        return max(0, irradiance * cloud_factor)
    
    def get_nearby_households(self, agent: HouseholdAgent, max_neighbors: int = 5) -> List[HouseholdAgent]:
        """
        Get nearby households for potential trading
        
        Args:
            agent: The household agent
            max_neighbors: Maximum number of neighbors to return
            
        Returns:
            List of nearby household agents
        """
        all_agents = list(self.schedule.agents)
        all_agents.remove(agent)
        
        # For simplicity, return random subset (could implement actual geography)
        n_neighbors = min(max_neighbors, len(all_agents))
        return np.random.choice(all_agents, size=n_neighbors, replace=False).tolist()
    
    def get_average_price(self) -> float:
        """Calculate average energy price across all households"""
        prices = [agent.energy_price for agent in self.schedule.agents]
        return np.mean(prices) if prices else self.average_price
    
    def get_total_generation(self) -> float:
        """Total solar generation across all households"""
        return sum(agent.solar_generated for agent in self.schedule.agents)
    
    def get_total_consumption(self) -> float:
        """Total energy consumption across all households"""
        return sum(agent.energy_consumed for agent in self.schedule.agents)
    
    def get_total_battery_storage(self) -> float:
        """Total energy stored in all batteries"""
        return sum(agent.battery_soc for agent in self.schedule.agents)
    
    def get_total_grid_import(self) -> float:
        """Total power imported from main grid"""
        return sum(agent.grid_import for agent in self.schedule.agents)
    
    def get_total_grid_export(self) -> float:
        """Total power exported to main grid"""
        return sum(agent.grid_export for agent in self.schedule.agents)
    
    def get_total_trades(self) -> int:
        """Total number of peer-to-peer trades"""
        return sum(len(agent.trades_made) for agent in self.schedule.agents) // 2  # Divide by 2 to avoid double counting
    
    def get_self_sufficiency(self) -> float:
        """
        Calculate community self-sufficiency ratio
        (Generation + Battery discharge) / Consumption
        """
        consumption = self.get_total_consumption()
        generation = self.get_total_generation()
        
        if consumption == 0:
            return 0.0
        
        return min(1.0, generation / consumption)
    
    def get_peak_load(self) -> float:
        """Get peak load on the distribution system"""
        net_loads = []
        for agent in self.schedule.agents:
            net_load = agent.energy_consumed - agent.solar_generated
            net_loads.append(max(0, net_load))
        return sum(net_loads)
    
    def step(self) -> None:
        """Advance the model by one step (1 hour)"""
        
        # Reset agent variables for this step
        for agent in self.schedule.agents:
            agent.solar_generated = 0
            agent.energy_consumed = 0
            agent.energy_bought = 0
            agent.energy_sold = 0
            agent.grid_import = 0
            agent.grid_export = 0
            agent.trades_made = []
        
        # Execute agent steps
        self.schedule.step()
        
        # Collect data
        self.datacollector.collect(self)
        
        # Update time
        self.current_hour += 1
        if self.current_hour >= 24:
            self.current_hour = 0
            self.current_day += 1
            
            # Update day type (simple 5 weekdays, 2 weekend pattern)
            self.day_type = "weekend" if self.current_day % 7 >= 5 else "weekday"
    
    def run_simulation(self, hours: int = 168) -> None:
        """
        Run the simulation for a specified number of hours
        
        Args:
            hours: Number of hours to simulate (default: 168 = 1 week)
        """
        for _ in range(hours):
            self.step()
