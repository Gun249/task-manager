import glob              # สำหรับค้นหาไฟล์ในโฟลเดอร์
import pandas as pd      # สำหรับจัดการข้อมูลในรูปแบบ DataFrame
import os                # สำหรับจัดการเส้นทางของไฟล์
import spacy             # สำหรับประมวลผลภาษา (NLP)

# โหลด spaCy model สำหรับแปลงข้อความเป็นเวกเตอร์
nlp = spacy.load("en_core_web_lg")


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
                self.feature_engineering_performance(clean_df, file_name)
                # ดำเนินการ Encoding สำหรับคอลัมน์ต่าง ๆ (Skill, Category หรือ Gender)
                self.endcode(clean_df)
                # เก็บ DataFrame ที่ผ่านการประมวลผลไว้ใน dictionary
                self.datasets[file_name] = clean_df
                print(f"\nSuccessfully processed file {file_name}")
            except Exception as e:
                print(f"\nError processing file {file_name}: {str(e)}")
        print(f"\nSuccessfully processed {len(self.datasets)} files")

    def feature_engineering_performance(self, df, file_name):
        # กำหนดคอลัมน์ที่จำเป็นต้องมีสำหรับการคำนวณ performance index
        required_columns = ['Projects Completed', 'Productivity (%)', 'Satisfaction Rate (%)', 'Feedback Score']
        if all(col in df.columns for col in required_columns):
            # คำนวณ normalized values ด้วยสูตร Min-Max Scaling
            df['Proj_norm'] = (df['Projects Completed'] - df['Projects Completed'].min()) / (df['Projects Completed'].max() - df['Projects Completed'].min())
            df['Prod_norm'] = (df['Productivity (%)'] - df['Productivity (%)'].min()) / (df['Productivity (%)'].max() - df['Productivity (%)'].min())
            df['Sat_norm'] = (df['Satisfaction Rate (%)'] - df['Satisfaction Rate (%)'].min()) / (df['Satisfaction Rate (%)'].max() - df['Satisfaction Rate (%)'].min())
            df['Feed_norm'] = (df['Feedback Score'] - df['Feedback Score'].min()) / (df['Feedback Score'].max() - df['Feedback Score'].min())
            
            # กำหนดน้ำหนักสำหรับแต่ละฟีเจอร์
            weight_proj = 0.3
            weight_prod = 0.35
            weight_sat = 0.25
            weight_feed = 0.1
            
            # คำนวณ performance_index โดยรวม normalized value เข้าด้วยกัน
            df['performance_index'] = (df['Proj_norm'] * weight_proj +
                                       df['Prod_norm'] * weight_prod +
                                       df['Sat_norm'] * weight_sat +
                                       df['Feed_norm'] * weight_feed)
            print(f"\nFile {file_name} has successfully undergone Feature Engineering")
            return df
        else:
            print("\nFeature Engineering not required")
            return df

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

    def compare_position_category_all(self, position, task_categories_df):
        """
        เปรียบเทียบ vector similarity ระหว่างตำแหน่ง (Position) กับ Category ใน task_categories_df
        โดยใช้ spaCy model และคืนค่าเป็น list ของ tuple (Category, similarity) ที่เรียงลำดับจากมากไปน้อย
        """
        # แปลงตำแหน่งของ candidate ให้เป็น spaCy document
        position_doc = nlp(position)
        similarities = []
        # เลือกเฉพาะ Category ที่ไม่ซ้ำใน task_categories_df
        unique_categories = task_categories_df['Category'].drop_duplicates()
        # วนลูปคำนวณ similarity สำหรับแต่ละ Category
        for category in unique_categories:
            category_doc = nlp(str(category))
            sim = position_doc.similarity(category_doc)
            similarities.append((category, sim))
        # เรียงลำดับค่า similarity จากสูงสุดไปต่ำสุด
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities

    def compute_suitability_scores(self, task_categories_df, candidates_df):
        """
        เปรียบเทียบ vector similarity ระหว่างตำแหน่ง (Position) ของ candidate กับ Category
        ใน task_categories_df และคำนวณ suitability_score จาก similarity ที่สูงสุด 
        ผลลัพธ์จะถูกเก็บไว้ในรูปแบบ list ของ dictionary สำหรับแต่ละ candidate
        """
        scores = []
        # วนลูปผ่าน candidate ทีละแถว
        for idx, row in candidates_df.iterrows():
            candidate_position = row.get("Position", "").strip()  # ดึงตำแหน่งและลบช่องว่าง
            print(f"\nProcessing candidate: {row.get('Name', 'Unknown')}")
            if candidate_position:
                # คำนวณ similarity ระหว่าง candidate กับทุก Category ใน task_categories_df
                similarities = self.compare_position_category_all(candidate_position, task_categories_df)
                # กำหนดน้ำหนักสำหรับส่วนประกอบการคำนวณ
                weight_category = 0.5
                weight_performance = 0.5
                if similarities:
                    # เลือก Category ที่ให้ similarity สูงสุด
                    best_category, best_sim = max(similarities, key=lambda x: x[1])
                    # คำนวณ Composite_score จาก similarity กับ performance_index (ถ้ามี)
                    Composite_score = best_sim * weight_category + row.get("performance_index", 0) * weight_performance
                else:
                    best_category, best_sim, Composite_score = None, 0, 0
                # เก็บค่าที่คำนวณได้ใน dictionary และเพิ่มเข้าสู่ list scores
                scores.append({
                    "Best_Category": best_category,
                    "Suitability_Score": best_sim,
                    "Performance_Index": row.get("performance_index", 0),
                    "Composite_score": Composite_score 
                })
            else:
                # กรณีที่ไม่มีข้อมูลตำแหน่ง ให้เก็บค่า 0 หรือ None
                scores.append({
                    "Best_Category": None,
                    "Suitability_Score": 0,
                    "Performance_Index": row.get("performance_index", 0),
                    "Composite_score": 0
                })
        return scores


# สร้าง instance ของ DatasetProcessor
processor = DatasetProcessor()

# เรียกใช้กระบวนการประมวลผลทุก dataset ในโฟลเดอร์
processor.process_all_datasets()

# ดึง DataFrame ของ "Task Catagories" และ "hr_dashboard_data" จาก datasets
task_categories_df = processor.get_dataset("Task Catagories")
hr_df = processor.get_dataset("hr_dashboard_data")

if task_categories_df is not None and hr_df is not None:
    print("\nCalculating suitability scores for all candidates:")
    # คำนวณ suitability scores สำหรับ candidate จาก hr_dashboard_data
    suitability_scores = processor.compute_suitability_scores(task_categories_df, hr_df)

    # เปลี่ยน list ที่ได้เป็น DataFrame เพื่อความสะดวกในการ merge กับ hr_df
    scores_df = pd.DataFrame(suitability_scores)
    
    # สมมุติว่า ordering ของ rows ใน scores_df ตรงกับ hr_df
    hr_df["Best_Category"] = scores_df["Best_Category"]
    hr_df["Suitability_Score"] = scores_df["Suitability_Score"]
    hr_df["Performance_Index"] = scores_df["Performance_Index"]
    hr_df["Composite_score"] = scores_df["Composite_score"]

else:
    print("\nRequired datasets not found.")