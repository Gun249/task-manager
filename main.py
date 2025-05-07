# from src.data import DatasetProcessor
# from src.suitabilty import Suitability
# from src.datasplit import DataSplitter
# import pandas as pd
from src.apichatbot import apichatbot
from src.botcompae import botcompae


class main:
    def __init__(self):
        # self.ds_processor = DatasetProcessor()
        # self.suitabilty = Suitability(self.ds_processor)
        # self.datasplit = DataSplitter()
        # สร้างอ็อบเจกต์สำหรับเรียกใช้งาน Chatbot และโมเดลเปรียบเทียบ Role-Task
        self.apichatbot = apichatbot()
        self.botcompae = botcompae()

    # def run(self):
        # self.ds_processor.process_all_datasets()

        # hr = self.ds_processor.get_dataset("hr_dashboard_data")
        # task = self.ds_processor.get_dataset("Task Catagories")

        # print("\nComputing suitability scores...")
        # scores = self.suitabilty.compute_suitability_scores(hr, task)

        # scores_df = pd.DataFrame(scores)

        # hr["Best_Category"] = scores_df["Best_Category"]
        # hr["Suitability_Score"] = scores_df["Suitability_Score"]
        # hr["Composite_score"] = scores_df["Composite_score"]

        
        # hr.drop(columns=["Department", "Position"], inplace=True, axis=1)
        # print("\nUpdated HR data with suitability scores:")
        # print(hr.head())

    def main(self):
        # วนลูปจนกว่าจะได้ข้อมูล Role และ Tasks ที่ถูกต้องจาก Chatbot
        while True:
            # รับรายละเอียดโปรเจกต์จากผู้ใช้
            try:
                Project_details = input("\nPlease provide project details: ").strip()
                if not Project_details:
                    print("Project details cannot be empty. Please try again.")
                    continue
            except Exception as e:
                print("Error reading project details:", e)
                continue

            # เรียก Chatbot เพื่อสร้างคำถาม-คำตอบและดึง Role กับ Tasks
            try:
                Role, Tasks = self.apichatbot.chatbot(Project_details)
            except Exception as e:
                print("Error during chatbot processing:", e)
                continue

            # ตรวจสอบความถูกต้องของผลลัพธ์
            if Role is None or Tasks is None:
                print("\nChatbot did not return valid results. Retrying...")
                continue
            if len(self.apichatbot.questions) < 5:
                print(f"\nInsufficient interview questions extracted (found only {len(self.apichatbot.questions)}). Retrying...")
                continue
            if not Tasks:
                print("\nNo tasks were extracted. Retrying...")
                continue

            # ถ้าผ่านทุกเงื่อนไข ให้หยุดลูป
            break

        # แสดง Role ที่ Chatbot วิเคราะห์ได้
        print("\nRole:", Role)

        # ส่ง Role และ Tasks ไปให้โมเดล Siamese เปรียบเทียบความเหมาะสม
        try:
            self.botcompae.model(Role, Tasks)
        except Exception as e:
            print("Error during role-task matching:", e)

# สร้างอินสแตนซ์และเรียกใช้เมธอด main()
if __name__ == "__main__":
    mainrun = main()
    mainrun.main()

