# Smart Microgrid Energy Trading Network

An agent-based model simulating a community microgrid where households act as autonomous agents that generate (solar panels), consume, and trade electricity with each other in real-time.

## 🎯 Project Overview

This project bridges **Electrical Engineering** and **Agent-Based Modeling** by simulating:
- Solar power generation with realistic PV characteristics
- Battery energy storage systems
- Peer-to-peer energy trading between households
- Grid stability and power flow analysis
- Economic optimization through trading strategies

## 🏗️ Project Structure

```
smart_microgrid/
├── agents/
│   └── household.py          # Household agent with solar, battery, trading
├── models/
│   └── microgrid.py          # Main microgrid simulation model
├── utils/
│   ├── visualization.py      # Plotting and visualization tools
│   └── electrical_analysis.py # EE metrics and analysis
├── run_simulation.py         # Main simulation runner
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🔧 Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Verify installation:**
```bash
python -c "import mesa; import numpy; import pandas; print('All dependencies installed!')"
```

## 🚀 Quick Start

Run the simulation with default parameters:

```bash
cd smart_microgrid
python run_simulation.py
```

This will:
- Create a microgrid with 20 households
- Simulate 1 week (168 hours) of operation
- Generate comprehensive analysis reports
- Save results to `./results/` directory

## 📊 What Gets Generated

The simulation produces:

### Visualizations
- **energy_flows.png** - Generation vs consumption, grid interaction, battery storage, self-sufficiency
- **trading_analysis.png** - P2P trading activity and price dynamics
- **household_comparison.png** - Individual household behaviors
- **load_duration_curve.png** - Peak vs base load analysis

### Data Files
- **summary_statistics.csv** - High-level simulation metrics
- **electrical_metrics.csv** - Grid stability and EE performance
- **emission_savings.csv** - Environmental impact metrics
- **model_data.csv** - Timestep-by-timestep model data
- **agent_data.csv** - Individual household data

## 🔬 Key Features

### Electrical Engineering Components

1. **Solar Generation Model**
   - PV panel efficiency (18-20%)
   - Temperature derating coefficients
   - Irradiance-based power calculation
   - Time-of-day solar patterns

2. **Battery Storage System**
   - State of charge (SOC) management
   - Charge/discharge rate limits (0.5C)
   - Round-trip efficiency (95%)
   - Capacity constraints

3. **Power Flow Analysis**
   - Load balancing
   - Grid import/export tracking
   - Distribution losses
   - Peak load analysis

### Agent-Based Modeling Components

1. **Autonomous Agents**
   - Individual consumption patterns
   - Varying solar capacities (0-8 kW)
   - Different battery sizes (0-15 kWh)
   - Strategic trading behavior

2. **Trading Strategies**
   - **Profit-maximizing**: Sell high, buy low
   - **Community-oriented**: Fair pricing
   - **Conservative**: Stable pricing

3. **Emergent Behaviors**
   - Market price formation
   - Peer-to-peer trading networks
   - Self-organization of energy flows
   - Community resilience patterns

## 📈 Customization

Edit `run_simulation.py` to modify parameters:

```python
model, model_data, agent_data = run_simulation(
    n_households=30,           # Number of households
    simulation_hours=336,      # 2 weeks instead of 1
    solar_penetration=0.9,     # 90% with solar
    battery_penetration=0.7,   # 70% with batteries
    output_dir='./custom_results',
    seed=123                   # For reproducibility
)
```

## 🎓 Educational Value

This project demonstrates:

### Electrical Engineering Concepts
- Renewable energy integration
- Energy storage systems
- Power system stability
- Load factor and capacity factor
- Distribution grid dynamics

### Agent-Based Modeling Concepts
- Multi-agent systems
- Emergent behavior
- Market mechanisms
- Distributed decision-making
- Complex adaptive systems

### Interdisciplinary Insights
- How physical constraints affect agent behavior
- Economic optimization under engineering constraints
- Grid stability through decentralized control
- Real-world smart grid challenges

## 📊 Example Metrics

After running the simulation, you'll see metrics like:

```
Energy Flows:
  • Total Solar Generation: 1,234.56 kWh
  • Total Consumption: 2,345.67 kWh
  • Grid Import: 567.89 kWh
  • Grid Export: 123.45 kWh
  • Average Self-Sufficiency: 52.6%

Trading Activity:
  • Total P2P Trades: 234
  • Average Trades per Hour: 1.4

Environmental Impact:
  • Net CO2 Emissions: 123.45 kg
  • Equivalent to 5.9 trees/year
```

## 🔬 Advanced Analysis

You can access the raw data for custom analysis:

```python
import pandas as pd

# Load data
model_data = pd.read_csv('./results/model_data.csv')
agent_data = pd.read_csv('./results/agent_data.csv')

# Custom analysis
peak_hours = model_data[model_data['Peak Load'] > model_data['Peak Load'].quantile(0.9)]
print(f"Peak hours: {len(peak_hours)}")
```

## 🛠️ Extension Ideas

1. **Add Electric Vehicles** - Mobile storage agents
2. **Weather Variability** - Cloud cover, seasonal changes
3. **Grid Faults** - Resilience testing
4. **Time-of-Use Pricing** - Dynamic grid tariffs
5. **Predictive Algorithms** - ML-based trading strategies
6. **Network Topology** - Geographic constraints
7. **Renewable Mix** - Add wind turbines
8. **Demand Response** - Flexible load management

## 📚 Technical Details

### Household Agent Attributes
- `solar_capacity`: 0-8 kW peak
- `battery_capacity`: 0-15 kWh
- `consumption_profile`: residential/high/low
- `trading_strategy`: profit/community/conservative

### Simulation Time Step
- Each step = 1 hour
- Hourly solar irradiance calculation
- Time-of-day consumption patterns
- Battery state updated each step

### Trading Mechanism
- Peer-to-peer bilateral trading
- Price negotiation based on strategy
- Energy amount limited by availability
- Transaction cost tracking

## 🤝 Contributing

Feel free to:
- Add new agent strategies
- Implement additional EE metrics
- Create new visualization types
- Optimize performance
- Add documentation

## 📖 References

This simulation is based on concepts from:
- Smart grid and microgrid literature
- Agent-based modeling frameworks (Mesa)
- Power systems engineering
- Energy economics

## 📝 License

This is an educational project. Feel free to use and modify for learning purposes.

## 🙋 Questions?

This project demonstrates:
- How to combine domain-specific knowledge (EE) with ABM
- Building realistic simulations with Mesa
- Analyzing complex systems with emergent behavior
- Visualizing multi-dimensional time-series data

Perfect for students, researchers, or anyone interested in smart grids and agent-based modeling!

---

**Created as an educational example of interdisciplinary simulation combining Electrical Engineering and Agent-Based Modeling.**
