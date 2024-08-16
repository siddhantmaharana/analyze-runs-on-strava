import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

class RunVisualizer:
    @staticmethod
    def save_plot(fig, filename):
        # Create 'plots' directory if it doesn't exist
        if not os.path.exists('plots'):
            os.makedirs('plots')
        fig.savefig(os.path.join('plots', filename))
        plt.close(fig)  # Close the figure to free up memory

    @staticmethod
    def plot_monthly_distance(aggregates):
        months = sorted(aggregates.keys())
        distances = [aggregates[m]['total_distance'] for m in months]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        x = range(len(months))
        ax.bar(x, distances)
        ax.set_title('Total Distance Run per Month')
        ax.set_xlabel('Month')
        ax.set_ylabel('Distance (miles)')
        ax.set_xticks(x)
        ax.set_xticklabels([f"{m[0]}-{m[1]:02d}" for m in months], rotation=45, ha='right')
        plt.tight_layout()
        RunVisualizer.save_plot(fig, 'monthly_distance.png')

    @staticmethod
    def plot_yearly_summary(aggregates):
        years = sorted(aggregates.keys())
        distances = [aggregates[y]['total_distance'] for y in years]
        times = [aggregates[y]['total_time'] / 60 for y in years]  # Convert to hours
        runs = [aggregates[y]['num_runs'] for y in years]

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15))
        
        ax1.bar(years, distances)
        ax1.set_title('Yearly Total Distance')
        ax1.set_ylabel('Distance (miles)')

        ax2.bar(years, times)
        ax2.set_title('Yearly Total Time')
        ax2.set_ylabel('Time (hours)')

        ax3.bar(years, runs)
        ax3.set_title('Number of Runs per Year')
        ax3.set_ylabel('Number of Runs')

        plt.tight_layout()
        RunVisualizer.save_plot(fig, 'yearly_summary.png')

    @staticmethod
    def plot_pace_comparison(comparison):
        years = sorted(comparison.keys())
        avg_paces = [comparison[y]['avg_pace'] for y in years]
        best_paces = [comparison[y]['best_pace'] for y in years]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(years, avg_paces, marker='o', label='Average Pace')
        ax.plot(years, best_paces, marker='s', label='Best Pace')
        ax.set_title('Pace Comparison Across Years')
        ax.set_xlabel('Year')
        ax.set_ylabel('Pace (minutes/mile)')
        ax.legend()
        ax.grid(True)
        plt.tight_layout()
        RunVisualizer.save_plot(fig, 'pace_comparison.png')

    @staticmethod
    def plot_monthly_run_count(aggregates):
        months = sorted(aggregates.keys())
        run_counts = [aggregates[m]['num_runs'] for m in months]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        x = range(len(months))
        ax.bar(x, run_counts)
        ax.set_title('Number of Runs per Month')
        ax.set_xlabel('Month')
        ax.set_ylabel('Number of Runs')
        ax.set_xticks(x)
        ax.set_xticklabels([f"{m[0]}-{m[1]:02d}" for m in months], rotation=45, ha='right')
        plt.tight_layout()
        RunVisualizer.save_plot(fig, 'monthly_run_count.png')