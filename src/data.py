import glob              # สำหรับค้นหาไฟล์ในโฟลเดอร์
import pandas as pd      # สำหรับจัดการข้อมูลในรูปแบบ DataFrame
import os                # สำหรับจัดการเส้นทางของไฟล์
from src.feature_engineering import feature_enginerr
# โหลด spaCy model สำหรับแปลงข้อความเป็นเวกเตอร์



class DatasetProcessor:
    def __init__(self, data_folder="dataset"):
        # กำหนดโฟลเดอร์เก็บไฟล์ CSV และสร้าง dictionary เพื่อเก็บ dataset

        self.data_folder = data_folder
        self.datasets = {}  # dictionary เก็บ dataset โดยใช้ชื่อไฟล์เป็น key

    def scan_file(self):
        # ค้นหาไฟล์ CSV ทั้งหมดในโฟลเดอร์ที่กำหนด
        csv_files = glob.glob(f"{self.data_folder}/*.csv")
        print(f"\nFound {len(csv_files)} CSV files")
        return csv_files

    def clean_data(self, df):
        # สร้างสำเนา DataFrame เพื่อไม่กระทบข้อมูลต้นฉบับ
        cleaned_df = df.copy()
        # ล้างช่องว่างบนชื่อคอลัมน์
        cleaned_df.columns = cleaned_df.columns.str.strip()
        # ลบแถวที่มีค่า missing (NaN)
        cleaned_df.dropna(inplace=True)
        # สามารถเปิดใช้ลบแถวที่ซ้ำได้หากต้องการ
        # cleaned_df.drop_duplicates(inplace=True)
        return cleaned_df

    def process_all_datasets(self):
        # เรียกใช้เมธอด scan_file เพื่อดึงรายชื่อไฟล์ CSV ทั้งหมด
        csv_files = self.scan_file()
        # วนลูปอ่านไฟล์แต่ละไฟล์
        for file_path in csv_files:
            # ดึงชื่อไฟล์โดยไม่รวมส่วนขยาย
            file_name = os.path.basename(file_path.split(".")[0])
            try:
                # ถ้าเป็นไฟล์ "hr_dashboard_data" ใช้ comma (,) เป็นตัวคั่น
                if file_name == "hr_dashboard_data":
                    df = pd.read_csv(file_path, delimiter=",")
                else:
                    # สำหรับไฟล์อื่น ๆ (เช่น "Task Catagories") ใช้เซมิโคลอน (;) เป็นตัวคั่น
                    df = pd.read_csv(file_path, delimiter=";")
                # ทำความสะอาดข้อมูล
                clean_df = self.clean_data(df)
                # ดำเนินการ Feature Engineering (เช่น calculate performance index)
                self.feature_enginerr = feature_enginerr(clean_df, file_name)
                clean_df = self.feature_enginerr.feature_engineering_performance()
                # ดำเนินการ Encoding สำหรับคอลัมน์ต่าง ๆ (Skill, Category หรือ Gender)
                self.endcode(clean_df)
                # เก็บ DataFrame ที่ผ่านการประมวลผลไว้ใน dictionary
                self.datasets[file_name] = clean_df
                print(f"\nSuccessfully processed file {file_name}")
            except Exception as e:
                print(f"\nError processing file {file_name}: {str(e)}")
        print(f"\nSuccessfully processed {len(self.datasets)} files")

    def endcode(self, df):
        # ระบุ required_columns สำหรับการ Encoding
        required_columns = [['Skill', 'Category'], ["Gender"]]
        if all(col in df.columns for col in required_columns[0]):
            # ถ้ามีคอลัมน์ 'Skill' และ 'Category' ทำการ Label Encoding
            df['Category_num'] = df['Category'].astype('category').cat.codes
            df['skill_num'] = df['Skill'].astype('category').cat.codes
            print("\nSuccessfully encoded Skill and Category columns")
            return df
        elif all(col in df.columns for col in required_columns[1]):
            # ถ้ามีคอลัมน์ 'Gender' ทำการ Encoding (ตัวอย่างนี้แสดงเพียง print)
            print("\nSuccessfully encoded Gender column")
            return df
        else:
            print("\nEncoding not required")
            return df

    def get_dataset(self, name, colums=None):
        # คืนค่า DataFrame ที่เก็บไว้ใน dictionary ตามชื่อไฟล์
        if name in self.datasets:
            return self.datasets[name]
        elif colums is not None:
            return self.datasets[name][colums]
        else:
            print(f"\nDataset named {name} not found")
            return None