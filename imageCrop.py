
import cv2 
class ImageCropper:
    def __init__(self, imagePath):
        import imutils
        self.imagePath = imagePath
        self.image = cv2.imread(imagePath)
        self.image = imutils.resize(self.image, height=800)
        self.cropping = False
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0


    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.cropping = True
            self.x0 = x
            self.y0 = y


        elif event == cv2.EVENT_MOUSEMOVE:
            if self.cropping:
                self.x1 = x
                self.y1 = y
        

        elif event == cv2.EVENT_LBUTTONUP:
            self.cropping = False
            self.x1 = x
            self.y1 = y
            cv2.rectangle(self.image, (self.x0-2, self.y0-2), (self.x1+2, self.y1+2), (0, 255, 0), 2)
    

            #temporary rectangle
            

    
    def crop(self):
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", self.mouse_callback)
        while True:
            cv2.imshow("image", self.image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("r"):
                self.image = cv2.imread(self.imagePath)
            elif key == ord("c"):
                break
            elif key == ord("q"):
                cv2.destroyAllWindows()
                return None
        cv2.destroyAllWindows()
        return self.image[self.y0:self.y1, self.x0:self.x1]



        
    