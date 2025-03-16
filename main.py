from src.data import DatasetProcessor
from src.suitabilty import Suitability
import pandas as pd


class main:
    def __init__(self):
        self.ds_processor = DatasetProcessor()
        self.suitabilty = Suitability(self.ds_processor)

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

        print("\nUpdated HR data:")
        print(hr.head())


mainrun = main()
mainrun.run()

        