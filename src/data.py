import glob                      # สำหรับค้นหาไฟล์ในโฟลเดอร์
import os                        # สำหรับจัดการเส้นทางของไฟล์
import pandas as pd              # สำหรับจัดการข้อมูลในรูปแบบ DataFrame
from src.feature_engineering import feature_enginerr   # ฟังก์ชันสำหรับ Feature Engineering

class DatasetProcessor:
    def __init__(self, data_folder="dataset"):
        """
        กำหนดโฟลเดอร์เก็บไฟล์ CSV และสร้าง dictionary เพื่อเก็บ dataset
        """
        self.data_folder = data_folder
        self.datasets = {}  # เก็บ dataset โดยใช้ชื่อไฟล์เป็น key

    def scan_file(self):
        """
        ค้นหาไฟล์ CSV ทั้งหมดในโฟลเดอร์ที่กำหนด
        """
        csv_files = glob.glob(f"{self.data_folder}/*.csv")
        print(f"\nFound {len(csv_files)} CSV files")
        return csv_files

    def clean_data(self, df):
        """
        ทำความสะอาดข้อมูล:
         - สร้างสำเนา DataFrame เพื่อไม่กระทบข้อมูลต้นฉบับ
         - ล้างช่องว่างบนชื่อคอลัมน์
         - ลบแถวที่มีค่า missing (NaN)
        """
        cleaned_df = df.copy()
        cleaned_df.columns = cleaned_df.columns.str.strip()
        cleaned_df.dropna(inplace=True)
        # สามารถเปิดใช้ลบแถวที่ซ้ำกันได้ (uncomment บรรทัดด้านล่างหากต้องการ)
        # cleaned_df.drop_duplicates(inplace=True)
        return cleaned_df

    def process_all_datasets(self):
        """
        โหลดและประมวลผลข้อมูลจากไฟล์ CSV ทั้งหมด:
         - อ่านข้อมูลจากไฟล์
         - ทำความสะอาดข้อมูล
         - ดำเนินการ Feature Engineering (เช่น คำนวณ performance index)
         - ลบคอลัมน์ไม่จำเป็น (เช่น Age, Gender, Joining Date, Salary)
         - ดำเนินการ Encoding สำหรับคอลัมน์ (เช่น Skill, Category, หรือ Gender)
         - เก็บ DataFrame ที่ผ่านการประมวลผลไว้ใน dictionary
        """
        csv_files = self.scan_file()
        for file_path in csv_files:
            # ดึงชื่อไฟล์โดยไม่รวมส่วนขยาย
            file_name = os.path.basename(file_path.split(".")[0])
            try:
                # กำหนด delimiter ตามชื่อไฟล์
                if file_name == "hr_dashboard_data":
                    df = pd.read_csv(file_path, delimiter=",")
                else:
                    df = pd.read_csv(file_path, delimiter=";")
                
                # ทำความสะอาดข้อมูล
                clean_df = self.clean_data(df)
                
                # ดำเนินการ Feature Engineering
                self.feature_enginerr = feature_enginerr(clean_df, file_name)
                clean_df = self.feature_enginerr.feature_engineering_performance()
                
                # ลบคอลัมน์ที่ไม่จำเป็น (ถ้ามี)
                required_columns = ['Age', 'Gender', 'Joining Date', 'Salary']
                if all(col in clean_df.columns for col in required_columns):
                    clean_df.drop(columns=required_columns, inplace=True, axis=1)
                
                # ดำเนินการ Encoding สำหรับคอลัมน์ที่ต้องการ (Skill/Category หรือ Department/Position)
                self.endcode(clean_df)
                
                # เก็บ DataFrame ที่ประมวลผลแล้วไว้ใน dictionary โดยใช้ชื่อไฟล์เป็น key
                self.datasets[file_name] = clean_df
                print(f"\nSuccessfully processed file {file_name}")
            except Exception as e:
                print(f"\nError processing file {file_name}: {str(e)}")
        
        print(f"\nSuccessfully processed {len(self.datasets)} files")

    def endcode(self, df):
        """
        ดำเนินการ Encoding สำหรับคอลัมน์ที่ต้องการ:
         - ถ้ามีคอลัมน์ 'Skill' และ 'Category' ให้ทำ Label Encoding
         - หากมีคอลัมน์ 'Department' และ 'Position' ให้ทำ Encoding
         - หากไม่มีคอลัมน์เหล่านี้ ให้แสดงข้อความว่าไม่จำเป็น
        """
        # กำหนดกลุ่มคอลัมน์สำหรับการ Encoding
        columns_group1 = ['Skill', 'Category']
        columns_group2 = ['Department', 'Position']
        
        if all(col in df.columns for col in columns_group1):
            df['Category_num'] = df['Category'].astype('category').cat.codes
            df['skill_num'] = df['Skill'].astype('category').cat.codes
            print("\nSuccessfully encoded Skill and Category columns")
            return df
        elif all(col in df.columns for col in columns_group2):
            df['department_num'] = df['Department'].astype('category').cat.codes
            df['position_num'] = df['Position'].astype('category').cat.codes
            print("\nSuccessfully encoded Department and Position columns")
            return df
        else:
            print("\nEncoding not required")
            return df

    def get_dataset(self, name, colums=None):
        """
        คืนค่า DataFrame ที่เก็บไว้ใน dictionary ตามชื่อไฟล์
         - หากระบุ colums จะคืนเฉพาะคอลัมน์ที่ต้องการ
        """
        if name in self.datasets:
            if colums is not None:
                return self.datasets[name][colums]
            return self.datasets[name]
        else:
            print(f"\nDataset named {name} not found")
            return None