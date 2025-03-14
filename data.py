import glob  # ใช้สำหรับค้นหาไฟล์ในโฟลเดอร์
import pandas as pd  # ใช้สำหรับจัดการข้อมูล DataFrame
import os  # ใช้สำหรับจัดการ path ของไฟล์

class DatasetProcessor:
    def __init__(self, data_folder="dataset"):
        # กำหนดโฟลเดอร์เก็บไฟล์ข้อมูลและสร้าง dictionary สำหรับเก็บ dataset
        self.data_folder = data_folder
        self.datasets = {}

    def scan_file(self):
        # ค้นหาไฟล์ CSV ทั้งหมดที่อยู่ในโฟลเดอร์ที่กำหนด
        csv_file = glob.glob(f"{self.data_folder}/*.csv")
        print(f"Found {len(csv_file)} CSV files")
        return csv_file

    def clean_data(self, df):
        # สร้างสำเนาของ DataFrame เพื่อป้องกันการเปลี่ยนแปลงข้อมูลต้นฉบับ
        cleaned_df = df.copy()
        
        # กำจัดแถวที่มีค่า missing (NaN)
        cleaned_df.dropna(inplace=True)
        
        # สามารถเปิดใช้งานเพื่อลบแถวที่ซ้ำกันได้
        # cleaned_df.drop_duplicates(inplace=True)
        
        return cleaned_df

    def process_all_datasets(self):
        # ดึงรายชื่อไฟล์ CSV ทั้งหมดในโฟลเดอร์
        csv_files = self.scan_file()

        # วนลูปเพื่อประมวลผลทุกไฟล์ CSV
        for file_path in csv_files:
            # แยกชื่อไฟล์ออกมาเป็น key สำหรับ dictionary (ไม่รวมส่วนขยาย)
            file_name = os.path.basename(file_path.split(".")[0])
            try:
                # อ่านข้อมูลจากไฟล์ CSV เข้าสู่ DataFrame
                df = pd.read_csv(file_path)
                # ทำความสะอาดข้อมูล (clean data)
                clean_df = self.clean_data(df)
                # สร้างฟีเจอร์ performance (รวมทั้ง normalization และคำนวณ performance_index)
                self.feature_engineering_performance(clean_df, file_name)
                # เข้ารหัสข้อมูลในคอลัมน์ 'Skill' ให้เป็นตัวเลข (Label Encoding)
                self.endcode(clean_df)

                # เก็บข้อมูลที่ประมวลผลแล้วลงใน dictionary โดยใช้ชื่อไฟล์เป็น key
                self.datasets[file_name] = clean_df
                print(f"Successfully processed file {file_name}")
            except Exception as e:
                print(f"Error processing file {file_name}: {str(e)}")

        print(f"Successfully processed {len(self.datasets)} files")
        # print(self.datasets)

    def feature_engineering_performance(self, df, file_name):
        # กำหนดคอลัมน์ที่จำเป็นต้องมีสำหรับการคำนวณ performance_index
        required_columns = ['Projects Completed', 'Productivity (%)', 'Satisfaction Rate (%)', 'Feedback Score']
        if all(col in df.columns for col in required_columns):
            # ทำการ normalization ค่าของแต่ละฟีเจอร์ให้อยู่ในช่วง 0-1 ด้วยสูตร Min-Max Scaling
            df['Proj_norm'] = (df['Projects Completed'] - df['Projects Completed'].min()) / (df['Projects Completed'].max() - df['Projects Completed'].min())
            df['Prod_norm'] = (df['Productivity (%)'] - df['Productivity (%)'].min()) / (df['Productivity (%)'].max() - df['Productivity (%)'].min())
            df['Sat_norm'] = (df['Satisfaction Rate (%)'] - df['Satisfaction Rate (%)'].min()) / (df['Satisfaction Rate (%)'].max() - df['Satisfaction Rate (%)'].min())
            df['Feed_norm'] = (df['Feedback Score'] - df['Feedback Score'].min()) / (df['Feedback Score'].max() - df['Feedback Score'].min())

            # น้ำหนักของแต่ละฟีเจอร์สำหรับคำนวณ performance_index
            weight_proj = 0.3
            weight_prod = 0.35
            weight_sat = 0.25
            weight_feed = 0.1

            # คำนวณ performance_index โดยการรวมค่าที่ normalized ของแต่ละฟีเจอร์เข้าด้วยกัน
            df['performance_index'] = (df['Proj_norm'] * weight_proj +
                                       df['Prod_norm'] * weight_prod +
                                       df['Sat_norm'] * weight_sat +
                                       df['Feed_norm'] * weight_feed)
            print(f"File {file_name} has successfully undergone Feature Engineering")
            return df
        else:
            print("Feature Engineering not required")
            return df
        
    def endcode(self, df):
        # ตรวจสอบว่ามีคอลัมน์ 'Skill' อยู่ใน DataFrame หรือไม่
        required_columns = ['Skill']
        if all(col in df.columns for col in required_columns):
            # เข้ารหัสข้อมูลในคอลัมน์ 'Skill' ให้เป็นตัวเลข โดยใช้ Label Encoding
            df['Category_num'] = df['Category'].astype('category').cat.codes
            df['skill_num'] = df['Skill'].astype('category').cat.codes
            # สร้าง mapping ระหว่างตัวเลขกับค่าจริงในคอลัมน์ 'Skill'
            # skill_mapping = dict(enumerate(df['Skill'].astype('category').cat.categories))
            # category_mapping = dict(enumerate(df['Category'].astype('category').cat.categories))
            # print(f"Category Mapping: {category_mapping}")
            # print(f"Skill Mapping: {skill_mapping}")
            print("Successfully encoded Skill and Category columns")

    def get_dataset(self, name, colums=None):
        # คืนค่า dataset ที่ต้องการ โดยใช้ key ที่กำหนดไว้ใน dictionary
        if name in self.datasets:
            return self.datasets[name]
        elif colums != None:
            return self.datasets[name][colums]
        else:
            print(f"Dataset named {name} not found")
            return None

