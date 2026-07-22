# 01 - Image Basics ★

## Goal
Read an image, inspect its shape/dtype, convert between BGR/Gray/HSV, and
write it back to disk. Runs with no assets (generates a gradient).

## What you learn
- `cv2.imread / imshow / imwrite / waitKey / destroyAllWindows`.
- That OpenCV stores images as BGR `numpy` arrays of shape `(H, W, 3)`.
- Color-space conversions with `cv2.cvtColor`.

## Run
```bash
python3 image_basics.py                 # synthetic gradient
python3 image_basics.py --image me.jpg  # your own image
```

## Extend it
- Split and merge channels with `cv2.split` / `cv2.merge`.
- Crop with numpy slicing `img[y1:y2, x1:x2]`.
