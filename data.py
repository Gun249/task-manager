import glob
import pandas as pd
import os

class DatasetProcessor:
    def __init__(self,data_folder = "datset"):
        self.data_folder = data_folder
        self.datasets = {}
        