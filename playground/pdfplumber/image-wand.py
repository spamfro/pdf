# Wand documentation
# https://docs.wand-py.org/en/stable/

# Enable Wand policy to read PDF
# https://imagemagick.org/script/security-policy.php


import argparse
import pdfplumber


def main(file_path, image_path):
  pdf = pdfplumber.open(file_path)
  page = pdf.pages[0]
  im = page.to_image(resolution=300)
  im.draw_rects(page.extract_words(keep_blank_chars=True, y_tolerance=0, x_tolerance=1))
  im.save(image_path) if image_path else im.show()


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('file_path', type=str, help='file path')
  parser.add_argument('--image-path', type=str, help='image file path')
  args = parser.parse_args()
  main(**vars(args))
