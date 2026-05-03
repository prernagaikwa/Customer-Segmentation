
# from flask import Flask, request, send_file, render_template, jsonify
# from flask_cors import CORS
# import pandas as pd
# from sklearn.preprocessing import LabelEncoder
# from sklearn.cluster import KMeans
# import matplotlib.pyplot as plt
# import io
# import base64
# import seaborn as sns

# app = Flask(__name__)
# CORS(app)  # Allow CORS for frontend requests



# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/choosefile")
# def choosefile():
#     return render_template("choosefile.html")


# def create_base64_image():
#     buf = io.BytesIO()
#     plt.savefig(buf, format='png', bbox_inches='tight')  # Ensure we don't use show()
#     buf.seek(0)
#     encoded = base64.b64encode(buf.read()).decode('utf-8')
#     buf.close()
#     plt.close()  # Close the plot to free resources
#     return encoded






# # 👉 Add your insights function here
# def generate_insights(df):
#     insights = {}

#     # Age Distribution
#     common_age = df['Age'].mode()[0]
#     insights['age_distribution'] = f"Most customers are around {common_age} years old. Focus marketing on this age group."

#     # Gender Distribution
#     male_count = (df['Gender'] == 1).sum()
#     female_count = (df['Gender'] == 0).sum()
#     if male_count > female_count:
#         insights['gender_pie'] = "Majority of customers are male. Campaigns should slightly lean towards male preferences."
#     else:
#         insights['gender_pie'] = "Majority of customers are female. Campaigns should slightly lean towards female preferences."

#     # Income vs Spending
#     avg_income = df['Income'].mean()
#     avg_spending = df['Spending Score'].mean()
#     insights['income_spending_heatmap'] = f"Average income is {avg_income:.0f} and average spending score is {avg_spending:.0f}. Higher income customers tend to spend more."

#     # Segmentation
#     insights['segmentation'] = "Clusters show different customer groups: price-sensitive, middle-tier, and premium. Each needs tailored offers."

#     # Spending vs Age
#     insights['spending_vs_age'] = "Spending varies with age. Older customers show higher spending in some cases, suggesting premium offers for them."

#     return insights








# @app.route('/segment', methods=['POST', 'GET'])
# def segment_customers():
#     if 'file' not in request.files:
#         return 'No file uploaded', 400

#     file = request.files['file']
#     if file.filename == '':
#         return 'No file selected', 400

#     try:
#         df = pd.read_csv(file)
#     except Exception as e:
#         return f'Error reading the CSV file: {e}', 400

#     required_columns = ['Age', 'Gender', 'Income', 'Spending Score']
#     if not all(col in df.columns for col in required_columns):
#         return f'CSV must contain the following columns: {", ".join(required_columns)}', 400

#     if df.shape[0] < 3:
#         return 'Insufficient data for clustering.', 400

#     try:
#         df['Gender'] = LabelEncoder().fit_transform(df['Gender'])

#         # Run KMeans clustering
#         kmeans = KMeans(n_clusters=3, random_state=42)
#         df['Cluster'] = kmeans.fit_predict(df[['Age', 'Gender', 'Income', 'Spending Score']])

#         graphs = {}

#         # 1. Customer Segmentation Scatter Plot
#         plt.figure(figsize=(6, 5))
#         for cluster in df['Cluster'].unique():
#             cluster_data = df[df['Cluster'] == cluster]
#             plt.scatter(cluster_data['Income'], cluster_data['Spending Score'], label=f'Cluster {cluster}')
#         plt.xlabel('Income')
#         plt.ylabel('Spending Score')
#         plt.title('Customer Segmentation')
#         plt.legend()
#         graphs['segmentation'] = create_base64_image()

#         # 2. Age Distribution
#         plt.figure(figsize=(6, 4))
#         df['Age'].hist(bins=10, color='skyblue')
#         plt.title('Age Distribution')
#         plt.xlabel('Age')
#         plt.ylabel('Count')
#         graphs['age_distribution'] = create_base64_image()

#         # 3. Gender Distribution Pie Chart
#         gender_counts = df['Gender'].value_counts()
#         plt.figure(figsize=(5, 5))
#         plt.pie(gender_counts, labels=['Male', 'Female'], autopct='%1.1f%%', startangle=140)
#         plt.title('Gender Distribution')
#         graphs['gender_pie'] = create_base64_image()