# สร้าง instance ของ DatasetProcessor
processor = DatasetProcessor()
# เรียกใช้กระบวนการประมวลผลทุก dataset ที่อยู่ในโฟลเดอร์
processor.process_all_datasets()
# แสดงข้อมูลจาก dataset ที่ชื่อ "Task Catagories"
# print(processor.get_dataset("Task Catagories"))

################################################################################
# สิ่งที่เหลืออยู่และต้องทำเพิ่มเติมก่อนเทรนโมเดล:
# 1. กำหนด Target Variable:
#    - ระบุเป้าหมายที่แน่ชัดสำหรับโมเดล เช่น "suitability_score" หรือ "match_score"
#    - สร้างหรือเตรียม label สำหรับการจับคู่สมาชิกกับงาน
#
# 2. Preprocess ข้อมูลเพิ่มเติม:
#    - เข้ารหัส (Encode) ข้อมูลอื่นๆ ที่เป็น categorical ใน datasets เช่น ใน "Task Catagories"
#      อาจต้องทำ One-Hot Encoding หรือ Label Encoding เพิ่มเติมสำหรับคอลัมน์อื่นๆ เช่น "Category"
#
# 3. การเชื่อมโยงข้อมูล (Mapping) ระหว่าง datasets:
#    - สร้างขั้นตอนการรวมข้อมูลจาก hr_dashboard_data และ Task Catagories
#      เพื่อใช้สำหรับเทรนโมเดลจับคู่สมาชิกกับงาน โดยอาจใช้ rule-based mapping หรือ feature engineering ระหว่าง datasets
#
# 4. แบ่งชุดข้อมูล (Train / Test Split):
#    - กำหนดวิธีแยกข้อมูลออกเป็นชุดเทรนและชุดทดสอบ เพื่อประเมินประสิทธิภาพของโมเดล
#
# 5. การเลือกและออกแบบโมเดล:
#    - คิดว่าจะใช้เทคนิคโมเดลแบบใด เช่น Recommendation System, Classification, Regression
#    - กำหนด hyperparameters และสร้าง pipeline สำหรับการเทรนโมเดล
#
# 6. การประเมินและปรับปรุงโมเดล:
#    - กำหนด metrics สำหรับวัดประสิทธิภาพของการจับคู่ (เช่น Precision, Recall, F1-Score)
#    - วางแผนการปรับแต่งโมเดลและทำ cross-validation
#
# 7. การใช้ API Chatbot (LLM) สำหรับการวิเคราะห์ข้อความ:
#    - นำ Large Language Model (LLM) มาใช้เป็นเครื่องมือช่วยวิเคราะห์โครงสร้างงาน (WBS)
#      และสร้างชุดคำถามเพื่อประเมินความสามารถของสมาชิก (ขั้นตอน 4.3 และ 4.4)
#    - ใช้เทคนิค NLP และ Pre-Trained Model เช่น ChatGPT หรือโมเดลที่ผ่านการเทรนล่วงหน้า
#      เพื่อสรุปข้อมูลจากข้อความที่หัวหน้าทีมป้อนเข้ามาและสร้างคำถามที่สอดคล้องกับขอบเขตงาน
################################################################################

