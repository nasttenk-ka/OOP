import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from canvas import DrawingCanvas
from shapes.rectangle import RectangleShape
from shapes.triangle import TriangleShape
from shapes.circle import CircleShape
2
class PaintApp:
    def __init__(self):
        self.canvas = DrawingCanvas()
        self.running = True

    def menu(self):
        while self.running:
            self.canvas.display()
            print("\n=== Paint Application Menu ===")
            print("1. Draw Rectangle")
            print("2. Draw Triangle") 
            print("3. Draw Circle")
            print("4. Fill Shape")
            print("5. Change Background")
            print("6. Save Canvas")
            print("7. Load Canvas")
            print("8. Move Shape")
            print("9. Delete Shape")
            print("10. List Shapes")
            print("11. Undo")
            print("12. Redo")
            print("13. Exit")
            
            choice = input("Enter your choice: ").strip()
            
            try:
                if choice == '1':
                    x, y = map(int, input("Enter top-left x y: ").split())
                    width, height = map(int, input("Enter width height: ").split())
                    border = input("Border character (default #): ") or '#'
                    fill = input("Fill character (optional): ") or None
                    rect = RectangleShape(x, y, width, height, border, fill)
                    self.canvas.add_shape(rect)
                    
                elif choice == '2':
                    x, y = map(int, input("Enter first point x y: ").split())
                    a, b, c = map(int, input("Enter 3 sides a b c: ").split())
                    border = input("Border character (default *): ") or '*'
                    fill = input("Fill character (optional): ") or None
                    tri = TriangleShape(x, y, a, b, c, border, fill)
                    self.canvas.add_shape(tri)
                    
                elif choice == '3':
                    try:
                     x, y = map(int, input("Enter center x y: ").split())
                     radius = int(input("Enter radius: "))
                     border = input("Border character (default @): ") or '@'
                     fill = input("Fill character (optional): ") or None
                     circle = CircleShape(x, y, radius, border, fill)
                     self.canvas.add_shape(circle)
                    except ValueError:
                     print("Error: Invalid input. Please enter numbers for coordinates and radius.")
                    except Exception as e:
                     print(f"Error: {str(e)}. Please try again.")

                elif choice == '4':
                    shape_id = int(input("Enter shape ID to fill: "))
                    fill_char = input("Enter fill character: ")
                    self.canvas.fill_shape(shape_id, fill_char)
                    
                elif choice == '5':
                    bg_char = input("Enter background character: ")
                    if len(bg_char) == 1:
                        self.canvas.change_background(bg_char)
                    else:
                        print("Error: Background must be single character")
                        
                elif choice == '6':
                    filename = input("Enter filename to save: ")
                    self.canvas.save_to_file(filename)
                    print(f"Saved to data/{filename}")
                    
                elif choice == '7':
                    filename = input("Enter filename to load: ")
                    self.canvas.load_from_file(filename)
                    
                elif choice == '8':
                    shape_id = int(input("Enter shape ID to move: "))
                    dx, dy = map(int, input("Enter dx dy: ").split())
                    self.canvas.move_shape(shape_id, dx, dy)
                    
                elif choice == '9':
                    shape_id = int(input("Enter shape ID to delete: "))
                    self.canvas.delete_shape(shape_id)
                    
                elif choice == '10':
                    self.canvas.show_shapes_list()
                    
                elif choice == '11':
                    if not self.canvas.undo():
                        print("Nothing to undo")
                        
                elif choice == '12':
                    print("Redo functionality not implemented yet")
                    
                elif choice == '13':
                    self.running = False
                    
                else:
                    print("Invalid choice. Please try again.")
                    
            except Exception as e:
                print(f"Error: {str(e)}. Please try again.")

if __name__ == "__main__":
    app = PaintApp()
    app.menu()