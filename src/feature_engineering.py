class feature_enginerr:
    def __init__(self,df, file_name):
        self.df = df
        self.file_name = file_name
    def feature_engineering_performance(self):
        # กำหนดคอลัมน์ที่จำเป็นต้องมีสำหรับการคำนวณ performance index
        required_columns = ['Projects Completed', 'Productivity (%)', 'Satisfaction Rate (%)', 'Feedback Score']
        if all(col in self.df.columns for col in required_columns):
            # คำนวณ normalized values ด้วยสูตร Min-Max Scaling
            self.df['Proj_norm'] = (self.df['Projects Completed'] - self.df['Projects Completed'].min()) / (self.df['Projects Completed'].max() - self.df['Projects Completed'].min())
            self.df['Prod_norm'] = (self.df['Productivity (%)'] - self.df['Productivity (%)'].min()) / (self.df['Productivity (%)'].max() - self.df['Productivity (%)'].min())
            self.df['Sat_norm'] = (self.df['Satisfaction Rate (%)'] - self.df['Satisfaction Rate (%)'].min()) / (self.df['Satisfaction Rate (%)'].max() - self.df['Satisfaction Rate (%)'].min())
            self.df['Feed_norm'] = (self.df['Feedback Score'] - self.df['Feedback Score'].min()) / (self.df['Feedback Score'].max() - self.df['Feedback Score'].min())
            
            # กำหนดน้ำหนักสำหรับแต่ละฟีเจอร์
            weight_proj = 0.3
            weight_prod = 0.35
            weight_sat = 0.25
            weight_feed = 0.1
            
            # คำนวณ performance_index โดยรวม normalized value เข้าด้วยกัน
            self.df['performance_index'] = (self.df['Proj_norm'] * weight_proj +
                                       self.df['Prod_norm'] * weight_prod +
                                       self.df['Sat_norm'] * weight_sat +
                                       self.df['Feed_norm'] * weight_feed)
            print(f"\nFile {self.file_name} has successfully undergone Feature Engineering")
            return self.df
        else:
            print("\nFeature Engineering not required")
            return self.df