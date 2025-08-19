from PIL import Image, ImageDraw, ImageFont
import numpy as np

SYMBOLS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*")


def assign_symbols(palette):
    """Map each RGB color in the palette to a unique symbol."""
    if len(palette) > len(SYMBOLS):
        raise ValueError("Palette too large for available symbols")
    return {tuple(color): SYMBOLS[i] for i, color in enumerate(palette)}


def readable_text_color(rgb):
    """Return black or white depending on brightness for readability."""
    r, g, b = map(int, rgb)  # Convert to regular Python ints to avoid overflow
    brightness = (r*299 + g*587 + b*114) / 1000
    return (0, 0, 0) if brightness > 128 else (255, 255, 255)


def save_bitmap(pixels: np.ndarray, output_path: str, dmc_df, pixel_size: int = 20, legend_gap: int = 5):
    """Save the image as a bitmap with symbols and DMC color legend at the bottom."""
    h, w, _ = pixels.shape
    unique_colors = np.unique(pixels.reshape(-1, 3), axis=0)
    symbol_map = assign_symbols(unique_colors)

    # Map RGB -> DMC floss number
    rgb_to_floss = {}
    for color in unique_colors:
        row = dmc_df[(dmc_df['Red'] == color[0]) &
                     (dmc_df['Green'] == color[1]) &
                     (dmc_df['Blue'] == color[2])]
        floss_num = row.iloc[0]['Floss#'] if not row.empty else "?"
        rgb_to_floss[tuple(color)] = floss_num

    # Legend height
    legend_height = len(unique_colors) * (pixel_size + legend_gap) + pixel_size
    img = Image.new("RGB", (w*pixel_size, h*pixel_size + legend_height), "white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    # Draw main grid
    for y in range(h):
        for x in range(w):
            color = tuple(int(c) for c in pixels[y, x])
            symbol = symbol_map[color]
            # Rectangle

            draw.rectangle([x*pixel_size, y*pixel_size, (x+1)*pixel_size, (y+1)*pixel_size],
                           fill=color, outline=(0,0,0))
            # Symbol
            text_color = readable_text_color(color)
            bbox = font.getbbox(symbol)
            w_text = bbox[2] - bbox[0]
            h_text = bbox[3] - bbox[1]
            draw.text((x*pixel_size + (pixel_size - w_text)/2, y*pixel_size + (pixel_size - h_text)/2),
                      symbol, fill=text_color, font=font)

    # Draw legend background
    draw.rectangle([0, h*pixel_size, w*pixel_size, h*pixel_size + legend_height], fill=(240,240,240))

    # Draw legend items
    for i, color in enumerate(unique_colors):
        color = tuple(
            int(c) for c in color  # Ensure RGB values are integers
        )
        symbol = symbol_map[tuple(color)]
        floss_num = rgb_to_floss[tuple(color)]
        y_pos = h*pixel_size + i * (pixel_size + legend_gap)
        # Color square
        draw.rectangle([0, y_pos, pixel_size, y_pos+pixel_size], fill=color, outline=(0,0,0))
        # Symbol
        bbox = font.getbbox(symbol)
        w_text = bbox[2] - bbox[0]
        h_text = bbox[3] - bbox[1]
        draw.text((pixel_size*1.5, y_pos + (pixel_size - h_text)/2), symbol,
                  fill=(0,0,0), font=font)
        # Floss #
        bbox_floss = font.getbbox(str(floss_num))
        h_floss = bbox_floss[3] - bbox_floss[1]
        draw.text((pixel_size*4, y_pos + (pixel_size - h_floss)/2), str(floss_num), fill=(0,0,0), font=font)

    img.save(output_path)
    print(f"Bitmap saved to {output_path}")
