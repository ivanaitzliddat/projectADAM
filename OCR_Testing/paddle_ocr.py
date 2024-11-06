from paddleocr import PaddleOCR, draw_ocr
import matplotlib.pyplot as plt
import cv2

class OCRProcessor:
    def __init__(self, lang='en', use_angle_cls=True, font_path=None):
        self.ocr = PaddleOCR(use_angle_cls=use_angle_cls, lang=lang)
        self.font_path = font_path

    def perform_ocr(self, frame):
        print("Performing OCR...")
        result = self.ocr.ocr(frame, cls=True)
        keyword = "monitor"
        # Display OCR results that contain the keyword "monitor"
        for line in result:
            for box, (text, score) in line:
                if keyword.lower() in text.lower():  # Case-insensitive search
                    print(f"Detected text: {text} (Confidence: {score:.2f})")
        return result

    def display_ocr_results(self, frame, result):
        keyword = "monitor"
        # Filter the results to include only texts containing the keyword
        filtered_boxes = []
        filtered_texts = []
        filtered_scores = []

        for line in result:
            for box, (text, score) in line:
                if keyword.lower() in text.lower():  # Case-insensitive search
                    filtered_boxes.append(box)
                    filtered_texts.append(text)
                    filtered_scores.append(score)

        # Draw filtered OCR results on the image
        image_with_boxes = draw_ocr(frame, filtered_boxes, filtered_texts, filtered_scores, font_path=self.font_path)

        # Display the image
        plt.imshow(image_with_boxes)
        plt.axis('off')
        plt.show()

    def run(self):
        image_path = './screenshots/screenshot.png'
        image = cv2.imread(image_path)
        frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        print("Completed frame conversion!")
        ocr_results = self.perform_ocr(frame_rgb)
        print("Completed OCR!")
        if None in ocr_results:
            print("No Text Found.")
        else:
            print("Displaying OCR Result...")
            self.display_ocr_results(image, ocr_results)

if __name__ == "__main__":
    ocr = OCRProcessor(font_path='C:\\Windows\\fonts\\arial.ttf')
    ocr.run()
