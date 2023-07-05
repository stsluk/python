from tkinter import *
import time
import math

window = Tk()
window.title("game")
window.resizable(0, 0)
canvas = Canvas(window, width=640, height=640, bg="white")
canvas.pack()

class Game:
    global objects
    objects = set()
    def __init__(self):
        self.keys = set()
        self.mx, self.my, self.mPressed = 0, 0, 0
        window.bind("<KeyPress>", self.keyPressHandler)
        window.bind("<KeyRelease>", self.keyReleaseHandler)
        canvas.bind("<Button-1>", self.mousePress)
        canvas.bind("<B1-Motion>", self.mousePress)
        canvas.bind("<ButtonRelease-1>", self.mouseRelease)
        canvas.pack
        
        obj_main = element(310, 310, 20, 20, "black")
        
        while True:
            for key in self.keys:
                if key == ord('A') and obj_main.x_accel > -10:
                    obj_main.x_accel -= 1
                elif key == ord('D') and obj_main.x_accel < 10:
                    obj_main.x_accel += 1
                elif key == ord('W') and obj_main.y_accel > -10:
                    obj_main.y_accel -= 1
                elif key == ord('S') and obj_main.y_accel < 10:
                    obj_main.y_accel += 1
            
            if self.mPressed == 1:
                obj_attack = object_attack(canvas.coords(obj_main.canvas_id)[0]+8, canvas.coords(obj_main.canvas_id)[1]+8, 4, 4, "black", 120)
                obj_attack.x_accel, obj_attack.y_accel = self.movePoint(canvas.coords(obj_attack.canvas_id)[0]+10, canvas.coords(obj_attack.canvas_id)[1]+10, self.mx, self.my, 25)
            
            for obj in objects.copy():
                obj.step()
            
            window.update()
            time.sleep(0.01)
            
    def keyPressHandler(self, event):
        self.keys.add(event.keycode)
        
    def keyReleaseHandler(self, event):
        if event.keycode in self.keys:
            self.keys.remove(event.keycode)
    
    def mousePress(self, event):
        self.mx, self.my, self.mPressed = event.x, event.y, 1
    
    def mouseRelease(self, event):
        self.mx, self.my, self.mPressed = event.x, event.y, 0
    
    def movePoint(self, x1, y1, x2, y2, spd):
        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        if spd < distance:
            return (x2-x1)*spd / distance, (y2-y1)*spd / distance
        else:
            return 0, 0


class element:
    def __init__(self, x, y, size_x, size_y, color):
        self.x, self.y = x, y
        self.size_x, self.size_y = size_x, size_y
        self.color = color
        self.x_accel, self.y_accel = 0, 0
        objects.add(self)
        self.canvas_id = canvas.create_rectangle(x, y, x + self.size_x, y + self.size_y, fill=self.color, width=0)
    
    def destroy(self):
        objects.discard(self)
        canvas.delete(self.canvas_id)
        del self
    
    def move(self):
        x_value, y_value = self.x_accel, self.y_accel
        if x_value != 0 or y_value != 0:
            if canvas.coords(self.canvas_id)[0] + x_value < 0:
                x_value = -2*canvas.coords(self.canvas_id)[0] - x_value
                self.x_accel *= -1
            if canvas.coords(self.canvas_id)[1] + y_value < 0:
                y_value = -2*canvas.coords(self.canvas_id)[1] - y_value
                self.y_accel *= -1
            if canvas.coords(self.canvas_id)[2] + x_value > 640:
                x_value = 1280 - 2*canvas.coords(self.canvas_id)[2] - x_value
                self.x_accel *= -1
            if canvas.coords(self.canvas_id)[3] + y_value > 640:
                y_value = 1280 - 2*canvas.coords(self.canvas_id)[3] - y_value
                self.y_accel *= -1
            canvas.move(self.canvas_id, x_value, y_value)
            self.x_accel -= self.x_accel/50
            self.y_accel -= self.y_accel/50
    
    def step(self):
        self.move()


class object_main(element):
    def __init__(self, x, y, size_x, size_y, color):
        super().__init__(x, y, size_x, size_y, color)
        self.mhp, self.hp = 1000, 1000
        self.cool, self.coolt = 25, 0
    
    def step(self):
        self.move()
        if self.coolt < self.cool:
            self.coolt += 1


class object_attack(element):
    def __init__(self, x, y, size_x, size_y, color, livetime):
        super().__init__(x, y, size_x, size_y, color)
        self.livetime = livetime
        self.fortime = 0
    
    def step(self):
        self.move()
        if self.livetime <= self.fortime:
            self.destroy()
        self.fortime += 1


Game()