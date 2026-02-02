import tkinter as tk
import random


class UIManager():
    
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=600, height=500, bg="white")
        
    def placing(self):
        self.root.geometry("600x700")
        self.root.title("Snake Game")
        self.label = tk.Label(self.root, text="Welcome!Snake moves with directional keys.\nDon't hit the walls or snake's tail,foods help you grow. ",font=("Arial", 12))
        self.label.grid(row=0, column=0, columnspan=2, pady=20, padx=108) 
        self.canvas.grid(row=2, column=0, columnspan=2,pady=15)
        
    def start_button(self,play):
        self.button = tk.Button(self.root, text="START", command=play)
        self.button.grid(row=3, column=0, columnspan=2)    
        
    def game_over(self,restart):
        self.frame = tk.Frame(self.root, background="black", width=600, height=700)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        self.try_again_btn = tk.Button(self.frame, text="Try Again", font=("Arial", 12),command=restart, bg="white", fg="black")
        self.try_again_btn.place(relx=0.5, rely=0.1, anchor="n")
        self.game_over_label = tk.Label(self.frame, text="GAME OVER", fg="red",bg="black", font=("Arial", 28, "bold"))
        self.game_over_label.place(relx=0.5, rely=0.5, anchor="center")

    def show(self):
        self.root.mainloop()
    
       
class Snake():
    
    def __init__(self,canvas,move):
        self.snake_coords = []
        self.snake_parts = []
        self.board = canvas
        self.move = move
        
    def make_snake(self):
        part_coords = [(100,100),(80,100),(60,100)]
        parts = []
        for x,y in part_coords:
                part = self.board.create_rectangle(x, y, x + 20, y + 20, fill="green")
                parts.append(part)
                self.snake_coords.append(self.board.coords(part))
                self.snake_parts.append(part)
                      
    def moving(self,growing):
            old_head = self.snake_coords[0]
            new_x = old_head[0] + self.move.x
            new_y = old_head[1] + self.move.y
            new_head = self.board.create_rectangle(new_x, new_y, new_x + 20, new_y + 20, fill="green")       
            self.snake_coords.insert(0, self.board.coords(new_head) )
            self.snake_parts.insert(0, new_head)
            if not growing:  
                self.board.delete(self.snake_parts[-1])
                self.snake_parts.pop()
                self.snake_coords.pop() 
                
    def reset(self):
         self.snake_coords.clear()
         self.snake_parts.clear()

        
class Food():
    def __init__(self,canvas):
        self.board = canvas
        self.food_coords = None
        
    def create_food(self):
            colors = ("blue","pink","red","yellow","purple")
            x = random.randint(0,380)
            y = random.randint(0,380)
            color = random.choice(colors)
            self.food = self.board.create_oval(x, y, x+20, y+20, fill=color)
            self.food_coords = (x,y)
    
    def delete_food(self):
        self.board.delete(self.food)
        self.food_coords = None
        self.create_food()        
        
    def reset(self):
        self.food_coords = (200,200)
            
class Rules():
    
    def __init__(self,snake,food):
        self.snake = snake
        self.food = food
        
    
    def is_head_in_body(self):
        head = self.snake.snake_coords[0]
        for body in self.snake.snake_coords[1:]:
            if abs(head[0] - body[0]) < 20 and abs(head[1] - body[1]) < 20 :
                return True
        return False
        
    def hit_the_wall(self):
        head = self.snake.snake_coords[0]
        x1, y1, x2, y2 = head
        if x1 < 0 or y1 < 0 or x2 > 500 or y2 > 600:
            return True
        return False
        
    def growing(self):
        head = self.snake.snake_coords[0]
        food = self.food.food_coords
        if abs(head[0] - food[0]) < 20 and abs(head[1] - food[1]) < 20:
            return True
        return False
            
            
class MoveManager():
    def __init__(self,root):
        self.x = 20
        self.y = 0
        self.root = root
        
    def left(self,event):
        self.x = -20
        self.y = 0
    
    def right(self,event):
        self.x = 20
        self.y = 0
    
    def up(self,event):
        self.y = -20
        self.x = 0
    
    def down(self,event):
        self.y = 20
        self.x = 0
        
    def binding(self):
        self.root.bind("<Left>", self.left)
        self.root.bind("<Right>", self.right)
        self.root.bind("<Up>", self.up)
        self.root.bind("<Down>", self.down)
        
    def reset(self):
        self.x = 20
        self.y = 0


class Game():
    def __init__(self):
        self.manager = UIManager()
        self.move = MoveManager(self.manager.root)
        self.snake = Snake(self.manager.canvas, self.move)
        self.food = Food(self.manager.canvas)
        self.rules = Rules(self.snake, self.food)
        
    def playing(self):
        growing = self.rules.growing()
        if not self.is_dead():
            self.snake.moving(growing)
            if growing:
                self.food.delete_food()
            self.manager.root.after(150, self.playing)
        else:
            self.manager.game_over(self.restart)       
    
    def is_dead(self):
        if self.rules.hit_the_wall() or self.rules.is_head_in_body():
            return True
    
    def start(self):
        self.manager.placing()
        self.snake.make_snake()
        self.food.create_food()
        self.move.binding()
        self.manager.start_button(self.playing)
        
    def restart(self):
        self.manager.canvas.delete("all")
        self.manager.frame.destroy()
        self.food.reset()
        self.snake.reset()
        self.move.reset()
        self.start()
        
    
    
game = Game()
game.start()
game.manager.show()
