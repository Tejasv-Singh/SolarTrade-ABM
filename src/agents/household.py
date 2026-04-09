"""
Household Agent for Smart Microgrid Simulation
Each household can generate solar power, consume electricity, store energy, and trade with neighbors
"""

import numpy as np
from mesa import Agent
from typing import Dict, List, Tuple


class HouseholdAgent(Agent):
    """
    A household agent with:
    - Solar generation capability
    - Energy consumption patterns
    - Battery storage system
    - Trading strategy
    """
    
    def __init__(
        self, 
        unique_id: int, 
        model,
        solar_capacity: float = 5.0,  # kW
        battery_capacity: float = 10.0,  # kWh
        consumption_profile: str = "residential",
        trading_strategy: str = "profit_maximizing"
    ):
        super().__init__(unique_id, model)
        
        # Physical characteristics
        self.solar_capacity = solar_capacity  # kW peak capacity
        self.battery_capacity = battery_capacity  # kWh
        self.battery_soc = battery_capacity * 0.5  # Start at 50% state of charge
        self.battery_efficiency = 0.95  # Round-trip efficiency
        self.battery_max_charge_rate = battery_capacity * 0.5  # 0.5C rate
        self.battery_max_discharge_rate = battery_capacity * 0.5
        
        # Consumption profile
        self.consumption_profile = consumption_profile
        self.base_consumption = self._get_base_consumption()
        
        # Trading parameters
        self.trading_strategy = trading_strategy
        self.energy_price = 0.15  # $/kWh initial price
        self.min_price = 0.05
        self.max_price = 0.30
        
        # Tracking variables
        self.solar_generated = 0
        self.energy_consumed = 0
        self.energy_bought = 0
        self.energy_sold = 0
        self.grid_import = 0
        self.grid_export = 0
        self.revenue = 0
        self.cost = 0
        self.trades_made = []
        
    def _get_base_consumption(self) -> float:
        """Get base consumption based on household type"""
        profiles = {
            "residential": np.random.uniform(0.8, 1.5),  # kW average
            "high_consumption": np.random.uniform(2.0, 3.5),
            "low_consumption": np.random.uniform(0.4, 0.8)
        }
        return profiles.get(self.consumption_profile, 1.0)
    
    def calculate_solar_generation(self, hour: int, irradiance: float) -> float:
        """
        Calculate solar power generation based on time and irradiance
        
        Args:
            hour: Hour of day (0-23)
            irradiance: Solar irradiance in W/m² (0-1000)
            
        Returns:
            Power generated in kW
        """
        # Solar panel efficiency (typical 18-20%)
        efficiency = 0.19
        
        # Temperature derating (assume 25°C nominal, 0.4%/°C loss)
        temperature = 25 + 10 * np.sin((hour - 6) * np.pi / 12)  # Simple temp model
        temp_coefficient = -0.004
        temp_factor = 1 + temp_coefficient * (temperature - 25)
        
        # Power calculation: P = Area * Efficiency * Irradiance * temp_factor
        # Assuming 15 m² per kW of capacity
        area = self.solar_capacity * 15 / 5  # m²
        power = (area * efficiency * irradiance / 1000) * temp_factor
        
        return max(0, min(power, self.solar_capacity))
    
    def calculate_consumption(self, hour: int, day_type: str = "weekday") -> float:
        """
        Calculate energy consumption based on time of day
        
        Args:
            hour: Hour of day (0-23)
            day_type: "weekday" or "weekend"
            
        Returns:
            Power consumption in kW
        """
        # Create realistic consumption pattern
        if day_type == "weekday":
            # Morning peak (6-9), Evening peak (17-22)
            pattern = np.array([
                0.3, 0.3, 0.3, 0.3, 0.4, 0.6,  # 0-5: Night/Early morning
                0.9, 1.2, 1.0, 0.7, 0.6, 0.6,  # 6-11: Morning peak then midday
                0.6, 0.6, 0.7, 0.7, 0.8, 1.1,  # 12-17: Afternoon rise
                1.4, 1.3, 1.2, 1.0, 0.7, 0.4   # 18-23: Evening peak
            ])
        else:
            # More distributed on weekends
            pattern = np.array([
                0.4, 0.3, 0.3, 0.3, 0.3, 0.4,
                0.5, 0.7, 0.9, 1.0, 1.1, 1.2,
                1.2, 1.1, 1.0, 1.0, 1.0, 1.1,
                1.3, 1.2, 1.1, 0.9, 0.6, 0.4
            ])
        
        # Add random variation (±15%)
        variation = np.random.uniform(0.85, 1.15)
        
        return self.base_consumption * pattern[hour] * variation
    
    def manage_battery(self, net_power: float, timestep: float = 1.0) -> float:
        """
        Manage battery charging/discharging
        
        Args:
            net_power: Net power available (positive = excess, negative = deficit) in kW
            timestep: Time step in hours
            
        Returns:
            Power still needed from/to grid after battery management (kW)
        """
        energy = net_power * timestep  # kWh
        
        if energy > 0:  # Excess energy - charge battery
            max_charge = min(
                self.battery_max_charge_rate * timestep,
                self.battery_capacity - self.battery_soc
            )
            charge_amount = min(energy * self.battery_efficiency, max_charge)
            self.battery_soc += charge_amount
            remaining_energy = energy - (charge_amount / self.battery_efficiency)
            return remaining_energy / timestep  # Return excess power
            
        else:  # Energy deficit - discharge battery
            max_discharge = min(
                self.battery_max_discharge_rate * timestep,
                self.battery_soc
            )
            discharge_amount = min(abs(energy) / self.battery_efficiency, max_discharge)
            self.battery_soc -= discharge_amount
            remaining_deficit = energy + (discharge_amount * self.battery_efficiency)
            return remaining_deficit / timestep  # Return remaining deficit
    
    def set_trading_price(self, net_power: float, market_avg_price: float) -> None:
        """
        Set energy price based on trading strategy and current situation
        
        Args:
            net_power: Current net power position (kW)
            market_avg_price: Average market price
        """
        if self.trading_strategy == "profit_maximizing":
            # Sell high when in surplus, buy low when in deficit
            if net_power > 0:  # Surplus - selling
                self.energy_price = min(
                    market_avg_price * 1.2,
                    self.max_price
                )
            else:  # Deficit - buying
                self.energy_price = max(
                    market_avg_price * 0.8,
                    self.min_price
                )
                
        elif self.trading_strategy == "community_oriented":
            # Price close to market average, slight preference for community
            self.energy_price = market_avg_price
            
        elif self.trading_strategy == "conservative":
            # Keep prices stable
            self.energy_price = np.clip(
                self.energy_price,
                self.min_price,
                self.max_price
            )
    
    def attempt_trade(self, other_agent: 'HouseholdAgent', amount: float) -> bool:
        """
        Attempt to trade energy with another household
        
        Args:
            other_agent: The other household to trade with
            amount: Amount of energy to trade in kWh (positive = buying, negative = selling)
            
        Returns:
            True if trade successful
        """
        if amount > 0:  # This agent is buying
            seller = other_agent
            buyer = self
            price = seller.energy_price
        else:  # This agent is selling
            seller = self
            buyer = other_agent
            price = buyer.energy_price
            amount = abs(amount)
        
        # Check if trade makes sense
        if price < self.min_price or price > self.max_price:
            return False
        
        # Execute trade
        cost = amount * price
        seller.energy_sold += amount
        seller.revenue += cost
        buyer.energy_bought += amount
        buyer.cost += cost
        
        # Record trade
        trade_record = {
            'buyer_id': buyer.unique_id,
            'seller_id': seller.unique_id,
            'amount': amount,
            'price': price,
            'step': self.model.schedule.steps
        }
        self.trades_made.append(trade_record)
        other_agent.trades_made.append(trade_record)
        
        return True
    
    def step(self) -> None:
        """
        Execute one step of the agent's behavior
        """
        # Get current time
        hour = self.model.current_hour
        day_type = self.model.day_type
        
        # Calculate solar generation
        irradiance = self.model.get_solar_irradiance(hour)
        self.solar_generated = self.calculate_solar_generation(hour, irradiance)
        
        # Calculate consumption
        self.energy_consumed = self.calculate_consumption(hour, day_type)
        
        # Calculate net power
        net_power = self.solar_generated - self.energy_consumed
        
        # Manage battery
        grid_power = self.manage_battery(net_power, timestep=1.0)
        
        # Set trading price based on market conditions
        market_avg = self.model.get_average_price()
        self.set_trading_price(grid_power, market_avg)
        
        # Try to trade with neighbors if needed
        if abs(grid_power) > 0.1:  # Only trade if significant power needed/available
            neighbors = self.model.get_nearby_households(self)
            for neighbor in neighbors:
                # Calculate neighbor's net position
                neighbor_net = (neighbor.solar_generated - neighbor.energy_consumed)
                
                # If opposite needs, try to trade
                if (grid_power > 0 and neighbor_net < 0) or (grid_power < 0 and neighbor_net > 0):
                    trade_amount = min(abs(grid_power), abs(neighbor_net)) * 0.5
                    if grid_power < 0:
                        trade_amount = -trade_amount
                    
                    if self.attempt_trade(neighbor, trade_amount):
                        grid_power += trade_amount  # Reduce grid dependency
                        break
        
        # Remaining power from/to main grid
        if grid_power > 0:
            self.grid_export = grid_power
            self.revenue += grid_power * 0.08  # Lower feed-in tariff
        elif grid_power < 0:
            self.grid_import = abs(grid_power)
            self.cost += abs(grid_power) * 0.20  # Higher grid purchase price
