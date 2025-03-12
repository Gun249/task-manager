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
        cleaned_df.ropna(inplace=True)  # ตัดแถวที่มีค่า NaN
        
        # 2. ลบข้อมูลซ้ำ
        cleaned_df.drop_duplicates(inplace=True)
        
        # 3. แปลงประเภทข้อมูลให้ถูกต้อง
        # ตัวอย่าง: cleaned_df['column_name'] = pd.to_numeric(cleaned_df['column_name'], errors='coerce')
        
        # 4. จัดการกับข้อมูลที่ผิดปกติ (Outliers)
        # ต้องปรับตามลักษณะข้อมูลจริง เช่น:
        # for column in numeric_columns:
        #     Q1 = cleaned_df[column].quantile(0.25)
        #     Q3 = cleaned_df[column].quantile(0.75)
        #     IQR = Q3 - Q1
        #     cleaned_df = cleaned_df[~((cleaned_df[column] < (Q1 - 1.5 * IQR)) | (cleaned_df[column] > (Q3 + 1.5 * IQR)))]
        
        # 5. มาตรฐานข้อมูลข้อความ (สำหรับคอลัมน์ประเภทข้อความ)
        # text_columns = ['col1', 'col2']  # ระบุคอลัมน์ข้อความ
        # for col in text_columns:
        #     if col in cleaned_df.columns:
        #         cleaned_df[col] = cleaned_df[col].str.lower()  # แปลงเป็นตัวพิมพ์เล็ก
        #         cleaned_df[col] = cleaned_df[col].str.strip()  # ตัดช่องว่างหน้าหลัง
        
        # 6. ลบคอลัมน์ที่ไม่จำเป็น
        # cleaned_df.drop(columns=['unnecessary_column'], inplace=True)d
        
        return cleaned_df
    
    def process_all_datasets(self):
        csv_files = self.scan_file()

        # for file_path in csv_files:
        


processor = DatasetProcessor()

processor.scan_file()