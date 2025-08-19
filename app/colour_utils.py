import numpy as np
from sklearn.cluster import KMeans
from skimage import color
from scipy.spatial import distance


def map_to_dmc(clustered_pixels: np.ndarray, dmc_df) -> np.ndarray:
    """
    Replace each color in clustered_pixels with the nearest DMC color.
    dmc_df: pandas DataFrame with columns 'R', 'G', 'B' for DMC colors.
    """
    h, w, _ = clustered_pixels.shape
    flat_pixels = clustered_pixels.reshape(-1, 3)

    dmc_colors = dmc_df[['Red', 'Green', 'Blue']].values

    # For each pixel, find nearest DMC color
    nearest_indices = distance.cdist(flat_pixels, dmc_colors).argmin(axis=1)
    mapped_pixels = dmc_colors[nearest_indices].reshape(h, w, 3).astype(np.uint8)

    return mapped_pixels


def find_distinct_colours(pixels: np.ndarray, n_colors: int = 5) -> np.ndarray:
    """
    Cluster pixels into n_colors using KMeans in LAB space for perceptual distinctness.
    Returns only the clustered image.
    """
    h, w, _ = pixels.shape
    flat_pixels = pixels.reshape(-1, 3)

    # Convert to LAB (better for perceptual clustering)
    lab_pixels = color.rgb2lab(flat_pixels.reshape(-1, 1, 3) / 255.0).reshape(-1, 3)

    # KMeans clustering
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    kmeans.fit(lab_pixels)

    # Convert cluster centers back to RGB
    lab_centers = kmeans.cluster_centers_.reshape(-1, 1, 3)
    rgb_centers = (color.lab2rgb(lab_centers) * 255).astype(np.uint8).reshape(-1, 3)

    # Assign each pixel to nearest center
    labels = kmeans.labels_
    clustered_pixels = rgb_centers[labels].reshape(h, w, 3)

    return clustered_pixels
