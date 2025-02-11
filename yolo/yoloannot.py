import cv2
import os

class_labels = ["Maize", "Weed"]
output_dir = "labels"

os.makedirs(output_dir, exist_ok=True)

drawing = False
ix, iy, x1, y1 = -1, -1, -1, -1
annotations = []
current_class = 0

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, x1, y1, annotations, current_class

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            x1, y1 = x, y
    
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x1, y1 = x, y
        annotations.append((current_class, ix, iy, x1, y1))

def convert_to_yolo(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[2]) / 2.0 * dw
    y = (box[1] + box[3]) / 2.0 * dh
    w = abs(box[2] - box[0]) * dw
    h = abs(box[3] - box[1]) * dh
    return f"{box[4]} {x:.6f} {y:.6f} {w:.6f} {h:.6f}"

image_folder = "images"
images = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png', 'jpeg'))]

for img_file in images:
    img_path = os.path.join(image_folder, img_file)
    img = cv2.imread(img_path)
    height, width, _ = img.shape

    annotations = []
    cv2.namedWindow("Annotator")
    cv2.setMouseCallback("Annotator", draw_rectangle)

    while True:
        temp_img = img.copy()
        for ann in annotations:
            cv2.rectangle(temp_img, (ann[1], ann[2]), (ann[3], ann[4]), (0, 255, 0), 2)
            cv2.putText(temp_img, class_labels[ann[0]], (ann[1], ann[2]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
        cv2.imshow("Annotator", temp_img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("c"):
            current_class = (current_class + 1) % len(class_labels)
            print(f"Current Class: {class_labels[current_class]}")

        elif key == ord("s"):
            label_path = os.path.join(output_dir, img_file.replace(".jpg", ".txt").replace(".png", "txt").replace("jpeg", "txt"))
            with open(label_path, "w") as f:
                for ann in annotations:
                    yolo_label = convert_to_yolo((width, height), (*ann[1:], ann[0]))
                    f.write(yolo_label + "\n")

            print(f"Saved: {label_path}")
            break
        elif key == ord("q"):
            cv2.destroyAllWindows()
            exit()

cv2.destroyAllWindows()