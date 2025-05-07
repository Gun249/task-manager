from sentence_transformers import util, SentenceTransformer

class botcompae:
    def __init__(self):
        try:
            # โหลดโมเดล Siamese สำหรับเปรียบเทียบความเหมือนของข้อความ
            # ถ้ามีไฟล์โมเดลในโฟลเดอร์ models ให้โหลดแบบ offline
            self.model_path = SentenceTransformer(
                "models/role_task_siamese_v1", local_files_only=True
            )
        except Exception as e:
            # กรณีโหลดโมเดลไม่สำเร็จ ให้แจ้ง error แล้วเซ็ตเป็น None
            print(f"Error loading model: {e}")
            self.model_path = None

    def model(self, Role, Tasks):
        # ตรวจสอบว่าโมเดลถูกโหลดสำเร็จหรือไม่
        if self.model_path is None:
            print("Model is not loaded successfully. Exiting model matching.")
            return

        # ตรวจสอบว่าได้รับ Role และ Tasks มาไม่เป็นค่าว่าง
        if not Role or not Tasks:
            print("Invalid input: Role or Tasks is empty.")
            return

        try:
            # แปลง Role เป็น embedding vector
            role_emb = self.model_path.encode(Role, convert_to_tensor=True)
        except Exception as e:
            print(f"Error encoding Role '{Role}': {e}")
            return

        if role_emb is None:
            # ถ้า embedding กลับมาเป็น None ให้หยุดการทำงาน
            print("Role embedding is None. Exiting.")
            return

        found_suitable = False  # ธงว่าพบงานที่เหมาะสมหรือไม่

        # วนลูปเช็คแต่ละ task
        for i, task in enumerate(Tasks):
            try:
                if not task:
                    # งานว่างข้ามไปเลย
                    print(f"Task at index {i} is empty. Skipping.")
                    continue

                # แปลง task เป็น embedding vector
                task_emb = self.model_path.encode(task, convert_to_tensor=True)
            except Exception as e:
                print(f"Error encoding Task '{task}': {e}")
                continue

            try:
                # คำนวณ cosine similarity ระหว่าง Role และ task
                similarities = util.cos_sim(role_emb, task_emb)
            except Exception as e:
                print(f"Error computing cosine similarity for Task '{task}': {e}")
                continue

            try:
                # ดึงค่า similarity ออกมาเป็น float
                sim_value = similarities.item() if similarities.numel() == 1 else None
                if sim_value is None:
                    print(f"Unexpected similarity tensor shape for Task '{task}'. Skipping.")
                    continue
            except Exception as e:
                print(f"Error converting similarity to scalar for Task '{task}': {e}")
                continue

            # ถ้า similarity สูงกว่า threshold (0.7) ถือว่าเหมาะสม
            if sim_value >= 0.7:
                print(f"\nYou are suitable for this task: {task}")
                found_suitable = True

        if not found_suitable:
            # ถ้าไม่พบงานไหนเหมาะสมเลย
            print("No suitable tasks found for this Role.")
        print("\nThank you for using our service.")
        print("Have a nice day!")

