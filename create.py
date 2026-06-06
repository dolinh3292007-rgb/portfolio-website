"""
Script tạo ảnh placeholder cho portfolio
Chạy file này để tạo ảnh mẫu cho các bài tập
"""

import os

def create_svg_placeholder(path, text, bg_color="#2ecc71", width=800, height=400):
    """Tạo file SVG placeholder đơn giản"""
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{bg_color};stop-opacity:1" />
      <stop offset="100%" style="stop-color:#27ae60;stop-opacity:1" />
    </linearGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="{width}" height="{height}" fill="url(#grad)"/>
  <rect width="{width}" height="{height}" fill="url(#grid)"/>
  <rect x="20" y="20" width="{width-40}" height="{height-40}" rx="12" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="1" stroke-dasharray="8,4"/>
  <text x="{width//2}" y="{height//2 - 20}" font-family="Arial, sans-serif" font-size="36" font-weight="bold" fill="white" text-anchor="middle">{text}</text>
  <text x="{width//2}" y="{height//2 + 20}" font-family="Arial, sans-serif" font-size="16" fill="rgba(255,255,255,0.75)" text-anchor="middle">Hình ảnh minh chứng bài tập</text>
  <text x="{width//2}" y="{height//2 + 50}" font-family="Arial, sans-serif" font-size="13" fill="rgba(255,255,255,0.5)" text-anchor="middle">Thay thế bằng ảnh thực của bạn</text>
</svg>'''
    with open(path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"Đã tạo: {path}")


def create_placeholder_png(path, text, bg_color=(46, 204, 113)):
    """Tạo ảnh PNG placeholder (cần Pillow)"""
    try:
        from PIL import Image, ImageDraw, ImageFont

        width, height = 800, 400

        # Ensure bg_color is an RGB tuple
        if isinstance(bg_color, tuple) and len(bg_color) == 3:
            bg_rgba = (*bg_color, 255)
        elif isinstance(bg_color, str):
            # fallback if color is a hex string
            try:
                bg_color = bg_color.lstrip('#')
                bg_rgba = tuple(int(bg_color[i:i+2], 16) for i in (0, 2, 4)) + (255,)
            except Exception:
                bg_rgba = (46, 204, 113, 255)
        else:
            bg_rgba = (46, 204, 113, 255)

        img = Image.new('RGBA', (width, height), color=bg_rgba)
        draw = ImageDraw.Draw(img, 'RGBA')

        # Vẽ lưới nền (sử dụng alpha nhỏ)
        for x in range(0, width, 40):
            draw.line([(x, 0), (x, height)], fill=(255, 255, 255, 25), width=1)
        for y in range(0, height, 40):
            draw.line([(0, y), (width, y)], fill=(255, 255, 255, 25), width=1)

        # Try to load a truetype font, fallback to default
        try:
            font_bold = ImageFont.truetype("arial.ttf", 36)
            font_small = ImageFont.truetype("arial.ttf", 16)
        except Exception:
            font_bold = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # Helper to draw centered text
        def draw_centered(y, txt, font, fill=(255, 255, 255, 255)):
            try:
                w, h = font.getsize(txt)
            except Exception:
                w, h = draw.textsize(txt, font=font)
            x = (width - w) // 2
            draw.text((x, y - h // 2), txt, font=font, fill=fill)

        draw_centered(170, text, font_bold, (255, 255, 255, 255))
        draw_centered(220, 'Hình ảnh minh chứng bài tập', font_small, (255, 255, 255, 200))
        draw_centered(250, 'Thay thế bằng ảnh thực của bạn', font_small, (255, 255, 255, 150))

        # If saving as JPEG, convert to RGB (JPEG doesn't support alpha)
        lower = path.lower()
        if lower.endswith('.jpg') or lower.endswith('.jpeg'):
            img_rgb = img.convert('RGB')
            img_rgb.save(path)
        else:
            img.save(path)
        print(f"Đã tạo PNG: {path}")
    except ImportError:
        # Nếu không có Pillow, tạo SVG thay thế
        svg_path = path.replace('.png', '.svg').replace('.jpg', '.svg')
        create_svg_placeholder(svg_path, text, '#%02x%02x%02x' % bg_color)


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(base_dir, 'static', 'images')
    os.makedirs(images_dir, exist_ok=True)

    # Tạo ảnh cho từng bài tập
    projects = [
        ("project1.svg", "Máy tính & Thiết bị Ngoại vi", "#2ecc71"),
        ("project2.svg", "Khai thác Dữ liệu", "#27ae60"),
        ("project3.svg", "Tổng quan về AI", "#16a085"),
        ("project4.svg", "Giao tiếp & Hợp tác Số", "#1abc9c"),
        ("project5.svg", "Sáng tạo Nội dung Số", "#2ecc71"),
        ("project6.svg", "An toàn & Liêm chính", "#27ae60"),
    ]

    for filename, text, color in projects:
        path = os.path.join(images_dir, filename)
        create_svg_placeholder(path, text, color)

    # Tạo ảnh placeholder chung (dùng khi ảnh thật không tìm thấy)
    placeholder_path = os.path.join(images_dir, 'placeholder.svg')
    create_svg_placeholder(placeholder_path, "Hình ảnh", "#95a5a6")

    print("\nHoàn thành! Các file SVG đã được tạo trong static/images/")
    print("Gợi ý: Thay thế các file SVG bằng ảnh thực của bạn (.jpg, .png)")
    print("   - Kích thước khuyến nghị: 800x400 pixels")
    print("   - Cập nhật đường dẫn trong app.py (trường 'image' của mỗi project)")