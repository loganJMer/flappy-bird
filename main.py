import tkinter as tk, sys, time, random, subprocess, os

# requirements = ["pygetwindow", "Pillow"]

# for package in requirements:
#         subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

import pygetwindow as gw
from PIL import Image, ImageTk

EASY_MODE = True

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class bird:

    GRAVITY = 2.5
    FLAP_STRENGTH = -25

    def __init__(self, height, path):

        self.height = height
        self.size = (int(self.height / 12 * 2**0.5), int(self.height / 12))

        self.root = tk.Toplevel()
        self.root.geometry(f"{self.size[0]}x{self.size[1]}+{0}+{int(self.height/2)}")

        self.root.overrideredirect(EASY_MODE)
        self.image = Image.open(path).resize(self.size)  
        self.photo = ImageTk.PhotoImage(image=self.image)

        self.label = tk.Label(self.root, image=self.photo)
        self.label.pack()

        self.root.title("Flappy Boi")

        self.flapping = False
        self.root.bind('<KeyPress-space>', self.flap_start)
        self.root.bind('<KeyRelease-space>', self.flap_end)     
        self.root.bind('<q>', self.end)
        self.root.lift()
        self.root.grab_set()

        self.velocity = 0
        self.y = int(self.height / 2)

        self.root.update()
        self.game_window = gw.getWindowsWithTitle("Flappy Boi")[0]

    def getRight(self):
        return self.game_window.right
    
    def getVertical(self):
        return [self.game_window.top, self.game_window.bottom]

    def draw(self):
        self.game_window.move(0, int(self.velocity))
        

    def update(self):

        self.velocity += self.GRAVITY

        self.y += int(self.velocity)

        if self.y <= 0 or self.y + self.size[1] >= self.height:
            self.end()

    def flap_start(self, event):
        if not self.flapping:  # Only flap if not already flapping
            self.velocity = self.FLAP_STRENGTH
            self.flapping = True

    def flap_end(self, event):
        self.flapping = False
        
    def end(self, event=None):
        self.root.destroy()
        global root
        root.destroy()
        sys.exit()
        
class pipe:

    def __init__(self, sWidth, sHeight, topPath, botPath, startX):
        self.width = sWidth
        self.height = sHeight
        self.x = startX
        self.speed = -int(self.width / 90)
        self.gap = random.randrange(int(self.height * 0.2), int(self.height * 0.8))
        self.size = (int(self.height * 0.72 * 0.43), int(self.height * 0.72))


        self.ty = self.gap - int(self.height * 0.87)

        self.troot = tk.Toplevel()
        self.troot.geometry(f"{self.size[0]}x{self.size[1]}+{self.x}+{self.ty}")
        
        self.timage = Image.open(topPath)
        self.tphoto = ImageTk.PhotoImage(image=self.timage)

        self.tlabel = tk.Label(self.troot, image=self.tphoto)
        self.tlabel.pack()

        self.troot.title("Pipe1")
        self.troot.update()
        self.tGameWindow = gw.getWindowsWithTitle("Pipe1")[0]
        self.troot.title("Pipe")
        self.troot.update()


        self.by = self.gap + int(sHeight * 0.15)

        self.broot = tk.Toplevel()
        self.broot.geometry(f"{self.size[0]}x{self.size[1]}+{self.x}+{self.by}")
        
        self.broot.overrideredirect(EASY_MODE)
        self.bimage = Image.open(botPath)
        self.bphoto = ImageTk.PhotoImage(image=self.bimage)

        self.blabel = tk.Label(self.broot, image=self.bphoto)
        self.blabel.pack()

        self.broot.title("Pipe1")
        self.broot.update()
        self.bGameWindow = gw.getWindowsWithTitle("Pipe1")[0]
        self.broot.title("Pipe")
        self.broot.update()

        


    def draw(self):
        self.tGameWindow.move(self.speed, 0)
        self.bGameWindow.move(self.speed, 0)

    def update(self):

        self.x += self.speed

        if self.tGameWindow.left < flappyBoi.getRight():
            topBot = flappyBoi.getVertical() 
            if self.tGameWindow.bottom > topBot[0] or self.bGameWindow .top < topBot[1]: 
                flappyBoi.end()

        if self.x <= 0 - self.size[0]:
            self.gap = random.randrange(int(self.height * 0.2), int(self.height * 0.8))
            self.ty = self.gap - int(self.height * 0.87)
            self.by = self.gap + int(self.height * 0.15)
            self.tGameWindow.moveTo(self.width, self.ty)
            self.bGameWindow.moveTo(self.width, self.by)
            self.x = self.width
    

if __name__ == "__main__":

    root = tk.Tk()
    SCREEN_WIDTH = root.winfo_screenwidth()
    SCREEN_HEIGHT = root.winfo_screenheight()
    root.withdraw()

    BIRD_PATH = resource_path("images/fBird.png")
    TOP_PATH = resource_path("images/tPipe.png")
    BOT_PATH = resource_path("images/bPipe.png")

    Image.open(TOP_PATH).resize(((int(SCREEN_HEIGHT * 0.72 * 0.43), int(SCREEN_HEIGHT * 0.72)))).save(TOP_PATH)
    Image.open(BOT_PATH).resize(((int(SCREEN_HEIGHT * 0.72 * 0.43), int(SCREEN_HEIGHT * 0.72)))).save(BOT_PATH)


    flappyBoi = bird(SCREEN_HEIGHT, BIRD_PATH)
    start = time.time()
    pipes = [pipe(SCREEN_WIDTH, SCREEN_HEIGHT, TOP_PATH, BOT_PATH, SCREEN_WIDTH), pipe(SCREEN_WIDTH, SCREEN_HEIGHT, TOP_PATH, BOT_PATH, int(SCREEN_WIDTH * 1.61))]

    while True:

        flappyBoi.update()
        flappyBoi.draw()

        root.update()

        for p in pipes:
            p.update()
            p.draw()

        while time.time() - start < 0.0333:
            pass
        start = time.time()

