import spacy
# โหลดโมเดลภาษาอังกฤษขนาดใหญ่ของ spaCy (ใช้วัดความคล้ายกันของข้อความ)
nlp = spacy.load('en_core_web_lg')

class Suitability:
    def __init__(self, ds_processor):
        # เก็บ instance ของ DatasetProcessor ไว้เพื่อดึงข้อมูล performance_index
        self.ds_processor = ds_processor
    
    def compute_suitability_scores(self, hr, task):
        """
        คำนวณคะแนนความเหมาะสมของแต่ละผู้สมัคร (hr) กับหมวดงาน (task)
        - hr: DataFrame ของผู้สมัครที่มีคอลัมน์ Name, Position, performance_index
        - task: DataFrame ของงานที่มีคอลัมน์ Category
        คืนค่า: list ของ dict แต่ละผู้สมัคร พร้อมรายละเอียดคะแนน
        """
        scores = []

        # วนอ่านแต่ละแถวใน hr DataFrame
        for idx, row in hr.iterrows():
            candidate = row.get("Position", "").strip()
            print(f"\nProcessing {row.get('Name', '')} for position {candidate}")

            if candidate:
                # หาความคล้ายกันระหว่างชื่อ Position กับแต่ละ Category ของงาน
                similarities = self.compare_pos(candidate, task)
                # กำหนดน้ำหนักของคะแนนส่วน Category กับ Performance
                weight_category = 0.5
                weight_performance = 0.5

                if similarities:
                    # เลือก Category ที่ similarity สูงสุด
                    best_category, best_sim = max(similarities, key=lambda x: x[1])
                    # คำนวณ Composite score = sim(category)*w1 + performance_index*w2
                    Composite_score = best_sim * weight_category + row.get("performance_index", 0) * weight_performance
                else:
                    # กรณีไม่มี similarity เก็บค่าเริ่มต้น
                    best_category, best_sim, Composite_score = None, 0, 0

                # เก็บผลลัพธ์ของผู้สมัครคนนี้
                scores.append({
                    "Name": row.get("Name", ""),
                    "Position": candidate,
                    "Best_Category": best_category,
                    "Suitability_Score": best_sim,
                    "Composite_score": Composite_score
                })
            else:
                # กรณีไม่มีตำแหน่งงานในข้อมูล
                print("\nNo position found for the candidate")
                scores.append({
                    "Name": row.get("Name", ""),
                    "Position": "No position found",
                    "Best_Category": None,
                    "Suitability_Score": 0,
                    "Composite_score": 0
                })

        return scores

    def compare_pos(self, position, task):
        """
        เปรียบเทียบความคล้ายกัน (semantic similarity) ระหว่างข้อความ position
        กับแต่ละ 'Category' ในตาราง task
        - position: ชื่อตำแหน่งงานของผู้สมัคร (string)
        - task: DataFrame ที่มีคอลัมน์ 'Category'
        คืนค่า: list ของ tuple (category, similarity) เรียงจากมากไปน้อย
        """
        # แปลง position เป็น spaCy Doc
        position_doc = nlp(position)
        similarities = []

        # หาหมวดหมู่ (Category) ที่ไม่ซ้ำกัน
        unique_categories = task['Category'].drop_duplicates()

        for category in unique_categories:
            category_doc = nlp(str(category))
            # วัดความคล้ายกันด้วย cosine similarity บนเวกเตอร์ spaCy
            sim = position_doc.similarity(category_doc)
            similarities.append((category, sim))
        
        # เรียงลำดับจาก similarity สูงสุดไปต่ำสุด
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities
