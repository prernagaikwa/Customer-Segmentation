import pandas as pd
import random

data = []

genders = ["Male", "Female"]
income_ranges = [15000, 35000, 75000, 120000]

for i in range(1, 501):
    customer = {
        "CustomerID": i,
        "Age": random.randint(18, 65),
        "Gender": random.choice(genders),
        "Income": random.choice(income_ranges),
        "Spending Score": random.randint(1, 100)
    }
    data.append(customer)

df = pd.DataFrame(data)
df.to_csv("customers_500.csv", index=False)

print("✅ 500 records generated successfully!")