# ===========================================================================================================
# 本程序用途如下：
# 将一列一列的数据转化为二维矩阵数据
#
# 用法如下：
#       data = ConvertData(<file_path>, <column_name>)        --> 输入参数为要读取的文件名和列名
#       data.read_data()                                      --> 读取数据（保存数据后可注释）
#       data.convert_data()                                   --> 转换数据（保存数据后可注释）
#       data.save_converted_data( <your_path> )               --> 保存转换后的数据（保存数据后可注释）
#       data.load_converted_data( <your_path> )               --> 读取转换后的数据
#
#       data.get_data( <column_name> )                        --> 获取转换后的数据
#       data.choose_data( <step> )                            --> 挑选数据，每隔 step 个数据挑选一个
# ===========================================================================================================
import shelve
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import scipy
from tqdm import trange


class ConvertData:
    """
    用于将一列一列的数据转化为二维矩阵数据
    """

    def __init__(self, filepath, col_names):
        """
        
        Args:
            filepath: 要读取的文件的路径 
            col_names: 列名
        """
        self.filepath = Path(filepath)
        self.col_names = col_names

        self.init_data = None
        self.data = None
        self.converted_data: Optional[dict] = None

    def read_data(self):
        """
        读取数据
        """
        init_data = pd.read_csv(self.filepath, sep='\s+', names=self.col_names)
        self.init_data = init_data
        self.data = self.init_data.copy()

    def choose_data(self, step):
        """
        挑选数据，每隔 step 个数据挑选一个
        Args:
            step: 挑选数据的间隔
        """
        self.data = self.init_data.iloc[::step]

    def convert_data(self):
        """
        转换数据
        """
        x_grid, y_grid, grid_datas = self.convert_data_to_matrix_2D(
            self.data.to_numpy())
        temp_dict = {}
        for i, name in enumerate(self.col_names[2:]):
            temp_dict[name] = grid_datas[i]
        self.converted_data = (x_grid, y_grid, temp_dict)

    @staticmethod
    def convert_data_to_matrix_2D(data: np.array, **kwargs):
        """
        将一列一列的数据转化为二维矩阵数据
        Args:
            data: 要转换的数据
                要求前两列为位置坐标，其余列为数据

        Returns:
            x_grid: x 坐标的网格
            y_grid: y 坐标的网格
            grid_datas(np.array): 转换后的数据
        """
        # 检查数据是否符合要求
        if data.shape[1] < 3:
            raise ValueError('data must have at least 3 columns')

        # 提取 kwargs 中的参数
        interpolate_args = {
            'method': 'linear'
        }
        if 'interpolate_method' in kwargs:
            interpolate_args['method'] = kwargs['interpolate_method']

        x_values = np.sort(np.unique(data[:, 0]))
        y_values = np.sort(np.unique(data[:, 1]))
        x_grid, y_grid = np.meshgrid(x_values, y_values)

        grid_datas = []

        for i in trange(2, data.shape[1]):
            grid_data = scipy.interpolate.griddata(
                data[:, 0:2], data[:, i], (x_grid, y_grid), **interpolate_args)
            grid_datas.append(grid_data)

        return x_grid, y_grid, grid_datas

    def save_converted_data(self, save_path):
        """
        保存转换后的数据
        Args:
            save_path: 路径
        """
        if self.converted_data is None:
            raise ValueError('Data has not been converted yet.')

        x_grid, y_grid, grid_datas = self.converted_data

        cache_file = shelve.open(save_path)
        cache_file['x_grid'] = x_grid
        cache_file['y_grid'] = y_grid
        cache_file['grid_datas'] = grid_datas
        cache_file.close()

    def load_converted_data(self, load_path):
        """
        读取转换后的数据
        Args:
            load_path: 加载路径
        """
        cache_file = shelve.open(load_path)
        x_grid = cache_file['x_grid']
        y_grid = cache_file['y_grid']
        grid_datas = cache_file['grid_datas']
        cache_file.close()

        self.converted_data = (x_grid, y_grid, grid_datas)

    def get_data(self, col_name):
        """
        获取转换后的数据
        Args:
            col_name: 要获取的列名

        Returns:
            x_grid: x 坐标的网格
            y_grid: y 坐标的网格
            grid_data: 转换后的数据
        """
        if col_name not in self.col_names:
            raise ValueError('Column name not in the data')

        return self.converted_data[0], self.converted_data[1], self.converted_data[2][col_name]
