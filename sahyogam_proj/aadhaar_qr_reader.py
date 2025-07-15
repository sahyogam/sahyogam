import cv2
import pytesseract

# Set path to tesseract executable if not in PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def extract_aadhaar_data(image_path):
    img = cv2.imread(image_path)

    if img is None:
        print(f"❌ Failed to load image: {image_path}")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(thresh)

    print("🔍 Extracted Text:\n")
    print(text)

# Example usage
extract_aadhaar_data("aadhaar_qr.png")