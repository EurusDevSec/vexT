import pandas as pd
import numpy as np 
# from sentence_transformer import SentenceTransformer
import os

#CONFIG

# print("Loading model AI... ")
# model = SentenceTransformer('all-MiniLM-L6-v2')


dir_script = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path= os.path.join(dir_script,"res", "products.csv")

# print(csv_path)
def normalize_data(file_path):
    # df = pd.DataFrame(file_path)
    # print(df.head())
    
    df =pd.read_csv(file_path)
    print(df)
    df["category"] = df["category"].fillna("Unknown")
    df["title"] = df["title"].fillna("Unknown")

    # Clear garbage
    
    print(df["category"])
    df["category"] = df["category"].apply(lambda x: str(x).strip().title())
    print(df["category"])
    
  


def main():
    normalize_data(file_path)
    
    




if __name__ == "__main__":
    main()