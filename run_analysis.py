import json
import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime, timedelta

class RunAnalysis:
	def __init__(self, data_source):
		self.df = self._load_data(data_source)
		self._preprocess_data()

	def _load_data(self, data_source):
		if isinstance(data_source, str):
			with open(data_source, 'r') as file:
				data = json.load(file)
		elif isinstance(data_source, list):
			data = data_source
		else:
			raise ValueError("Data source must be a file path or a list of dictionaries")
		return pd.DataFrame(data)

	def _preprocess_data(self):
		self.df['date'] = pd.to_datetime(self.df['date'])
		self.df['pace'] = self.df['time'].apply(self._time_to_minutes) / self.df['distance']
		self.df['week'] = self.df['date'].dt.to_period('W')
		self.df['month'] = self.df['date'].dt.to_period('M')
		self.df['year'] = self.df['date'].dt.year

	@staticmethod
	def _time_to_minutes(time_str):
		if 's' in time_str:
			return float(time_str.rstrip('s')) / 60
		parts = time_str.split(':')
		if len(parts) == 1:
			return float(parts[0])
		elif len(parts) == 2:
			return int(parts[0]) + int(parts[1]) / 60
		elif len(parts) == 3:
			return int(parts[0]) * 60 + int(parts[1]) + int(parts[2]) / 60

	def streak_analysis(self):
		self.df['days_since_last_run'] = self.df['date'].diff().dt.days
		streaks = self.df[self.df['days_since_last_run'] <= 1]
		current_streak = streaks[streaks['date'] >= streaks['date'].max() - pd.Timedelta(days=streaks['days_since_last_run'].iloc[-1])]
		
		longest_streak = streaks.groupby((streaks['days_since_last_run'] != 1).cumsum()).size().max()
		current_streak_length = len(current_streak)
		
		return {
			"longest_streak": int(longest_streak),
			"current_streak": int(current_streak_length)
		}

	def weekly_mileage_trend(self):
		weekly_mileage = self.df.groupby('week')['distance'].sum().reset_index()
		weekly_mileage['week'] = weekly_mileage['week'].astype(str)
		
		slope, intercept, r_value, p_value, std_err = stats.linregress(range(len(weekly_mileage)), weekly_mileage['distance'])
		
		trend = "increasing" if slope > 0 else "decreasing"
		strength = abs(r_value)
		
		return {
			"trend": trend,
			"strength": float(strength),
			"weekly_mileage": weekly_mileage.to_dict('records')
		}

	def pace_analysis(self):
		avg_pace = self.df['pace'].mean()
		best_pace = self.df['pace'].min()
		worst_pace = self.df['pace'].max()
		
		recent_runs = self.df.sort_values('date').tail(10)
		recent_avg_pace = recent_runs['pace'].mean()
		
		pace_improvement = (avg_pace - recent_avg_pace) / avg_pace * 100
		
		return {
			"average_pace": float(avg_pace),
			"best_pace": float(best_pace),
			"worst_pace": float(worst_pace),
			"recent_average_pace": float(recent_avg_pace),
			"pace_improvement": float(pace_improvement)
		}

	def distance_distribution(self):
		bins = [0, 3, 5, 10, float('inf')]
		labels = ['Short (0-3 miles)', 'Medium (3-5 miles)', 'Long (5-10 miles)', 'Very Long (10+ miles)']
		self.df['distance_category'] = pd.cut(self.df['distance'], bins=bins, labels=labels, include_lowest=True)
		distribution = self.df['distance_category'].value_counts().to_dict()
		return {k: int(v) for k, v in distribution.items()}

	def elevation_vs_pace_correlation(self):
		correlation = self.df['elevation'].corr(self.df['pace'])
		return float(correlation)

	def aggregate_by_period(self, period='month'):
			if period not in ['month', 'year']:
				raise ValueError("Period must be 'month' or 'year'")
			
			grouper = 'month' if period == 'month' else 'year'
			aggregates = self.df.groupby(grouper).agg({
				'distance': 'sum',
				'time': lambda x: sum(self._time_to_minutes(t) for t in x),
				'elevation': 'sum'
			}).reset_index()
			
			aggregates['avg_pace'] = aggregates['time'] / aggregates['distance']
			aggregates['num_runs'] = self.df.groupby(grouper).size().values
			
			if period == 'month':
				aggregates['month'] = aggregates['month'].astype(str)
			
			return aggregates.to_dict('records')

	def compare_performance(self, distance_range=(0, 5), title_keyword=None):
		mask = (self.df['distance'] >= distance_range[0]) & (self.df['distance'] <= distance_range[1])
		if title_keyword:
			mask &= self.df['title'].str.contains(title_keyword, case=False)
		
		filtered_df = self.df[mask]
		
		performance = filtered_df.groupby(filtered_df['date'].dt.year).agg({
			'pace': ['mean', 'median', 'min', 'count']
		})
		
		performance.columns = ['avg_pace', 'median_pace', 'best_pace', 'num_runs']
		return performance.reset_index().to_dict('records')

	def generate_insights(self):
		return {
			"streak_analysis": self.streak_analysis(),
			"weekly_mileage_trend": self.weekly_mileage_trend(),
			"pace_analysis": self.pace_analysis(),
			"distance_distribution": self.distance_distribution(),
			"elevation_pace_correlation": self.elevation_vs_pace_correlation()
		}

	def save_insights_to_json(self, filename='run_insights.json'):
		insights = self.generate_insights()
		
		def json_serializable(obj):
			if isinstance(obj, (np.int64, np.int32)):
				return int(obj)
			elif isinstance(obj, np.float64):
				return float(obj)
			elif isinstance(obj, pd.Period):
				return str(obj)
			raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

		with open(filename, 'w') as f:
			json.dump(insights, f, default=json_serializable, indent=4)
		
		print(f"Insights saved to {filename}")

# Usage example
# analysis = RunAnalysis('out_starting_2023.json')
# insights = analysis.generate_insights()
# analysis.save_insights_to_json('my_run_insights.json')