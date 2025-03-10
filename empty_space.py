import pdfplumber
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def find_top_and_bottom_empty_space_with_visuals(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            page_height = page.height
            page_width = page.width

            # Gather content bounding boxes (text + images)
            y_tops = []
            y_bottoms = []

            # Extract words
            words = page.extract_words()
            for word in words:
                y_tops.append(float(word['top']))
                y_bottoms.append(float(word['bottom']))

            # Extract images
            images = page.images
            for img in images:
                y_tops.append(float(img['y0']))  # top of image
                y_bottoms.append(float(img['y1']))  # bottom of image

            if not y_tops or not y_bottoms:
                print(f"Page {page_num}: No content found.")
                print(f"  - Top Empty Space: 100%")
                print(f"  - Bottom Empty Space: 100%")
                continue

            # Topmost Y is the smallest y_tops (closer to top of page)
            topmost_y = min(y_tops)
            bottommost_y = max(y_bottoms)

            # Top empty space = space from top of page to topmost content
            top_empty_space_percent = (page_height - topmost_y) / page_height * 100

            # Bottom empty space = space from bottom of page to bottommost content
            bottom_empty_space_percent = bottommost_y / page_height * 100

            print(f"Page {page_num}:")
            print(f"  - Top Empty Space: {top_empty_space_percent:.2f}% of page height")
            print(f"  - Bottom Empty Space: {bottom_empty_space_percent:.2f}% of page height")
            print("-" * 40)

            # --- Visualization ---
            fig, ax = plt.subplots(figsize=(6, 8))

            # Draw the full page boundary
            ax.add_patch(Rectangle((0, 0), page_width, page_height, linewidth=1, edgecolor='black', facecolor='none'))

            # Draw the content area (red box)
            content_height = bottommost_y - topmost_y
            ax.add_patch(Rectangle((0, topmost_y), page_width, content_height, linewidth=2, edgecolor='red', facecolor='none', label='Content Area'))

            # Highlight the top empty space (yellow)
            ax.add_patch(Rectangle((0, topmost_y), page_width, page_height - topmost_y, linewidth=0, facecolor='yellow', alpha=0.3, label='Top Empty Space'))

            # Highlight the bottom empty space (cyan)
            ax.add_patch(Rectangle((0, 0), page_width, bottommost_y, linewidth=0, facecolor='cyan', alpha=0.3, label='Bottom Empty Space'))

            # Plot settings
            ax.set_title(f"Page {page_num} - Empty Space Visualization")
            ax.set_xlim(0, page_width)
            ax.set_ylim(0, page_height)
            ax.invert_yaxis()  # Because PDF coordinate origin is bottom-left
            ax.set_aspect('equal')

            # Custom legend
            handles = [
                Rectangle((0, 0), 1, 1, color='yellow', alpha=0.3),
                Rectangle((0, 0), 1, 1, color='cyan', alpha=0.3),
                Rectangle((0, 0), 1, 1, color='red', fill=False, edgecolor='red', linewidth=2)
            ]
            labels = ['Top Empty Space', 'Bottom Empty Space', 'Content Area']
            ax.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, -0.1), ncol=3)

            plt.show()

# Example usage
find_top_and_bottom_empty_space_with_visuals(r"C:\Users\Prakash Nani\Desktop\New folder\ai_pro\testing.pdf")
