# Smart Microgrid Project - Getting Started Guide

## 🚀 Quick Start

1. **Navigate to the project directory:**
```bash
cd smart_microgrid
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Test the setup:**
```bash
python test_setup.py
```

4. **Run the full simulation:**
```bash
python run_simulation.py
```

## 📁 Project Files

### Core Components
- **agents/household.py** - Household agent with solar, battery, and trading logic
- **models/microgrid.py** - Main microgrid simulation model using Mesa
- **utils/visualization.py** - Plotting and visualization tools
- **utils/electrical_analysis.py** - Electrical engineering metrics

### Scripts
- **run_simulation.py** - Main simulation runner (START HERE)
- **test_setup.py** - Verify installation
- **advanced_examples.py** - Scenario comparison examples

### Documentation
- **README.md** - Complete project documentation
- **requirements.txt** - Python dependencies

## 🎯 What This Project Does

Simulates a community of 20 households over 1 week where:

### Electrical Engineering Features:
- ☀️ **Solar Generation**: Realistic PV modeling with temperature effects
- 🔋 **Battery Storage**: SOC management, charge/discharge limits
- ⚡ **Power Flows**: Grid import/export, load balancing
- 📊 **Stability Metrics**: Load factor, peak analysis, voltage drop

### Agent-Based Modeling Features:
- 🏠 **Autonomous Agents**: Each household makes independent decisions
- 💰 **Trading Strategies**: Profit-maximizing, community-oriented, conservative
- 🤝 **P2P Trading**: Households trade energy with neighbors
- 📈 **Emergent Behavior**: Market prices emerge from agent interactions

## 📊 Output Files

After running `run_simulation.py`, you'll get:

### Visualizations (in ./results/)
- energy_flows.png
- trading_analysis.png
- household_comparison.png
- load_duration_curve.png

### Data Files (in ./results/)
- summary_statistics.csv
- electrical_metrics.csv
- emission_savings.csv
- model_data.csv (full time series)
- agent_data.csv (individual household data)

## 🔧 Customization

Edit parameters in `run_simulation.py`:

```python
model, model_data, agent_data = run_simulation(
    n_households=30,           # More households
    simulation_hours=336,      # 2 weeks
    solar_penetration=0.9,     # 90% with solar
    battery_penetration=0.7,   # 70% with batteries
    seed=42                    # Random seed
)
```

## 💡 Key Insights You'll Discover

1. **Self-Sufficiency**: How much can a community meet its own energy needs?
2. **Trading Benefits**: Does P2P trading reduce grid dependency?
3. **Battery Value**: How do batteries improve stability?
4. **Price Dynamics**: How do trading strategies affect market prices?
5. **Peak Reduction**: Can distributed generation reduce peak loads?

## 🎓 Learning Objectives

### For Electrical Engineers:
- Integrate renewable generation into power systems
- Understand battery storage economics
- Analyze grid stability with DERs
- Calculate power system metrics

### For Computer Scientists:
- Build agent-based models with Mesa
- Implement autonomous decision-making
- Analyze emergent system behavior
- Visualize complex time-series data

### Interdisciplinary:
- How physical constraints shape agent behavior
- Economic optimization under engineering limits
- Decentralized vs centralized control
- Real-world smart grid challenges

## 🚀 Next Steps

1. **Run the basic simulation** to see how it works
2. **Explore the visualizations** to understand patterns
3. **Run advanced_examples.py** to compare scenarios
4. **Modify agent strategies** to test new ideas
5. **Add new features** - EVs, wind, demand response, etc.

## 📖 Further Reading

The code is heavily commented to explain:
- Solar PV power calculations
- Battery state-of-charge management
- Trading price negotiations
- Grid stability metrics
- Data collection and analysis

## 🤝 Troubleshooting

**Import errors?**
→ Run: `pip install -r requirements.txt`

**Plots not showing?**
→ Check if matplotlib backend is configured correctly

**Want faster simulation?**
→ Reduce `simulation_hours` or `n_households`

**Need help?**
→ All functions have detailed docstrings

## 🎨 Example Output

After running, you'll see:
```
SMART MICROGRID SIMULATION
============================================================

Configuration:
  • Households: 20
  • Simulation Duration: 168 hours (7.0 days)
  • Solar Penetration: 70%
  • Battery Penetration: 50%

[1/4] Initializing microgrid model...
  ✓ Created 20 households
    - 14 with solar panels (70.0%)
    - 10 with batteries (50.0%)

[2/4] Running simulation for 168 hours...
  → Day 1 complete
  → Day 2 complete
  ...

[3/4] Extracting and processing data...
  ✓ Collected 168 timesteps of data

[4/4] Generating analysis reports...
  ✓ Report generated successfully

📊 KEY RESULTS:
Energy Flows:
  • Total Solar Generation: 1,234.56 kWh
  • Average Self-Sufficiency: 52.6%
```

---

**Start exploring: `python run_simulation.py`** 🚀
