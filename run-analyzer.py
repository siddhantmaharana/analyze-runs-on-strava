import json
from datetime import datetime
from collections import defaultdict
import statistics
from run_visualizer import RunVisualizer
import os
import sys

class RunAnalyzer:
    def __init__(self, json_file):
        with open(json_file, 'r') as file:
            self.data = json.load(file)
        self.parse_dates()
        self.visualizer = RunVisualizer()

    def parse_dates(self):
        for run in self.data:
            run['date'] = datetime.strptime(run['date'], "%Y-%m-%d")

    def aggregate_by_period(self, period='month'):
        aggregates = defaultdict(lambda: defaultdict(list))
        for run in self.data:
            if period == 'month':
                key = (run['date'].year, run['date'].month)
            elif period == 'year':
                key = run['date'].year
            else:
                raise ValueError("Period must be 'month' or 'year'")
            
            aggregates[key]['distance'].append(run['distance'])
            aggregates[key]['time'].append(self.time_to_minutes(run['time']))
            aggregates[key]['elevation'].append(run['elevation'])

        results = {}
        for key, values in aggregates.items():
            results[key] = {
                'total_distance': sum(values['distance']),
                'total_time': sum(values['time']),
                'total_elevation': sum(values['elevation']),
                'avg_pace': sum(values['time']) / sum(values['distance']) if sum(values['distance']) > 0 else 0,
                'num_runs': len(values['distance'])
            }
        return results

    def compare_performance(self, distance_range=(0, 5), title_keyword=None):
        filtered_runs = [run for run in self.data 
                         if distance_range[0] <= run['distance'] <= distance_range[1]
                         and (title_keyword is None or title_keyword.lower() in run['title'].lower())]
        
        runs_by_year = defaultdict(list)
        for run in filtered_runs:
            runs_by_year[run['date'].year].append(run)

        results = {}
        for year, runs in runs_by_year.items():
            paces = [self.time_to_minutes(run['time']) / run['distance'] for run in runs if run['distance'] > 0]
            if paces:
                results[year] = {
                    'avg_pace': statistics.mean(paces),
                    'median_pace': statistics.median(paces),
                    'best_pace': min(paces),
                    'num_runs': len(runs)
                }
            else:
                results[year] = {
                    'avg_pace': 0,
                    'median_pace': 0,
                    'best_pace': 0,
                    'num_runs': len(runs)
                }
        return results

    @staticmethod
    def time_to_minutes(time_str):
        if 's' in time_str:  # Handle seconds format
            return float(time_str.rstrip('s')) / 60
        parts = time_str.split(':')
        if len(parts) == 1:  # Handle minutes only
            return float(parts[0])
        elif len(parts) == 2:
            return int(parts[0]) + int(parts[1]) / 60
        elif len(parts) == 3:
            return int(parts[0]) * 60 + int(parts[1]) + int(parts[2]) / 60
        else:
            raise ValueError(f"Invalid time format: {time_str}")

    @staticmethod
    def minutes_to_time_str(minutes):
        hours, minutes = divmod(minutes, 60)
        minutes, seconds = divmod(minutes * 60, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

    def generate_visualizations(self):
        print("Generating visualizations...")
        
        self.visualizer.plot_monthly_distance(self.aggregate_by_period('month'))
        print("Monthly distance plot saved as 'monthly_distance.png'")
        
        self.visualizer.plot_yearly_summary(self.aggregate_by_period('year'))
        print("Yearly summary plot saved as 'yearly_summary.png'")
        
        self.visualizer.plot_pace_comparison(self.compare_performance(distance_range=(3, 3.5)))
        print("Pace comparison plot saved as 'pace_comparison.png'")
        
        self.visualizer.plot_monthly_run_count(self.aggregate_by_period('month'))
        print("Monthly run count plot saved as 'monthly_run_count.png'")
        
        print(f"All plots have been saved in the 'plots' directory: {os.path.abspath('plots')}")

# Usage example
if __name__ == "__main__":
    input_file = sys.argv[1]
    analyzer = RunAnalyzer(input_file)
    analyzer.generate_visualizations()