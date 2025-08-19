from PIL import Image
from app.image_utils import resize_max, image_to_array
from app.colour_utils import find_distinct_colours, map_to_dmc
from app.output_utils import save_bitmap
from app.thread_colours import load_dmc_dataframe


def cross_stitch_svg(input_path: str, output_path: str, n_colors: int = 5,
                     max_dim: int = 100, pixel_size: int = 20):
    """Full pipeline: resize, extract colors, map to DMC, and save as SVG."""
    # Load and resize image
    img = Image.open(input_path).convert("RGB")
    img_small = resize_max(img, max_dim)
    pixels = image_to_array(img_small)

    # Cluster pixels
    clustered_pixels = find_distinct_colours(pixels, n_colors=n_colors)

    #save_svg(clustered_pixels, "app/outputs/stage_1.svg", pixel_size=pixel_size)

    # Load DMC colors
    dmc_df = load_dmc_dataframe(
        "app/inputs/dmc_colours.csv"
    )

    # Map clustered colors to nearest DMC
    dmc_pixels = map_to_dmc(clustered_pixels, dmc_df)

    # Save as SVG
    save_bitmap(dmc_pixels, output_path, dmc_df, pixel_size=pixel_size)


if __name__ == "__main__":

    INPUT_PATH = "app/inputs/input.png"
    OUTPUT_PATH = "app/outputs/output.png"
    N_COLOURS = 5
    cross_stitch_svg(
        INPUT_PATH,
        OUTPUT_PATH,
        n_colors=N_COLOURS,
        max_dim=90,
        pixel_size=20
    )
