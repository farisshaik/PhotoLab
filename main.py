import tkinter
from tkinter import ttk, Tk, PhotoImage, RIDGE, Canvas, GROOVE, filedialog, colorchooser, messagebox
from tkinter.ttk import Scale

from PIL import ImageTk, Image
import cv2 as cv
import numpy as np

import sv_ttk

class EditorWindow:
    def __init__(self, parent):
        self.parent = parent

        self.frame_header = ttk.Frame(self.parent)
        self.frame_header.pack()

        ttk.Label(self.frame_header, text='PhotoLab').grid(row=0, column=1, columnspan=2)
        ttk.Label(self.frame_header, text='OpenCV Image Editor').grid(row=1, column=1, columnspan=2)

        self.menu_framing = ttk.Frame(self.parent)
        self.menu_framing.pack()
        self.menu_framing.config(relief=RIDGE, padding=(50,15))

        ttk.Button(self.menu_framing, text= "Import Image", command=self.import_func).grid(
            row=0, column=0, columnspan=2, padx=2, pady=3, sticky='sw')

        ttk.Button(self.menu_framing, text="Save As", command=self.save_func).grid(
            row=1, column=0, columnspan=2, padx=2, pady=3, sticky='sw')

        ttk.Button(self.menu_framing, text="Crop", command=self.crop_func).grid(
            row=2, column=0, columnspan=2, padx=2, pady=3, sticky='sw')

        ttk.Button(self.menu_framing, text="Rotate / Flip", command=self.rotate_flip_func).grid(
            row=3, column=0, columnspan=2, padx=2, pady=3, sticky='sw')

        ttk.Button(self.menu_framing, text="Draw Tool", command=self.draw_func).grid(
            row=4, column=0, columnspan=2, padx=2, pady=3, sticky='sw')

        ttk.Button(self.menu_framing, text="Filters", command=self.filters_func).grid(
            row=5, column=0, columnspan=2, padx=2, pady=3, sticky='sw')

        ttk.Button(self.menu_framing, text="Blur / Smoothen", command=self.blur_func).grid(
            row=6, column=0, columnspan=2, padx=2, pady=3, sticky='sw')

        ttk.Button(self.menu_framing, text="Adjust Levels", command=self.levels_func).grid(
            row=7, column=0, columnspan=2, padx=2, pady=3, sticky='sw')

        ttk.Button(self.menu_framing, text="Add Logo", command=self.watermark_func).grid(
            row=8, column=0, columnspan=2, padx=2, pady=3, sticky='sw')

        self.apply_cancel_footer = ttk.Frame(self.parent)
        self.apply_cancel_footer.pack()

        ttk.Button(self.apply_cancel_footer, text="Apply", command=self.apply_func).grid(
            row=0, column=0, columnspan=2, padx=5, pady=3, sticky='sw')

        ttk.Button(self.apply_cancel_footer, text="Cancel", command=self.cancel_func).grid(
            row=0, column=2, columnspan=2, padx=5, pady=3, sticky='sw')

        ttk.Button(self.apply_cancel_footer, text="Revert", command=self.revert_func).grid(
            row=0, column=4, columnspan=2, padx=5, pady=3, sticky='sw')

        self.canvas = Canvas(self.menu_framing, bg="pink", width=900, height=600)
        self.canvas.grid(row=0, column=2, rowspan=10)

        self.side_frame = ttk.Frame(self.menu_framing)
        self.side_frame.grid(row=0, column=4, rowspan=10)
        self.side_frame.config(relief=GROOVE, padding=(50, 15))

    def watermark_func(self):
        self.refresh_addl_menu()
        ttk.Button(
            self.side_frame, text="Import Logo", command=self.import_watermark_func).grid(row=0, column=2,
                                                                                  padx=5, pady=5,
                                                                                  sticky='sw')
        ttk.Button(
            self.side_frame, text="Add Logo", command=self.add_watermark_menu).grid(row=1, column=2,
                                                                                               padx=5, pady=5,
                                                                                               sticky='sw')

    def add_watermark_menu(self):
        self.refresh_addl_menu()
        ttk.Button(
            self.side_frame, text="Top Left", command=self.add_watermark_tl).grid(row=1, column=2,
                                                                                     padx=5, pady=5,
                                                                                     sticky='sw')
        ttk.Button(
            self.side_frame, text="Top Right", command=self.add_watermark_tr).grid(row=1, column=3,
                                                                                      padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.side_frame, text="Bottom Left", command=self.add_watermark_bl).grid(row=2, column=2,
                                                                                        padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.side_frame, text="Bottom Right", command=self.add_watermark_br).grid(row=2, column=3,
                                                                                         padx=5, pady=5, sticky='sw')

    def import_watermark_func(self):
        self.logo_filename = filedialog.askopenfilename()
        self.logo_png = cv.imread(self.logo_filename, cv.IMREAD_UNCHANGED)
        self.h_logo, self.w_logo, self._ = self.logo_png.shape

        self.height, self.width, channels = self.edited_img.shape

        if self.width >= self.height:
            resize_w = self.width/10
            resize_h = resize_w * (self.h_logo/self.w_logo)
        else:
            resize_w = self.width / 5
            resize_h = resize_w * (self.h_logo / self.w_logo)

        self.w_logo = resize_w
        self.h_logo = resize_h
        self.logo_png = cv.resize(self.logo_png, (int(resize_w), int(resize_h)))

        self.top_y = int(self.height/2) - int(self.h_logo / 2)
        self.bottom_y = self.top_y + self.h_logo
        self.left_x = int(self.width/2) - int(self.w_logo / 2)
        self.right_x = self.left_x + self.w_logo

    def add_watermark_tl(self):
        self.add_transparent_image(self.edited_img, self.logo_png, 50,50)
        self.edited_img=self.filter_img
        self.output_image(self.filter_img)

    def add_watermark_tr(self):
        self.add_transparent_image(self.edited_img, self.logo_png, int(self.width - self.w_logo - 50), 50)
        self.edited_img = self.filter_img
        self.output_image(self.filter_img)

    def add_watermark_bl(self):
        self.add_transparent_image(self.edited_img, self.logo_png, 50, int(self.height - self.h_logo - 50))
        self.edited_img = self.filter_img
        self.output_image(self.filter_img)

    def add_watermark_br(self):
        self.add_transparent_image(self.edited_img, self.logo_png, int(self.width - self.w_logo - 50),  int(self.height - self.h_logo - 50))
        self.edited_img = self.filter_img
        self.output_image(self.filter_img)

    def add_transparent_image(self, background, foreground, x_offset, y_offset):
        bg_h, bg_w, bg_channels = background.shape
        fg_h, fg_w, fg_channels = foreground.shape

        w = min(fg_w, bg_w, fg_w + x_offset, bg_w - x_offset)
        h = min(fg_h, bg_h, fg_h + y_offset, bg_h - y_offset)

        if w < 1 or h < 1: return

        bg_x = max(0, x_offset)
        bg_y = max(0, y_offset)
        fg_x = max(0, x_offset * -1)
        fg_y = max(0, y_offset * -1)
        foreground = foreground[fg_y:fg_y + h, fg_x:fg_x + w]
        background_subsection = background[bg_y:bg_y + h, bg_x:bg_x + w]

        foreground_colors = foreground[:, :, :3]
        alpha_channel = foreground[:, :, 3] / 255  # 0-255 => 0.0-1.0

        alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))

        composite = background_subsection * (1 - alpha_mask) + foreground_colors * alpha_mask

        background[bg_y:bg_y + h, bg_x:bg_x + w] = composite

    def import_func(self):
        self.canvas.delete("all")
        try:
            self.filename = filedialog.askopenfilename()
            if not self.filename:
                return
            self.input_img = cv.imread(self.filename)
            if self.input_img is None:
                messagebox.showerror("Error", "Failed to load image. Ensure file is an image file")
                return
            self.edited_img = cv.imread(self.filename)
            self.filter_img = cv.imread(self.filename)
            self.output_image(self.edited_img)
        except Exception as e:
            messagebox.showerror("Error", "An error occured: {e}")


    def rotate_flip_func(self):
        self.refresh_addl_menu()
        ttk.Button(
            self.side_frame, text="Rotate Counterclockwise", command=self.rotate_left_func).grid(row=0, column=2,
                                                                                                 padx=5,pady=5, sticky='sw')
        ttk.Button(
            self.side_frame, text="Rotate Clockwise", command=self.rotate_right_func).grid(row=1, column=2,
                                                                                                 padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.side_frame, text="Flip Horizontally", command=self.flip_horz_func).grid(row=2, column=2,
                                                                                           padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.side_frame, text="Flip Vertically", command=self.flip_vert_func).grid(row=3, column=2,
                                                                                           padx=5, pady=5, sticky='sw')

    def rotate_left_func(self):
        self.filter_img=cv.rotate(self.filter_img, cv.ROTATE_90_COUNTERCLOCKWISE)
        self.output_image(self.filter_img)

    def rotate_right_func(self):
        self.filter_img = cv.rotate(self.filter_img, cv.ROTATE_90_CLOCKWISE)
        self.output_image(self.filter_img)

    def flip_horz_func(self):
        self.filter_img = cv.flip(self.filter_img,2)
        self.output_image(self.filter_img)

    def flip_vert_func(self):
        self.filter_img = cv.flip(self.filter_img,0)
        self.output_image(self.filter_img)


    def crop_func(self):
        self.rectangle = 0
        self.crop_x1 = 0
        self.crop_y1 = 0
        self.crop_x2 = 0
        self.crop_y2 = 0
        self.canvas.bind("<ButtonPress>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.crop_action)
        self.canvas.bind("<ButtonRelease>", self.end_crop)

    def start_crop(self, action):
        self.crop_x1 = action.x
        self.crop_y1 = action.y

    def crop_action(self, action):
        if self.rectangle:
            self.canvas.delete(self.rectangle)
        self.crop_x2 = action.x
        self.crop_y2 = action.y
        self.rectangle=self.canvas.create_rectangle(self.crop_x1, self.crop_y1,
                                                         self.crop_x2, self.crop_y2, width=1)

    def end_crop(self, event):
        if self.crop_x1 <= self.crop_x2 and self.crop_y1 <= self.crop_y2:
            start_x = int(self.crop_x1 * self.ratio)
            start_y = int(self.crop_y1 * self.ratio)
            end_x = int(self.crop_x2 * self.ratio)
            end_y = int(self.crop_y2 * self.ratio)
        elif self.crop_x1 > self.crop_x2 and self.crop_y1 <= self.crop_y2:
            start_x = int(self.crop_x2 * self.ratio)
            start_y = int(self.crop_y1 * self.ratio)
            end_x = int(self.crop_x1 * self.ratio)
            end_y = int(self.crop_y2 * self.ratio)
        elif self.crop_x1 <= self.crop_x2 and self.crop_y1 > self.crop_y2:
            start_x = int(self.crop_x1 * self.ratio)
            start_y = int(self.crop_y2 * self.ratio)
            end_x = int(self.crop_x2 * self.ratio)
            end_y = int(self.crop_y1 * self.ratio)
        else:
            start_x = int(self.crop_x2 * self.ratio)
            start_y = int(self.crop_y2 * self.ratio)
            end_x = int(self.crop_x1 * self.ratio)
            end_y = int(self.crop_y1 * self.ratio)

        x = slice(start_x, end_x,  1)
        y = slice(start_y, end_y, 1)

        self.filter_img = self.edited_img[y, x]
        self.output_image(self.filter_img)


    def save_func(self):
        orig_file_type = self.filename.split('.')[-1]
        savefilename = filedialog.asksaveasfilename()
        savefilename = savefilename + "." + orig_file_type
        save_as_img = self.edited_img
        cv.imwrite(savefilename, save_as_img)
        self.filename = savefilename


    def draw_func(self):
        self.color_hex = ((0,0,0), '#000000')
        self.refresh_addl_menu()
        self.canvas.bind("<ButtonPress>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw_follow)
        self.draw_color_btn = ttk.Button(self.side_frame, text="Select Color", command=self.color_select)
        self.draw_color_btn.grid(row=1, column=2, padx=5, pady=5, sticky='sw')

    def color_select(self):
        self.color_hex = colorchooser.askcolor(title="Select color")

    def start_drawing(self, action):
        self.x = action.x
        self.y = action.y
        self.draw_arr = []

    def draw_follow(self, action):
        print(self.draw_arr)
        self.draw_arr.append(self.canvas.create_line(self.x, self.y, action.x, action.y, width=2, fill=self.color_hex[1], capstyle=tkinter.ROUND, smooth=True))

        cv.line(self.filter_img, (int(self.x * self.ratio), int(self.y * self.ratio)), (int(action.x * self.ratio), int(action.y * self.ratio)), (self.color_hex[0][2],self.color_hex[0][1],self.color_hex[0][0]) , thickness=int(self.ratio * 2), lineType=8)

        self.x = action.x
        self.y = action.y

    def filters_func(self):
        self.refresh_addl_menu()
        ttk.Button(
            self.side_frame, text="Negative", command=self.modify_negative).grid(row=0, column=2, padx=5, pady=5,
                                                                                 sticky='sw')
        ttk.Button(
            self.side_frame, text="Black And white", command=self.modify_bw).grid(row=1, column=2, padx=5, pady=5,
                                                                                  sticky='sw')
        ttk.Button(
            self.side_frame, text="Sketch Effect", command=self.modify_sketch).grid(row=3, column=2, padx=5, pady=5,
                                                                                    sticky='sw')
        ttk.Button(
            self.side_frame, text="Emboss", command=self.modify_emboss).grid(row=4, column=2, padx=5, pady=5, sticky='sw')

    def modify_negative(self):
        self.filter_img=cv.bitwise_not(self.edited_img)
        self.output_image(self.filter_img)

    def modify_bw(self):
        self.filter_img=cv.cvtColor(self.edited_img,cv.COLOR_BGR2GRAY)
        self.filter_img=cv.cvtColor(self.filter_img, cv.COLOR_GRAY2BGR)
        self.output_image(self.filter_img)

    def modify_sketch(self):
        skt, self.filter_img=cv.pencilSketch(self.edited_img, sigma_s=150, sigma_r=0.25)
        self.output_image(self.filter_img)

    def modify_emboss(self):
        arr = np.array([[0, -1, -1],
                           [1, 0, -1],
                           [1, 1, 0]])
        self.filter_img=cv.filter2D(self.input_img, -1, arr)
        self.output_image(self.filter_img)


    def blur_func(self):
        self.refresh_addl_menu()
        ttk.Label(
            self.side_frame, text="Averaging Blur").grid(row=0, column=2, padx=5, sticky='sw')

        self.averaging_blur_slider = Scale(self.side_frame, from_=0, to=100, orient=tkinter.HORIZONTAL,
                                           command=self.averaging_blur_func)
        self.averaging_blur_slider.grid(row=1, column=2, padx=5, sticky='sw')

        ttk.Label(
            self.side_frame, text="Gaussian Blur").grid(row=2, column=2, padx=5, sticky='sw')

        self.gaussian_blur_slider = Scale(self.side_frame, from_=0, to=100, orient=tkinter.HORIZONTAL,
                                           command=self.gaussian_blur_func)
        self.gaussian_blur_slider.grid(row=3, column=2, padx=5, sticky='sw')

        ttk.Label(
            self.side_frame, text="Median Blur").grid(row=4, column=2, padx=5, sticky='sw')

        self.median_blur_slider = Scale(self.side_frame, from_=0, to=100, orient=tkinter.HORIZONTAL,
                                           command=self.median_blur_func)
        self.median_blur_slider.grid(row=5, column=2, padx=5, sticky='sw')

    def averaging_blur_func(self, pct):
        pct = int(float(pct)*256/100)
        if pct % 2 == 0:
            pct += 1
        self.filter_img=cv.blur(self.edited_img, (pct, pct))
        self.output_image(self.filter_img)

    def gaussian_blur_func(self, pct):
        pct = int(float(pct)*256/100)
        if pct % 2 == 0:
            pct += 1
        self.filter_img=cv.GaussianBlur(self.edited_img, (pct, pct), 0)
        self.output_image(self.filter_img)

    def median_blur_func(self, pct):
        pct = int(float(pct)*256/100)
        if pct % 2 == 0:
            pct += 1
        self.filter_img=cv.medianBlur(self.edited_img, pct)
        self.output_image(self.filter_img)



    def levels_func(self):
        self.refresh_addl_menu()
        ttk.Label(
            self.side_frame, text="Brightness").grid(row=0, column=2, padx=5, sticky='sw')

        self.brightness_slider = Scale(self.side_frame, from_=0, to=2, orient=tkinter.HORIZONTAL,
                                           command=self.brightness_func)
        self.brightness_slider.grid(row=1, column=2, padx=5, sticky='sw')
        self.brightness_slider.set(1)

        ttk.Label(
            self.side_frame, text="Saturation").grid(row=2, column=2, padx=5, sticky='sw')

        self.saturation_slider = Scale(self.side_frame, from_=-200, to=200, orient=tkinter.HORIZONTAL,
                                           command=self.saturation_func)
        self.saturation_slider.grid(row=3, column=2, padx=5, sticky='sw')
        self.saturation_slider.set(0)

    def brightness_func(self, pct):
        self.filter_img = cv.convertScaleAbs(self.edited_img, alpha=self.brightness_slider.get())
        self.output_image(self.filter_img)


    def saturation_func(self, pct):
        self.filter_img = cv.convertScaleAbs(self.edited_img, alpha=1, beta=self.saturation_slider.get())
        self.output_image(self.filter_img)

    def apply_func(self):
        self.edited_img=self.filter_img
        self.output_image(self.edited_img)

    def cancel_func(self):
        self.output_image(self.edited_img)

    def revert_func(self):
        self.edited_img = self.input_img.copy()
        self.output_image(self.input_img)

    def refresh_addl_menu(self):
        try:
            self.side_frame.grid_forget()
        except:
            pass

        self.canvas.unbind("<ButtonPress>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease>")
        self.output_image(self.edited_img)
        self.side_frame = ttk.Frame(self.menu_framing)
        self.side_frame.grid(row=0, column=3, rowspan=10)
        self.side_frame.config(relief=GROOVE, padding=(50, 15))

    def output_image(self, image=None):
        self.canvas.delete("all")
        if image is None:
            image = self.edited_img.copy()
        else:
            image = image

        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        height, width, channels = image.shape
        ratio = height/width

        new_width = width
        new_height = height

        if height > 600 or width > 900:
            if ratio < 1:
                new_width = 900
                new_height = int(new_width * ratio)
            else:
                new_height = 600
                new_width = int(new_height * (width / height))

        self.ratio = height / new_height
        self.new_img = cv.resize(image, (new_width, new_height))

        self.new_img = ImageTk.PhotoImage(
            Image.fromarray(self.new_img))

        self.canvas.config(width=new_width, height=new_height)
        self.canvas.create_image(
            new_width / 2, new_height / 2, image=self.new_img)

mainWindow = Tk()
EditorWindow(mainWindow)
sv_ttk.set_theme("light")
mainWindow.mainloop()