#         # 4. Spending Score vs Age
#         plt.figure(figsize=(6, 5))
#         plt.scatter(df['Age'], df['Spending Score'], c='green')
#         plt.xlabel('Age')
#         plt.ylabel('Spending Score')
#         plt.title('Spending Score vs Age')
#         graphs['spending_vs_age'] = create_base64_image()

# #         # 5. Income vs Spending Score (Heatmap style)
# #         plt.figure(figsize=(6, 5))
# #         sns.kdeplot(data=df, x="Income", y="Spending Score", fill=True, cmap="coolwarm")
# #         plt.title('Income vs Spending Score Density')
# #         graphs['income_spending_heatmap'] = create_base64_image()

# # #         return jsonify(graphs)

# # #     except Exception as e:
# # #         print(f"Error during processing: {e}")
# # #         return f'Error during segmentation: {e}', 500

# # # if __name__ == '__main__':
# # #     app.run(debug=True, port=5000)


# # # 👉 Generate insights
# # insights = generate_insights(df)

# # # 👉 Return both graphs and insights together
# # return jsonify({"graphs": graphs, "insights": insights})


#         # 5. Income vs Spending Score (Heatmap style)
#         plt.figure(figsize=(6, 5))
#         sns.kdeplot(data=df, x="Income", y="Spending Score", fill=True, cmap="coolwarm")
#         plt.title('Income vs Spending Score Density')
#         graphs['income_spending_heatmap'] = create_base64_image()

#         insights = generate_insights(df)
# return render_template("index.html", graphs=graphs, insights=insights)

#     except Exception as e:
#         print(f"Error during processing: {e}")
#         return f'Error during segmentation: {e}', 500

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)






import matplotlib
matplotlib.use('Agg')

from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
import io
import base64
import seaborn as sns
import matplotlib.pyplot as plt

# Create app
app = Flask(__name__)
CORS(app)

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/choosefile")
def choosefile():
    return render_template("choosefile.html")


# Convert graph to base64
def create_base64_image():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()
    return encoded


# Segmentation API
@app.route('/segment', methods=['POST'])
def segment_customers():

    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']

    try:
        df = pd.read_csv(file)
    except Exception as e:
        return f"CSV Error: {e}", 400

    required_columns = ['Age', 'Gender', 'Income', 'Spending Score']
    if not all(col in df.columns for col in required_columns):
        return f"CSV must contain: {', '.join(required_columns)}", 400

    try:
        # Convert Gender to numeric
        df['Gender'] = LabelEncoder().fit_transform(df['Gender'])

        # Apply KMeans
        kmeans = KMeans(n_clusters=3, random_state=42)
        df['Cluster'] = kmeans.fit_predict(df[['Age', 'Gender', 'Income', 'Spending Score']])

        graphs = {}

        # 1. Segmentation
        plt.figure(figsize=(6, 5))
        for cluster in df['Cluster'].unique():
            cluster_data = df[df['Cluster'] == cluster]
            plt.scatter(cluster_data['Income'], cluster_data['Spending Score'], label=f'Cluster {cluster}')
        plt.xlabel('Income')
        plt.ylabel('Spending Score')
        plt.title('Customer Segmentation')
        plt.legend()
        graphs['segmentation'] = create_base64_image()

        # 2. Age Distribution
        plt.figure(figsize=(6, 4))
        df['Age'].hist(bins=10, color='skyblue')
        plt.title('Age Distribution')
        graphs['age_distribution'] = create_base64_image()

        # 3. Gender Pie
        plt.figure(figsize=(5, 5))
        df['Gender'].value_counts().plot.pie(autopct='%1.1f%%')
        plt.title('Gender Distribution')
        graphs['gender_pie'] = create_base64_image()

        # 4. Spending vs Age
        plt.figure(figsize=(6, 5))
        plt.scatter(df['Age'], df['Spending Score'], c='green')
        plt.title('Spending vs Age')
        graphs['spending_vs_age'] = create_base64_image()

        # 5. Income vs Spending
        plt.figure(figsize=(6, 5))
        sns.kdeplot(data=df, x="Income", y="Spending Score", fill=True, cmap="coolwarm")
        plt.title('Income vs Spending')
        graphs['income_spending_heatmap'] = create_base64_image()

        # ✅ IMPORTANT: return JSON (NOT HTML)
        return jsonify(graphs)

    except Exception as e:
        print("Error:", e)
        return f"Error: {e}", 500


# Run app
if __name__ == "__main__":
    # app.run(debug=True)
     app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))