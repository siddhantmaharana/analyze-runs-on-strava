from run_analysis import RunAnalysis
from data_visualizer import DataVisualizer
from running_strategy import RunningStrategy

import pandas as pd

# Initialize the analysis
analysis = RunAnalysis('data/out_starting_2023.json')

# # Generate insights
# insights = analysis.generate_insights()
# analysis.save_insights_to_json('data/my_run_insights.json')

# # Initialize the visualizer
# visualizer = DataVisualizer()

# # Create various plots
# monthly_data = pd.DataFrame(analysis.aggregate_by_period('month'))
# visualizer.plot_time_series(monthly_data, 'month', 'distance', 'Monthly Distance', 'Month', 'Distance (miles)', 'monthly_distance.png')

# weekly_mileage = pd.DataFrame(analysis.weekly_mileage_trend()['weekly_mileage'])
# visualizer.plot_bar_chart(weekly_mileage, 'week', 'distance', 'Weekly Mileage', 'Week', 'Distance (miles)', 'weekly_mileage.png')

# visualizer.plot_scatter(analysis.df, 'elevation', 'pace', 'Elevation vs Pace', 'Elevation (ft)', 'Pace (min/mile)', 'elevation_vs_pace.png')

# distance_dist = pd.DataFrame.from_dict(analysis.distance_distribution(), orient='index', columns=['count']).reset_index()
# visualizer.plot_bar_chart(distance_dist, 'index', 'count', 'Run Distance Distribution', 'Distance Category', 'Number of Runs', 'distance_distribution.png')

# Generate a half marathon training plan
strategy = RunningStrategy(analysis, '2024-11-28', 13.1)
plan = strategy.generate_plan()
strategy_insights = strategy.get_strategy_insights()

# Print strategy insights
print("Training Strategy Insights:")
for key, value in strategy_insights.items():
    print(f"{key.replace('_', ' ').title()}: {value}")

# Print the training plan
print("\nTraining Plan:")
for week in plan:
    print(f"\nWeek {week['Week']} (Total: {week['Total Mileage']} miles)")
    for day, workout in week.items():
        if day not in ['Week', 'Total Mileage']:
            print(f"  {day}: {workout}")

# Optionally, save the plan to a CSV file
plan_df = pd.DataFrame(plan)
plan_df.to_csv('half_marathon_training_plan.csv', index=False)