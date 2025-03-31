from sklearn.model_selection import train_test_split

class DataSplitter:
    def __init__(self):
        pass


    def data_split(self, hr):
        # แบ่งข้อมูลเป็น train และ test ด้วยสัดส่วน 80:20
        
        X = hr.drop(columns=["Composite_score"],axis=1)
        y = hr["Composite_score"]

        trainx, testx = train_test_split(X, test_size=0.2, random_state=42)

        return trainx, testx
    