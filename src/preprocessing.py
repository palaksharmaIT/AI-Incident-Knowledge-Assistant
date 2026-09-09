import pandas as pd


def load_data(path):
    df = pd.read_csv(path)

    print("Original shape:", df.shape)

    return df


def preprocess_data(df):

    # Remove duplicate records
    df = df.drop_duplicates()

    # Remove rows with missing important values
    df = df.dropna(
        subset=[
            "title",
            "description",
            "root_cause",
            "resolution",
            "category"
        ]
    )

    # Clean text columns
    text_columns = [
        "title",
        "description",
        "root_cause",
        "resolution"
    ]

    for column in text_columns:
        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
            .str.lower()
        )

    # Create combined text for ML and RAG
    df["text"] = (
        df["title"] + " "
        + df["description"] + " "
        + df["root_cause"] + " "
        + df["resolution"]
    )

    print("Processed shape:", df.shape)

    print("\nCategory distribution:")
    print(df["category"].value_counts())

    return df


if __name__ == "__main__":

    df = load_data("data/incidents.csv")

    df = preprocess_data(df)

    # Save processed dataset
    df.to_csv(
        "data/processed_incidents.csv",
        index=False
    )

    print("\nProcessed data saved.")

    print("\nSample processed data:")
    print(
        df[["title", "text", "category"]].head()
    )