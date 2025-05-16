from src.apichatbot import apichatbot
from src.botcompae import RoleTaskMatcher


class main:
    def __init__(self):
        # สร้างอ็อบเจกต์สำหรับเรียกใช้งาน Chatbot และโมเดลเปรียบเทียบ Role-Task
        self.apichatbot = apichatbot()
        self.botcompae = RoleTaskMatcher()


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

            if Role is None or Tasks is None:
                print("\nChatbot did not return valid results. Retrying...")
                continue
            if not hasattr(self.apichatbot, 'questions') or len(self.apichatbot.questions) < 5 :
                questions_count = len(self.apichatbot.questions) if hasattr(self.apichatbot, 'questions') else 0
                print(f"\nInsufficient interview questions extracted (found only {questions_count}). Retrying...")
                continue
            if not Tasks: 
                print("\nNo tasks were extracted. Retrying...")
                continue

            break


        try:
            suitable_tasks_found = self.botcompae.find_suitable_tasks(Role, Tasks)
            
            if suitable_tasks_found:
                print("\n--- Role-Task Matching Results ---")
                print(f"For Role: {Role}")
                print("Suitable tasks found:")
                for task_text, score in suitable_tasks_found:
                    print(f"  - Task: \"{task_text}\" (Score: {score:.4f})")

        except Exception as e:
            print("Error during role-task matching execution in main:", e)

if __name__ == "__main__":
    mainrun = main()
    mainrun.main()