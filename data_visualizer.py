import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class DataVisualizer:
    def __init__(self):
        self.plt = plt
        self.sns = sns
        sns.set_style("whitegrid")

    def save_plot(self, filename):
        self.plt.savefig(filename)
        self.plt.close()

    def plot_time_series(self, data, x, y, title, xlabel, ylabel, filename):
        plt.figure(figsize=(12, 6))
        plt.plot(data[x], data[y])
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=45)
        plt.tight_layout()
        self.save_plot(filename)

    def plot_bar_chart(self, data, x, y, title, xlabel, ylabel, filename):
        plt.figure(figsize=(12, 6))
        plt.bar(data[x], data[y])
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=45)
        plt.tight_layout()
        self.save_plot(filename)

    def plot_scatter(self, data, x, y, title, xlabel, ylabel, filename):
        plt.figure(figsize=(10, 6))
        plt.scatter(data[x], data[y])
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()
        self.save_plot(filename)

    def plot_heatmap(self, data, title, filename):
        plt.figure(figsize=(12, 10))
        sns.heatmap(data, annot=True, cmap='YlGnBu')
        plt.title(title)
        plt.tight_layout()
        self.save_plot(filename)

    def plot_distribution(self, data, column, title, xlabel, ylabel, filename):
        plt.figure(figsize=(10, 6))
        sns.histplot(data=data, x=column, kde=True)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()
        self.save_plot(filename)

# Usage example
# visualizer = DataVisualizer()
# df = pd.DataFrame(analysis.aggregate_by_period('month'))
# visualizer.plot_time_series(df, 'month', 'distance', 'Monthly Distance', 'Month', 'Distance (miles)', 'monthly_distance.png')