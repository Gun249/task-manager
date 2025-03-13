import glob
import pandas as pd
import os

class DatasetProcessor:
    def __init__(self,data_folder = "dataset"):
        self.data_folder = data_folder
        self.datasets = {}

    def scan_file(self):
        csv_file = glob.glob(f"{self.data_folder}/*.csv")
        # json_file = glob.glob(f"{self.data_folder}/*.json")
        print(f"พบไฟล์ CSV ทั้งหมด {len(csv_file)} ไฟล์")
        # print(f"พบไฟล์ json ทั้งหมด {len(json_file)} ไฟล์")
        return csv_file

    def clean_data(self, df):
        # สร้างสำเนาเพื่อไม่เปลี่ยนแปลงข้อมูลต้นฉบับ
        cleaned_df = df.copy()
        
        # 1. จัดการกับค่าที่หายไป (Missing Values)
        cleaned_df.dropna(inplace=True)  # ตัดแถวที่มีค่า NaN
        
        # # 2. ลบข้อมูลซ้ำ
        # cleaned_df.drop_duplicates(inplace=True)
        
        return cleaned_df
    
    def process_all_datasets(self):
        csv_files = self.scan_file()

        for file_path in csv_files:
            file_name = os.path.basename(file_path.split(".")[0])
            try : 
                df = pd.read_csv(file_path)
                
                clean_df = self.clean_data(df)

                self.datasets[file_name] = clean_df
                print(f"ประมวลผลสำเร็จ {file_name} แล้ว ")

            except Exception as e:
                print(f"เกิดข้อผิดพลากไฟล์ {file_name} {str(e)}")

        print(f"ประมวลผลทั้งหมด {len(self.datasets)} สำเร็จไฟล์แล้ว ")
        # print(self.datasets)

    def get_dataset(self,name):
        if name in self.datasets:
            return self.datasets[name]
        else:
            print(f"ไม่พบชื่อ {name}")
            return None


        


processor = DatasetProcessor()

processor.process_all_datasets()
print(processor.get_dataset("Absenteeism_at_work_Project"))

# def ordinal_encode_with_category(self, df, column_name):
#     categories = ['Below College', 'College', 'Bachelor', 'Master', 'Doctor']
#     df[column_name] = pd.Categorical(df[column_name], categories=categories, ordered=True)
#     df[column_name] = df[column_name].cat.codes + 1  # +1 เพื่อให้ 1 เป็นค่าเริ่มต้น
#     return df