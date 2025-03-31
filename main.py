from src.data import DatasetProcessor
from src.suitabilty import Suitability
from src.datasplit import DataSplitter
import pandas as pd


class main:
    def __init__(self):
        self.ds_processor = DatasetProcessor()
        self.suitabilty = Suitability(self.ds_processor)
        self.datasplit = DataSplitter()

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

        output_file = "updated_hr_data.csv"
        hr.to_csv(output_file, index=False)
        print(f"\nExported updated HR data to {output_file}")

        data = self.datasplit.data_split(hr)
        # print("\nSplitting data...")
        # print(data)
        



        # print("\nUpdated HR data:")
        # print(hr.head())


mainrun = main()
mainrun.run()

        