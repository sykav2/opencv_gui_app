import tkinter as tk
from tkinter import filedialog, messagebox

# ✅ Импортируем simpledialog отдельно
import tkinter.simpledialog as tk_simpledialog

import cv2
import numpy as np


class ImageViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")

        self.panel = tk.Label(root)
        self.panel.pack()

        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=10)

        tk.Button(self.btn_frame, text="Загрузить изображение", command=self.load_image).pack(side=tk.LEFT, padx=5)
        tk.Button(self.btn_frame, text="Сделать фото с камеры", command=self.capture_from_camera).pack(side=tk.LEFT, padx=5)
        tk.Button(self.btn_frame, text="Обрезка", command=self.crop_image).pack(side=tk.LEFT, padx=5)
        tk.Button(self.btn_frame, text="Повернуть", command=self.rotate_image).pack(side=tk.LEFT, padx=5)
        tk.Button(self.btn_frame, text="Нарисовать круг", command=self.draw_circle).pack(side=tk.LEFT, padx=5)
        tk.Button(self.btn_frame, text="Красный канал", command=lambda: self.show_channel(2)).pack(side=tk.LEFT, padx=5)
        tk.Button(self.btn_frame, text="Зеленый канал", command=lambda: self.show_channel(1)).pack(side=tk.LEFT, padx=5)
        tk.Button(self.btn_frame, text="Синий канал", command=lambda: self.show_channel(0)).pack(side=tk.LEFT, padx=5)

        self.image = None
        self.original_image = None

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png")])
        if not path:
            return
        try:
            self.original_image = cv2.imread(path)
            if self.original_image is None:
                raise ValueError("Файл не является изображением")
            self.image = self.original_image.copy()
            self.show_image()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение:\n{e}")

    def capture_from_camera(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Ошибка", "Не удалось подключиться к камере.\nПроверьте подключение.")
            return
        ret, self.original_image = cap.read()
        cap.release()
        self.image = self.original_image.copy()
        self.show_image()

    def show_image(self):
        if self.image is not None:
            img_resized = cv2.resize(self.image, (600, 400))
            cv2.imshow("Image", img_resized)

    def crop_image(self):
        if self.image is None:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение!")
            return
        try:
            x = int(tk_simpledialog.askstring("Обрезка", "Введите x:"))
            y = int(tk_simpledialog.askstring("Обрезка", "Введите y:"))
            w = int(tk_simpledialog.askstring("Обрезка", "Введите ширину:"))
            h = int(tk_simpledialog.askstring("Обрезка", "Введите высоту:"))
            h_img, w_img = self.image.shape[:2]
            if x < 0 or y < 0 or x + w > w_img or y + h > h_img:
                raise ValueError("Координаты вне диапазона")
            self.image = self.image[y:y+h, x:x+w]
            self.show_image()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Неверный ввод: {e}")

    def rotate_image(self):
        if self.image is None:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение!")
            return
        try:
            angle = float(tk_simpledialog.askstring("Поворот", "Введите угол:"))
            h, w = self.image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            self.image = cv2.warpAffine(self.image, M, (w, h))
            self.show_image()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Неверный ввод: {e}")

    def draw_circle(self):
        if self.image is None:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение!")
            return
        try:
            cx = int(tk_simpledialog.askstring("Круг", "x центра:"))
            cy = int(tk_simpledialog.askstring("Круг", "y центра:"))
            r = int(tk_simpledialog.askstring("Круг", "радиус:"))
            cv2.circle(self.image, (cx, cy), r, (0, 0, 255), 2)  # Красный цвет
            self.show_image()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Неверный ввод: {e}")

    def show_channel(self, channel):
        if self.image is None:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение!")
            return
        zero = np.zeros_like(self.image[:, :, 0])
        channels = [zero, zero, zero]
        channels[channel] = self.image[:, :, channel]

        merged = cv2.merge(channels)

        # ✅ Нормализуем изображение для улучшения контраста
        merged = cv2.normalize(merged, None, 0, 255, cv2.NORM_MINMAX)

        self.image = merged
        self.show_image()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewerApp(root)
    root.mainloop()