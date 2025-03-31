import spacy
nlp = spacy.load('en_core_web_lg')

class Suitability:
    def __init__(self, ds_processor):
        # ใช้ instance ของ DatasetProcessor ผ่าน composition
        self.ds_processor = ds_processor
    
    def compute_suitability_scores(self, hr, task):
        scores = []

        for idx, row in hr.iterrows():
            candidate = row.get("Position", "").strip()
            print(f"\nProcessing {row.get('Name', '')} for position {candidate}")
            if candidate:
                similarities = self.compare_pos(candidate, task)
                weight_category = 0.5
                weight_performance = 0.5

                if similarities:
                    # similarities: list of tuples (category, similarity)
                    best_category, best_sim = max(similarities, key=lambda x: x[1])
                    Composite_score = best_sim * weight_category + row.get("performance_index", 0) * weight_performance
                else:
                    best_category, best_sim, Composite_score = None, 0, 0

                scores.append({
                    "Name": row.get("Name", ""),
                    "Position": candidate,
                    "Best_Category": best_category,
                    "Suitability_Score": best_sim,
                    "Composite_score": Composite_score
                })
            else:
                print("\nNo position found for the candidate")
                scores.append({
                    "Name": row.get("Name", ""),
                    "Position": "No position found",
                    "Best_Category": None,
                    "Suitability_Score": 0,
                    "Composite Score": 0
                })
        return scores

    def compare_pos(self, position, task):
        position_doc = nlp(position)
        similarities = []
        unique_categories = task['Category'].drop_duplicates()
        for category in unique_categories:
            category_doc = nlp(str(category))
            sim = position_doc.similarity(category_doc)
            similarities.append((category, sim))
        
        # เรียงลำดับ tuple โดย similarity จากมากไปน้อย
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities
