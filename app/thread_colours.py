import pandas as pd


def load_dmc_dataframe(csv_path: str) -> pd.DataFrame:
    """
    Reads a CSV of DMC floss colors into a pandas DataFrame.

    Expected columns:
        "Floss#", "Description", "Red", "Green", "Blue"

    Args:
        csv_path: Path to the CSV file.

    Returns:
        pandas DataFrame with the DMC color data.
    """
    df = pd.read_csv(csv_path)

    # Ensure RGB values are integers (just in case CSV reads them as floats)
    df[["Red", "Green", "Blue"]] = df[["Red", "Green", "Blue"]].astype(int)

    return df
