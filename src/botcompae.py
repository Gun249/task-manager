from sentence_transformers import util
from sentence_transformers import SentenceTransformer
class botcompae:
    def __init__(self):
        self.model_path = SentenceTransformer("models/role_task_siamese_v1")

    def model(self, Role, Tasks):
        for i in range(len(Tasks)):
            role_emb = self.model_path.encode(Role, convert_to_tensor=True)
            task_emb = self.model_path.encode(Tasks[i], convert_to_tensor=True)
            similarities = util.cos_sim(role_emb, task_emb)
            if similarities >= 0.7:
                print(f"\nYou are suitable for this task: {Tasks[i]}")
        print("Thank you for using our service.")
        print("Have a nice day!")
            