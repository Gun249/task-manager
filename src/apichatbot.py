from google import genai
from dotenv import load_dotenv
import os
import re

load_dotenv()

class apichatbot:
    def __init__(self):
        # อ่าน API key จาก environment
        self.API_KEY = os.getenv("apikey")
        # เก็บคำถามที่สร้างได้
        self.questions = []
        # เก็บรายการ task ที่ดึงมา
        self.tasks = []
        # เก็บคำตอบที่ผู้ใช้ป้อน
        self.awser = []
        # เก็บ task หลังล้างข้อมูล
        self.cleandtask = []

    def chatbot(self, Project_details):
        """
        ฟังก์ชันหลัก ใช้ติดต่อกับ API
         1. สร้าง prompt แรกเพื่อให้ AI สร้างคำถามและ task
         2. แยกคำถามกับ task ออกจากข้อความตอบกลับ
         3. รอรับคำตอบจากผู้ใช้สำหรับคำถามเหล่านั้น
         4. สร้าง prompt ที่สองเพื่อให้ AI วิเคราะห์คำตอบ และเลือก Role ที่เหมาะสม
        คืนค่า: (Role, list_of_tasks)
        """
        # สร้าง client ด้วย API key
        try:
            client = genai.Client(api_key=self.API_KEY)
        except Exception as e:
            print("Error initializing client:", e)
            return None, None

        prompt1 = f"""You are an assistant team planner in a software project.

        1.  Analyze the content of the project and generate 5 **concise** interview questions.
        2.  Derive key Tasks that are necessary based on the project description. **Crucially, ensure that all identified tasks are explicitly assigned to, and suitable for, one of the following four major roles *only*:** Backend Developer, Frontend Developer, Project Manager (PM), and UX/UI Designer. Do not list tasks that do not clearly align with one of these specific roles.
        3.  The interview questions should be designed for **first-year university students or individuals with very foundational technical exposure**. The questions should be **simple and introductory, aiming to gauge basic understanding, enthusiasm for learning, and a general approach to thinking about technology projects**, rather than testing deep existing knowledge. The goal is to understand their interests, initial learning experiences, very basic technical inclinations, and nascent problem-solving mindset — so you can determine which **Role** they might be most suited for or could learn towards.
        4.  Do not mention or assign any Role directly in the questions. Just create thoughtful, open-ended questions that reveal a student's **foundational understanding**, preferences, and how they approach **simple technical or logical problems**. Questions should encourage them to think and explain in their own terms, even if not highly technical, focusing on "how" and "why" at a basic level.
        5.  The questions must collectively touch upon **very basic concepts relevant to all four Roles** (Backend Developer, Frontend Developer, PM, and UX/UI Designer), suitable for a first-year student's perspective.
            The aim is to discover their natural curiosity, initial understanding, and how they articulate their thoughts on these basic concepts.
        6.  The questions should be **technical in a very light and conceptual sense**, relevant to the project description but framed so a first-year student can relate without prior specific project experience. Avoid complex jargon. The questions should be designed to be answerable by a student at this level, encouraging them to share their thoughts rather than testing for specific correct answers.

        **Project Description:**
        {Project_details}

        **Expected Answer Format:**
        - **Question 1**: …
        - **Question 2**: …
        (Up to Question 5)

        - Identified Tasks:
            1.  **Role:** Backend Developer: (Task description for Backend Developer)
            2.  **Role:** Frontend Developer: (Task description for Frontend Developer)
            3.  **Role:** Project Manager (PM): (Task description for PM)
            4.  **Role:** UX/UI Designer: (Task description for UX/UI Designer)
            (and so on, ensuring each task clearly states one of the four roles above)
        """
        # เรียก API ให้สร้างเนื้อหา
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt1
            )
        except Exception as e:
            print("Error generating content:", e)
            return None, None

        # แสดงผลลัพธ์ดิบจาก API
        lines = response.text.splitlines()

        # เคลียร์ตัวแปรก่อนเริ่มแยกข้อมูล
        self.questions.clear()
        self.tasks.clear()
        self.awser.clear()
        self.cleandtask.clear()

        # แยกคำถามและ task
        try:
            # 1) แยกคำถาม และ raw task
            self.questions, raw_tasks = self.Separate_questions_and_tasks(lines)
            # 2) ทำความสะอาดชื่อ Role ออกจาก raw_tasks
            self.tasks = self.cleand_task(raw_tasks)
            # 3) ส่งโครงสร้างงานให้หัวหน้าทีมตรวจสอบและยืนยัน
            if not self.review_tasks_structure(self.tasks):
                print("โครงสร้างงานไม่ผ่านการยืนยัน เสร็จสิ้นการทำงาน")
                return None, None
            # 4) ถามผู้ใช้เพื่อรับคำตอบสำหรับคำถาม
            self.aws_questions(self.questions)
        except Exception as e:
            print("Error during parsing:", e)
            return None, None

        # ตรวจสอบว่ามีข้อมูลครบก่อนดำเนินการต่อ
        if len(self.questions) < 5:
            print(f"\nNo interview questions were extracted (found only {len(self.questions)}). Please try again.")
            return None, None
        if not self.tasks:
            print("\nNo tasks were extracted. Please try again.")
            return None, None


        # สร้าง prompt2 ถ้ามีข้อมูลครบถ้วน
        prompt2 = f"""
            You are the assistant team leader who analyzes the capabilities of team members.

            The following are the answers from a team member to interview questions (related to the project).  
            Your objectives are to:  
            - Analyze these answers and  
            - Identify which **Role** he/she best fits

            **Available Roles**:  
            - Backend Developer  
            - Project Manager (PM)  
            - Frontend Developer  
            - UX/UI Designer
            - (Please choose only one Role that best fits the member's answers)

            **Question**:  
            {self.questions[0]}  
            {self.questions[1]}  
            {self.questions[2]}  
            {self.questions[3]}  
            {self.questions[4]}

            **Member Answers:**  
            {self.awser[0] if len(self.awser) > 0 else "N/A"}  
            {self.awser[1] if len(self.awser) > 1 else "N/A"}  
            {self.awser[2] if len(self.awser) > 2 else "N/A"}  
            {self.awser[3] if len(self.awser) > 3 else "N/A"}  
            {self.awser[4] if len(self.awser) > 4 else "N/A"}

            **Required Answer:**  
            Please provide only the most appropriate Role name from the list above. Without further explanation.
            """
        
        try:
            response2 = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt2
            )
        except Exception as e:
            print("Error generating content for prompt2:", e)
            return None, None
        Role = response2.text.strip()
        print(f"\nRole: {Role}")
        return Role, self.tasks

    def Separate_questions_and_tasks(self, lines):
        """
        แยกบรรทัด text ที่ได้มา
        - ดักคำถาม (Question 1-5)
        - ดักบล็อก Identified Tasks
        """
        in_task_section = False

        for line in lines:
            line = line.strip()

            # เจอบล็อก Identified Tasks -> สลับไปเก็บ task แทน
            if "Identified Tasks" in line:
                in_task_section = True
                continue

            # เก็บคำถาม ถ้ายังไม่เข้าไปในบล็อก task
            if not in_task_section and re.match(r"-\s*(\*\*)?\s*Question\s+\d+", line, re.IGNORECASE):
                match = re.match(r"-\s*(\*\*)?\s*Question\s+\d+\s*(\*\*)?\s*:?\s*(.*)", line)
                if match:
                    question_text = match.group(3).strip()
                    self.questions.append(question_text)

            # เก็บ task แบบหัวข้อใหม่ (เลขนำหน้า)
            if in_task_section and re.match(r"^\d+\.", line):
                # เอาชื่อ Role ออกก่อน (ล้างภายหลัง)
                task_detail = re.sub(r"^\d+\.\s*(\*\*Role:\*\*\s*)?[^\:]+:\s*", "", line).strip()
                self.tasks.append(task_detail)

            # ถ้า task ต่อบรรทัดใหม่ (ขึ้นบรรทัดด้วย *) ให้ผนวกข้อความ
            elif in_task_section and line.startswith("*"):
                followup = line.lstrip("*").strip()
                if self.tasks:
                    self.tasks[-1] += f" {followup}"
                else:
                    self.tasks.append(followup)

        return self.questions, self.tasks

    def aws_questions(self, question):
        for q in question:
            print("\n", q)
            aws = input("กรุณาใส่คำตอบของคุณ: ")
            self.awser.append(aws)

    def cleand_task(self, raw_tasks):
        pattern = re.compile(
            r"^\*{0,2}\s*(Backend Developer|Frontend Developer|Project Manager \(PM\)|UX/UI Designer)\*{0,2}\s*:?\s*",
            re.IGNORECASE
        )

        for task in raw_tasks:
            cleaned = re.sub(pattern, "", task).strip()
            self.cleandtask.append(cleaned)

        return self.cleandtask

    def review_tasks_structure(self, tasks):
        print("\n--- ตรวจสอบโครงสร้างงาน ---")
        for i, t in enumerate(tasks, 1):
            print(f"  {i}. {t}")
        while True:
            ans = input("หัวหน้าทีมยืนยันโครงสร้างงานนี้หรือไม่? (Y/N): ").strip().upper()
            if ans == "Y":
                return True
            elif ans == "N":
                return False
            else:
                print("กรุณาใส่ Y หรือ N เท่านั้น")


