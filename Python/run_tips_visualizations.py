import plotly.express as px
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os

import matplotlib
matplotlib.use('Agg')


def save_matplotlib_figure(fig, filename):
    fig.tight_layout()
    fig.savefig(filename, dpi=150)
    plt.close(fig)


out_dir = '/workspaces/Visualizations/tips_outputs'
os.makedirs(out_dir, exist_ok=True)

# https://github.com/mwaskom/seaborn-data/blob/master/tips.csv
tips = sns.load_dataset('tips')
print('Tips dataset shape:', tips.shape)
print('Columns:', list(tips.columns))
print(tips.head().to_string(index=False))

# Matplotlib graphs
fig, ax = plt.subplots(figsize=(8, 5))

by_day = tips.groupby('day', as_index=False)['total_bill'].mean()
print(by_day.head().to_string(index=False))
ax.plot(by_day['day'], by_day['total_bill'],
        marker='o', color='royalblue', linewidth=2)
ax.set_title('Matplotlib - Average Bill by Day')
ax.set_xlabel('Day')
ax.set_ylabel('Average Total Bill')
ax.grid(True, alpha=0.3)
save_matplotlib_figure(fig, os.path.join(out_dir, 'matplotlib_line.png'))

fig, ax = plt.subplots(figsize=(8, 5))
by_day = tips.groupby('day', as_index=False)['total_bill'].mean()
ax.bar(by_day['day'], by_day['total_bill'], color='seagreen')
ax.set_title('Matplotlib - Bar Chart of Average Bill by Day')
ax.set_xlabel('Day')
ax.set_ylabel('Average Total Bill')
for i, value in enumerate(by_day['total_bill']):
    ax.text(i, value + 2, f'{value:.1f}', ha='center')
save_matplotlib_figure(fig, os.path.join(out_dir, 'matplotlib_bar.png'))

fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(tips['total_bill'], bins=15, color='purple', edgecolor='black')
ax.set_title('Matplotlib - Histogram of Total Bill')
ax.set_xlabel('Total Bill')
ax.set_ylabel('Frequency')
save_matplotlib_figure(fig, os.path.join(out_dir, 'matplotlib_histogram.png'))

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(tips['total_bill'], tips['tip'], alpha=0.7, color='darkorange')
ax.set_title('Matplotlib - Scatter Plot: Total Bill vs Tip')
ax.set_xlabel('Total Bill')
ax.set_ylabel('Tip')
save_matplotlib_figure(fig, os.path.join(out_dir, 'matplotlib_scatter.png'))

fig, ax = plt.subplots(figsize=(8, 5))
box_data = [tips[tips['day'] == d]['total_bill']
            for d in ['Sun', 'Sat', 'Thur', 'Fri']]
ax.boxplot(box_data)
ax.set_xticklabels(['Sun', 'Sat', 'Thur', 'Fri'])
ax.set_title('Matplotlib - Box Plot of Total Bill by Day')
ax.set_xlabel('Day')
ax.set_ylabel('Total Bill')
save_matplotlib_figure(fig, os.path.join(out_dir, 'matplotlib_boxplot.png'))

# Seaborn graphs- 
#The important point is that you don't have to manually use groupby() here. sns.lineplot() handles the grouping and aggregation because you specified estimator='mean'.
sns.set_style('whitegrid')
fig, ax = plt.subplots(figsize=(8, 5))
sns.lineplot(data=tips, x='day', y='total_bill',
             estimator='mean', marker='o', ax=ax)
ax.set_title('Seaborn - Average Bill by Day')
ax.set_xlabel('Day')
ax.set_ylabel('Average Total Bill')
save_matplotlib_figure(fig, os.path.join(out_dir, 'seaborn_line.png'))

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=tips, x='day', y='total_bill',
            estimator='mean', palette='Set2', ax=ax)
ax.set_title('Seaborn - Bar Plot of Average Bill by Day')
ax.set_xlabel('Day')
ax.set_ylabel('Average Total Bill')
save_matplotlib_figure(fig, os.path.join(out_dir, 'seaborn_bar.png'))

fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(tips['total_bill'], bins=15, kde=True,
             color='cornflowerblue', ax=ax)
ax.set_title('Seaborn - Histogram of Total Bill')
ax.set_xlabel('Total Bill')
ax.set_ylabel('Frequency')
save_matplotlib_figure(fig, os.path.join(out_dir, 'seaborn_histogram.png'))

fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=tips, x='total_bill', y='tip',
                hue='sex', alpha=0.8, ax=ax)
ax.set_title('Seaborn - Scatter Plot: Total Bill vs Tip')
ax.set_xlabel('Total Bill')
ax.set_ylabel('Tip')
save_matplotlib_figure(fig, os.path.join(out_dir, 'seaborn_scatter.png'))

fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=tips, x='day', y='total_bill', palette='pastel', ax=ax)
ax.set_title('Seaborn - Box Plot of Total Bill by Day')
ax.set_xlabel('Day')
ax.set_ylabel('Total Bill')
save_matplotlib_figure(fig, os.path.join(out_dir, 'seaborn_boxplot.png'))

# Plotly graphs
fig = px.line(
    tips.groupby('day', as_index=False)['total_bill'].mean(),
    x='day',
    y='total_bill',
    title='Plotly - Average Bill by Day',
    markers=True,
)
fig.write_html(os.path.join(out_dir, 'plotly_line.html'))

fig = px.bar(
    tips.groupby('day', as_index=False)['total_bill'].mean(),
    x='day',
    y='total_bill',
    title='Plotly - Bar Chart of Average Bill by Day',
)
fig.write_html(os.path.join(out_dir, 'plotly_bar.html'))

fig = px.histogram(tips, x='total_bill', nbins=15,
                   title='Plotly - Histogram of Total Bill')
fig.write_html(os.path.join(out_dir, 'plotly_histogram.html'))

fig = px.scatter(tips, x='total_bill', y='tip', color='sex',
                 title='Plotly - Scatter Plot: Total Bill vs Tip')
fig.write_html(os.path.join(out_dir, 'plotly_scatter.html'))

fig = px.box(tips, x='day', y='total_bill',
             title='Plotly - Box Plot of Total Bill by Day')
fig.write_html(os.path.join(out_dir, 'plotly_boxplot.html'))

print('\nGenerated files:')
for file in sorted(os.listdir(out_dir)):
    print('-', file)
