from run_analysis import RunAnalysis
from data_visualizer import DataVisualizer

import pandas as pd

# Initialize the analysis
analysis = RunAnalysis('data/out_starting_2023.json')

# Generate insights
insights = analysis.generate_insights()
analysis.save_insights_to_json('data/my_run_insights.json')

# Initialize the visualizer
visualizer = DataVisualizer()

# Create various plots
monthly_data = pd.DataFrame(analysis.aggregate_by_period('month'))
visualizer.plot_time_series(monthly_data, 'month', 'distance', 'Monthly Distance', 'Month', 'Distance (miles)', 'monthly_distance.png')

weekly_mileage = pd.DataFrame(analysis.weekly_mileage_trend()['weekly_mileage'])
visualizer.plot_bar_chart(weekly_mileage, 'week', 'distance', 'Weekly Mileage', 'Week', 'Distance (miles)', 'weekly_mileage.png')

distance_dist = pd.DataFrame.from_dict(analysis.distance_distribution(), orient='index', columns=['count']).reset_index()
visualizer.plot_bar_chart(distance_dist, 'index', 'count', 'Run Distance Distribution', 'Distance Category', 'Number of Runs', 'distance_distribution.png')
