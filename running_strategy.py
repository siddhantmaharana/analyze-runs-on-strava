import pandas as pd
from datetime import datetime, timedelta

class RunningStrategy:
    def __init__(self, analysis, race_date, race_distance):
        self.analysis = analysis
        self.race_date = pd.to_datetime(race_date)
        self.race_distance = race_distance
        self.current_date = pd.to_datetime(datetime.now().date())
        self.weeks_until_race = (self.race_date - self.current_date).days // 7
        self.current_weekly_mileage = self._calculate_current_weekly_mileage()

    def _calculate_current_weekly_mileage(self):
        recent_runs = self.analysis.df[self.analysis.df['date'] > (self.current_date - timedelta(days=28))]
        return recent_runs['distance'].sum() / 4  # Average over last 4 weeks

    def generate_plan(self):
        if self.race_distance == 13.1:  # Half Marathon
            return self._generate_half_marathon_plan()
        else:
            raise ValueError("Currently only half marathon plans are supported.")

    def _generate_half_marathon_plan(self):
        plan = []
        target_peak_mileage = min(self.current_weekly_mileage * 1.5, 50)  # Increase by 50% or cap at 50 miles
        weekly_mileage_increase = (target_peak_mileage - self.current_weekly_mileage) / (self.weeks_until_race - 3)  # Peak 3 weeks before race

        for week in range(1, self.weeks_until_race + 1):
            if week < self.weeks_until_race - 2:
                weekly_mileage = self.current_weekly_mileage + (weekly_mileage_increase * week)
            elif week == self.weeks_until_race - 2:
                weekly_mileage = target_peak_mileage
            elif week == self.weeks_until_race - 1:
                weekly_mileage = target_peak_mileage * 0.8  # 20% reduction for taper
            else:
                weekly_mileage = target_peak_mileage * 0.6  # 40% reduction for race week

            plan.append(self._generate_week_plan(week, weekly_mileage))

        return plan

    def _generate_week_plan(self, week_number, weekly_mileage):
        long_run_distance = weekly_mileage * 0.4  # 40% of weekly mileage for long run
        remaining_mileage = weekly_mileage - long_run_distance
        
        # Distribute remaining mileage across 1-2 other runs
        if weekly_mileage < 20:  # For lower mileage weeks, do 2 runs total
            midweek_run_distance = remaining_mileage
            week_plan = {
                "Week": week_number,
                "Total Mileage": round(weekly_mileage, 1),
                "Monday": "Rest",
                "Tuesday": "Rest",
                "Wednesday": f"{round(midweek_run_distance, 1)} miles with speed work",
                "Thursday": "Cross-training or rest",
                "Friday": "Rest",
                "Saturday": "Rest or cross-training",
                "Sunday": f"{round(long_run_distance, 1)} miles long run"
            }
        else:  # For higher mileage weeks, do 3 runs total
            midweek_run_distance = remaining_mileage / 2
            week_plan = {
                "Week": week_number,
                "Total Mileage": round(weekly_mileage, 1),
                "Monday": "Rest",
                "Tuesday": f"{round(midweek_run_distance, 1)} miles easy",
                "Wednesday": "Cross-training or rest",
                "Thursday": f"{round(midweek_run_distance, 1)} miles with speed work",
                "Friday": "Rest",
                "Saturday": "Rest or cross-training",
                "Sunday": f"{round(long_run_distance, 1)} miles long run"
            }

        return week_plan

    def get_strategy_insights(self):
        return {
            "current_weekly_mileage": round(self.current_weekly_mileage, 1),
            "weeks_until_race": self.weeks_until_race,
            "target_peak_mileage": round(min(self.current_weekly_mileage * 1.5, 50), 1),
            "suggested_weekly_increase": round((min(self.current_weekly_mileage * 1.5, 50) - self.current_weekly_mileage) / (self.weeks_until_race - 3), 1)
        }

# Usage example
# analysis = RunAnalysis('out_starting_2023.json')
# strategy = RunningStrategy(analysis, '2024-11-28', 13.1)
# plan = strategy.generate_plan()
# insights = strategy.get_strategy_insights()