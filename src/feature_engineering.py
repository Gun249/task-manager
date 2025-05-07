class feature_enginerr:
    def __init__(self, df, file_name):
        # เก็บ DataFrame และชื่อไฟล์ต้นทาง
        self.df = df
        self.file_name = file_name

    def feature_engineering_performance(self):
        """
        สร้างฟีเจอร์ performance_index จากคอลัมน์เดิม:
        1. ตรวจสอบว่ามีคอลัมน์สำคัญครบหรือไม่
        2. ทำ Min-Max Scaling ให้แต่ละคอลัมน์
        3. ผสม weighted sum เพื่อคำนวณ performance_index
        """

        # รายชื่อคอลัมน์ที่ต้องมีสำหรับคำนวณ
        required_columns = [
            'Projects Completed',
            'Productivity (%)',
            'Satisfaction Rate (%)',
            'Feedback Score'
        ]

        # ถ้ามีครบทุกคอลัมน์
        if all(col in self.df.columns for col in required_columns):
            # 1. Min-Max Scaling แต่ละคอลัมน์ -> เก็บในคอลัมน์ใหม่
            self.df['Proj_norm'] = (
                self.df['Projects Completed'] - self.df['Projects Completed'].min()
            ) / (
                self.df['Projects Completed'].max() - self.df['Projects Completed'].min()
            )
            self.df['Prod_norm'] = (
                self.df['Productivity (%)'] - self.df['Productivity (%)'].min()
            ) / (
                self.df['Productivity (%)'].max() - self.df['Productivity (%)'].min()
            )
            self.df['Sat_norm'] = (
                self.df['Satisfaction Rate (%)'] - self.df['Satisfaction Rate (%)'].min()
            ) / (
                self.df['Satisfaction Rate (%)'].max() - self.df['Satisfaction Rate (%)'].min()
            )
            self.df['Feed_norm'] = (
                self.df['Feedback Score'] - self.df['Feedback Score'].min()
            ) / (
                self.df['Feedback Score'].max() - self.df['Feedback Score'].min()
            )

            # 2. ลบคอลัมน์ดิบออกเพื่อลดความซ้ำซ้อน
            self.df.drop(
                columns=required_columns,
                inplace=True,
                axis=1
            )

            # 3. กำหนดน้ำหนักให้แต่ละฟีเจอร์ (รวมเป็น 1.0)
            weight_proj = 0.3
            weight_prod = 0.35
            weight_sat = 0.25
            weight_feed = 0.1

            # 4. คำนวณ performance_index โดย weighted sum
            self.df['performance_index'] = (
                self.df['Proj_norm'] * weight_proj +
                self.df['Prod_norm'] * weight_prod +
                self.df['Sat_norm'] * weight_sat +
                self.df['Feed_norm'] * weight_feed
            )

            # แจ้งสำเร็จและคืน DataFrame ที่ปรับแล้ว
            print(f"\nFile {self.file_name} has successfully undergone Feature Engineering")
            return self.df

        else:
            # ถ้าไม่พบคอลัมน์ทั้งหมด -> ไม่ต้องทำอะไร คืน DataFrame เดิม
            print("\nFeature Engineering not required")
            return self.df