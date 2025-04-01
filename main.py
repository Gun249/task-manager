from src.data import DatasetProcessor
from src.suitabilty import Suitability
from src.datasplit import DataSplitter
from src.apichatbot import apichatbot
from src.botcompae import botcompae
import pandas as pd


class main:
    def __init__(self):
        self.ds_processor = DatasetProcessor()
        self.suitabilty = Suitability(self.ds_processor)
        self.datasplit = DataSplitter()
        self.apichatbot = apichatbot()
        self.botcompae = botcompae()

    def run(self):
        self.ds_processor.process_all_datasets()

        hr = self.ds_processor.get_dataset("hr_dashboard_data")
        task = self.ds_processor.get_dataset("Task Catagories")

        print("\nComputing suitability scores...")
        scores = self.suitabilty.compute_suitability_scores(hr, task)

        scores_df = pd.DataFrame(scores)

        hr["Best_Category"] = scores_df["Best_Category"]
        hr["Suitability_Score"] = scores_df["Suitability_Score"]
        hr["Composite_score"] = scores_df["Composite_score"]

        
        hr.drop(columns=["Department", "Position"], inplace=True, axis=1)
        print("\nUpdated HR data with suitability scores:")
        # print(hr.head())

    def main(self):
        Project_details = str(input("กรุณาใส่รายละเอียดของโปรเจกต์: "))
        Role,Tasks = self.apichatbot.chatbot(Project_details)
        print("\nRole: ", Role)
        self.botcompae.model(Role,Tasks)
        


mainrun = main()
mainrun.main()

        