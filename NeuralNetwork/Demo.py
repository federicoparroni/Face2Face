import FaceExtractionPipeline
import skimage.io
import skimage.transform
import cv2
import LoadData
import numpy as np
import math

import ModelBuilder
from ModelBuilder import read_model

import time

import tkinter as tk
import PIL.Image, PIL.ImageTk


class Demo:

    cap = None
    graph = None
    model = None
    ref_img = None
    captureWidth = 0
    captureHeight = 0

    def ElaborateImagesAndMakePredition(self, inp_img):
        # crop a good percentage of the image in order to gain performances. found a good tradeoff with those values

        start_time = time.time()

        img_data_pipelined = FaceExtractionPipeline.SingletonPipeline().FaceExtractionPipelineImage(inp_img,
                                                                                                    math.ceil(np.shape(inp_img)[0]*20/100),
                                                                                                    math.ceil(np.shape(inp_img)[0]*40/100))

        if img_data_pipelined is not None:
            # plt.imshow(img_data_pipelined, 'gray')
            # plt.show()

            inp = LoadData.MergeImages(self.ref_img, img_data_pipelined)
            inp = np.expand_dims(inp, axis=0)

            #with self.graph.as_default():
            predicted_label = self.model.predict(inp)

            print(('same' if predicted_label[0, 1] > 0.975 else 'wrong') + str(predicted_label))
            return True, predicted_label[0, 1]

        else:
            return False, 0

        print("--- %s seconds for a frame---" % (time.time() - start_time))

        # self.OneFrameComputation()


    def OneFrameComputation(self):
        # threading.Timer(0.5, self.OneFrameComputation).start()

        # read frame

        # cv2.imshow('my webcam', frame)

        while True:
            ret, frame = self.cap.read()
            cv2.imshow('my webcam', frame)
            if cv2.waitKey(1) == 27:
                break  # esc to quit
            self.ElaborateImagesAndMakePredition(frame)
        cv2.destroyAllWindows()

        # do the prediction in a different thread
        #t = threading.Thread(target=self.ElaborateImagesAndMakePredition, args=(frame,))
        #t.setDaemon(True)
        #t.start()


    def StartDemo(self, ref, model_path):
        self.captureWidth = 640
        self.captureHeight = 480
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, self.captureWidth)
        self.cap.set(4, self.captureHeight)

        # self.graph = tf.get_default_graph()

        bp = 'trained_model/'

        a = read_model("models/model99.txt")
        modelObject = ModelBuilder.ModelBuilder(a, (80, 80, 2))
        self.model = modelObject.model
        self.model.load_weights(bp+model_path)

        #self.model = load_model(bp+model_path)
        self.ref_img = FaceExtractionPipeline.SingletonPipeline().FaceExtractionPipelineImage(skimage.io.imread(ref))

        demo.Window(ref)

        # plt.imshow(self.ref_img, 'gray')
        # plt.show()

        # self.OneFrameComputation()

    def Window(self, imageName):
        self.counter = 0

        # Set up GUI
        window = tk.Tk()  # Makes main window
        window.wm_title("Face2Face")

        window.config(background="#FFFFFF")
        #window.geometry("400x200")

        # Graphics window
        imageFrame1 = tk.Frame(window, width=self.captureWidth, height=self.captureHeight)
        imageFrame1.grid(row=0, column=0, padx=10, pady=2)

        imageFrame2 = tk.Frame(window, width=self.captureWidth, height=self.captureHeight)
        imageFrame2.grid(row=0, column=1, padx=10, pady=2)

        # Capture video frames
        image1 = tk.Label(imageFrame1, width=self.captureWidth, height=self.captureHeight)
        image1.grid(row=0, column=0)

        img = PIL.Image.open(imageName)
        img = img.resize((self.captureWidth, self.captureHeight), PIL.Image.ANTIALIAS)
        staticPhoto = PIL.ImageTk.PhotoImage(img)

        image2 = tk.Label(imageFrame2, width=self.captureWidth, height=self.captureHeight, image=staticPhoto)
        image2.grid(row=0, column=0)
        image2.image = staticPhoto

        lblProbability = tk.Label(window, text='INITIALIZING', bg='white', font=('arial', 30))
        lblProbability.grid(row=1, pady=40, columnspan=2)
        #lblProbability.pack()
        #lblProbability.configure(text="0")

        def show_frame():
            _, frame = self.cap.read()
            frame = cv2.flip(frame, 1)

            if self.counter > 10:
                foundPerson, pSame = self.ElaborateImagesAndMakePredition(frame)
                self.counter = 0
                if foundPerson:
                    if pSame > 0.85:
                        lblProbability.config(text='MATCHING PROBABILITY: {} ;)'.format(pSame))
                    else:
                        lblProbability.config(text='MATCHING PROBABILITY: {} :\'('.format(pSame))
                else:
                    lblProbability.config(text='FACE NOT FOUND')

            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = PIL.Image.fromarray(cv2image)
            imgtk = PIL.ImageTk.PhotoImage(image=img)
            image1.imgtk = imgtk
            image1.configure(image=imgtk)



            self.counter += 1
            image1.after(10, show_frame)


        # Slider window (slider controls stage position)
        #sliderFrame = tk.Frame(window, width=600, height=100)
        #sliderFrame.grid(row=600, column=0, padx=10, pady=2)

        show_frame()  # Display 2
        window.mainloop()  # Starts GUI


demo=Demo()
demo.StartDemo('/Users/federico/Desktop/io.jpg', 'finalmodel99.h5')
