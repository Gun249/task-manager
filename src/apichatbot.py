from google import genai
from dotenv import load_dotenv
import os
import re

load_dotenv()

class apichatbot:
    def __init__(self):
        self.API_KEY = os.getenv("apikey")
        self.questions = []
        self.tasks = []
        self.awser = []
        self.cleandtask = []

    def chatbot(self, Project_details):
        client = genai.Client(api_key=self.API_KEY)
        prompt1 = f"""You are an assistant team planner in a software project.

        1. Analyze the content of the project and generate 5 interview questions.  
        2. Derive key Tasks that are necessary based on the project description. Please include tasks that align with the following four major roles: Backend Developer, Frontend Developer, Project Manager (PM), and UX/UI Designer.  
        3. The interview questions should be designed for **students** (e.g., university students or interns) in order to understand their interests, learning experiences, technical skills, and problem-solving mindset — so you can determine which **Role** they might be most suited for.  
        4. Do not mention or assign any Role directly. Just create thoughtful, open-ended questions that reveal a student's capabilities, preferences, and how they approach problems.
        5. The questions should be relevant to the project description and should not be generic.

        
        **Project Description:**  
        {Project_details}

        **Expected Answer Format:**  
        - ** Question 1 **: …  
        - ** Question 2 **: …  
        (Up to Question 5)

        - Identified Tasks:
            1.  **Role:** ...
            2.  **Role:** ...
        """

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt1
        )

        print(response.text)
        lines = response.text.splitlines()
        questions, tasks = self.Separate_questions_and_tasks(lines)
        tasks = self.cleand_task(tasks)
        print("\n", tasks)
        self.aws_questions(questions)

        prompt2 = f"""
            You are the assistant team leader who analyzes the capabilities of team members.

            The following are the answers from a team member to interview questions (related to the project).  
            Your objectives are to:  
            - Analyze these answers and  
            - Identify which **Role** he/she best fits

            **Question**:
            {self.questions[0]}
            {self.questions[1]}
            {self.questions[2]}
            {self.questions[3]}
            {self.questions[4]}

            **Member Answers:**
            {self.awser[0]}
            {self.awser[1]}
            {self.awser[2]}
            {self.awser[3]}
            {self.awser[4]}

            **Required Answers:**
            Please provide only the most appropriate Role name. Without further explanation.
            """

        response2 = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt2
        )
        Role = response2.text.strip()
        return Role, tasks

    def Separate_questions_and_tasks(self, lines):
        in_task_section = False
        current_task = ""

        for line in lines:
            line = line.strip()

            # เริ่มบล็อค Task
            if "Identified Tasks" in line:
                in_task_section = True
                continue

            # เก็บคำถาม
            if not in_task_section and re.match(r"-\s*(\*\*)?\s*Question\s+\d+\s*(\*\*)?\s*:?", line, re.IGNORECASE):
                match = re.match(r"-\s*(\*\*)?\s*Question\s+\d+\s*(\*\*)?\s*:?\s*(.*)", line)
                if match:
                    question_text = match.group(3).strip()
                    self.questions.append(question_text)

            # เก็บ Task
            if in_task_section and re.match(r"^\d+\.", line):
                task_detail = re.sub(r"^\d+\.\s*(\*\*Role:\*\*\s*)?[^\:]+:\s*", "", line).strip()
                current_task = task_detail
                self.tasks.append(current_task)

            # ต่อ Task ถ้าบรรทัดขึ้นต้นด้วย "*"
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
            aws = str(input("กรุณาใส่คำตอบของคุณ: "))
            self.awser.append(aws)
    def cleand_task(self,raw_tasks):
        pattern = re.compile(
                                r"^\*{0,2}\s*(Backend Developer|Frontend Developer|Project Manager \(PM\)|UX/UI Designer)\*{0,2}\s*:?\s*",
                                re.IGNORECASE
)

        for task in raw_tasks:
            cleaned = re.sub(pattern, "", task).strip()
            self.cleandtask.append(cleaned)
            
        return self.cleandtask
        

