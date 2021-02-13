from godot import exposed, export, Vector2, Area2D, Node2D
from godot import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import collections

'''
Tasks:

1. Find Anomalies in the data set to automatically flag events
2. Categorize anomalies as "Systm fault" or "External event"
3. Provide any other useful conclusions from the pattern in the data set
4. Visualize inter-dependencies of the features in the dataset 

'''


@exposed
class Node(Node2D):

	# member variables here, example:
	a = export(int)
	b = export(str, default='foo')

	def _ready(self):
		'''ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
		ts = ts.cumsum()
		ts.plot()
		plt.show()'''
		data_file1 = pd.read_csv("Data/data11.csv")
		data_file2 = pd.read_csv("Data/data12.csv")
		data = pd.concat([data_file1.iloc[1:], data_file2[1:]], axis=0, ignore_index=True)
		data.drop(columns=['Date', 'Time GMT -4', 'Latitude', 'Longitude', 'Unnamed: 16'], inplace=True)
		data['Timestamp'] = pd.to_datetime(data.Timestamp, unit='ms')
		data.set_index('Timestamp', inplace=True)
		data.index = data.index.tz_localize('UTC').tz_convert('US/Eastern')
		
		intervals = []
		for i in range(1, len(data.index)):
			intervals.append((data.index[i] - data.index[i-1]).seconds)
			
		cnt = collections.Counter(intervals)
		df_cnt = pd.DataFrame(sorted(cnt.items(), key=lambda x: x[1], reverse=True))
		df_cnt.columns = ['Interval (s)', 'Counts']
		print(df_cnt.head(5))
		
		fig, ax = plt.subplots(figsize=(16, 6))
		for col in data.columns:
			data[col] = data[col].astype('float64')    
			data.plot(y=col, use_index=True, ax=ax)
		plt.show()
		
	def _draw(self):
		self.draw_line(Vector2(10, 10), Vector2(50, 30), Color(1, 1, 0))
