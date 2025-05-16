import logging
from sentence_transformers import util, SentenceTransformer

# กำหนดค่าเริ่มต้นสำหรับการ logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RoleTaskMatcher:
    """
    คลาสสำหรับจับคู่คำอธิบาย Role กับรายการ Tasks โดยใช้ความคล้ายคลึงของประโยค
    """
    DEFAULT_MODEL_PATH = "models/role_task_siamese_v1" 
    DEFAULT_SIMILARITY_THRESHOLD = 0.4  

    def __init__(self, model_path: str = None, similarity_threshold: float = None):
        """
        เมธอด (constructor) ของคลาส RoleTaskMatcher

        Args:
            model_path (str, optional): Path ไปยัง directory ของโมเดล SentenceTransformer ที่เก็บไว้ในเครื่อง
                                        หากไม่กำหนด จะใช้ค่าจาก DEFAULT_MODEL_PATH
            similarity_threshold (float, optional): ค่าคะแนนความคล้ายคลึง (cosine similarity) ขั้นต่ำ
                                                    ที่ถือว่า task นั้นเหมาะสมกับ role หากไม่กำหนด จะใช้ค่าจาก
                                                    DEFAULT_SIMILARITY_THRESHOLD
        """
        self.model_path = model_path if model_path is not None else self.DEFAULT_MODEL_PATH
        self.similarity_threshold = similarity_threshold if similarity_threshold is not None else self.DEFAULT_SIMILARITY_THRESHOLD
        self.st_model = None  

        try:
            # โหลดโมเดล Siamese สำหรับเปรียบเทียบความเหมือนของข้อความ
            # โดยคาดหวังว่าโมเดลจะถูกเก็บไว้ในเครื่องตาม path ที่ระบุ
            self.st_model = SentenceTransformer(
                self.model_path, local_files_only=True
            )
            logging.info(f"โหลดโมเดลสำเร็จจาก: {self.model_path}")
        except Exception as e:
            logging.error(f"เกิดข้อผิดพลาดในการโหลดโมเดลจาก '{self.model_path}': {e}")


    def find_suitable_tasks(self, role_description: str, tasks: list[str]) -> list[tuple[str, float]]:
        """
        ค้นหา tasks ที่เหมาะสมสำหรับ role ที่กำหนด โดยอิงจากความคล้ายคลึงทางความหมาย

        Args:
            role_description (str): คำอธิบายของ role
            tasks (list[str]): รายการของคำอธิบาย tasks

        Returns:
            list[tuple[str, float]]: รายการของ tuples โดยแต่ละ tuple ประกอบด้วย
                                     task ที่เหมาะสม (str) และคะแนนความคล้ายคลึง (float)
                                     จะคืนค่าเป็น list ว่างหากไม่พบ tasks ที่เหมาะสม
                                     หรือเกิดข้อผิดพลาดร้ายแรง (เช่น โมเดลโหลดไม่สำเร็จ)
        """
        if self.st_model is None:
            logging.error("โมเดลยังไม่ได้ถูกโหลด ไม่สามารถทำการจับคู่ task ได้")
            return []

        if not role_description:
            logging.warning("คำอธิบาย Role ว่างเปล่า ไม่สามารถทำการจับคู่ได้")
            return []
        if not tasks:
            logging.warning("รายการ Tasks ว่างเปล่า ไม่มี task ให้จับคู่")
            return []

        # กรอง tasks ที่เป็นค่าว่างหรือมีแต่ช่องว่างออกไปก่อน
        valid_tasks = [task for task in tasks if task and task.strip()]
        suitable_matches = []  # เก็บผลลัพธ์ tasks ที่เหมาะสม

        try:
            # แปลง Role เป็น embedding vector
            role_embedding = self.st_model.encode(role_description, convert_to_tensor=True)
        except Exception as e:
            logging.error(f"เกิดข้อผิดพลาดในการ encode Role '{role_description}': {e}")
            return []

        try:
            task_embeddings = self.st_model.encode(valid_tasks, convert_to_tensor=True)
        except Exception as e:
            logging.error(f"เกิดข้อผิดพลาดในการ encode Tasks: {e}")
            return []

        # ตรวจสอบว่าการ encode ได้ผลลัพธ์ที่ถูกต้อง
        if role_embedding is None or task_embeddings is None or len(task_embeddings) == 0:
            logging.error("ไม่สามารถสร้าง embeddings สำหรับ role หรือ tasks ได้")
            return []

        try:
            cosine_scores = util.cos_sim(role_embedding, task_embeddings)

            if cosine_scores.ndim == 2 and cosine_scores.shape[0] == 1:
                scores_tensor = cosine_scores[0]
            elif cosine_scores.ndim == 1:
                scores_tensor = cosine_scores
            else:
                logging.error(f"ขนาดของ tensor cosine_scores ไม่เป็นไปตามที่คาดไว้: {cosine_scores.shape}")
                return []

        except Exception as e:
            logging.error(f"เกิดข้อผิดพลาดในการคำนวณ cosine similarity: {e}")
            return []

        # วนลูปเช็คแต่ละ task และคะแนนความคล้ายคลึง
        for i, task_text in enumerate(valid_tasks):
            try:
                sim_value = scores_tensor[i].item()  # ดึงค่า similarity ออกมาเป็น float
                # ถ้า similarity สูงกว่า threshold ที่กำหนดไว้ ถือว่าเหมาะสม
                if sim_value >= self.similarity_threshold:
                    suitable_matches.append((task_text, sim_value))
            except IndexError: 
                logging.error(f"เกิด IndexError ขณะเข้าถึงคะแนนความคล้ายคลึงสำหรับ task '{task_text}'. "
                              f"ความยาว scores: {len(scores_tensor)}, index: {i}")
            except Exception as e:
                logging.error(f"เกิดข้อผิดพลาดในการประมวลผลความคล้ายคลึงสำหรับ task '{task_text}': {e}")

        if not suitable_matches:
            logging.info(f"ไม่พบ task ที่เหมาะสมสำหรับ Role '{role_description}' ด้วย threshold {self.similarity_threshold}")
        else:
            logging.info(f"พบ {len(suitable_matches)} task(s) ที่เหมาะสมสำหรับ Role '{role_description}'.")

        return suitable_matches