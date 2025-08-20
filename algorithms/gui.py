from utils.color_palette import ColorPalette
import time
import algorithms
import tkinter as tk
import tkinter.font as tkFont
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class Root(tk.Tk):

    def __init__(self, master=None):
        super().__init__(master)

        # Configuration of the root
        self.iconbitmap("utils/icon.ico")
        self.config(cursor="@utils/cursor.cur")
        self.geometry("1024x768")
        self.configure(bg=ColorPalette.get_hex("Baby Blue"))
        self.default_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
        self.minsize(800, 400)
        self.title("Algorithms comparison")
        
        self.array = []
        self.input_number = tk.IntVar()
        self.input_number.set(100)
        self.range_value = tk.IntVar()
        self.range_value.set(1000)  # Valor por defecto para el rango
        self.time_text = tk.StringVar()
        self.search_result = tk.StringVar()
        self.search_result.set("Results")
        self.search_value = tk.IntVar()
        self.placeholder_color = ColorPalette.get_hex("Blush Pink")
        self.default_color = ColorPalette.get_hex("Denim Blue")
        self.time_text.set("00:00")
        
        # For storing search history
        self.search_history = {
            'linear': {'times': [], 'sizes': []},
            'binary': {'times': [], 'sizes': []}
        }
        
        # For the plot
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = None
        
        self.widgets()

    def widgets(self):
        # Main frames
        self.frame_label_pack = tk.Frame(self)
        self.frame_label_pack.pack(padx=10, pady=10, fill='x')
        self.frame_label_pack.config(bg=ColorPalette.get_hex("Baby Blue"))
        
        self.frame_grid = tk.Frame(self)
        self.frame_grid.pack(fill='x', pady=10)
        self.frame_grid.config(bg=ColorPalette.get_hex("Baby Blue"))
        
        self.frame_range = tk.Frame(self)
        self.frame_range.pack(fill='x', pady=5)
        self.frame_range.config(bg=ColorPalette.get_hex("Baby Blue"))
        
        self.frame_search = tk.Frame(self)
        self.frame_search.pack(fill='x', pady=10)
        self.frame_search.config(bg=ColorPalette.get_hex("Baby Blue"))
        
        self.frame_results = tk.Frame(self)
        self.frame_results.pack(fill='x', pady=10)
        self.frame_results.config(bg=ColorPalette.get_hex("Baby Blue"))
        
        self.frame_plot = tk.Frame(self)
        self.frame_plot.pack(fill='both', expand=True, padx=10, pady=10)
        self.frame_plot.config(bg=ColorPalette.get_hex("Baby Blue"))

        # Array size selection
        self.array_label = tk.Label(self.frame_label_pack, 
                                   text="Choose the size of the list between: [100, 1000, 10000, 100000] : ",
                                   bg=ColorPalette.get_hex("Baby Blue"),
                                   fg=ColorPalette.get_hex("Denim Blue"))
        self.array_label.pack(anchor='w')

        self.entry_number = tk.Entry(self.frame_grid, textvariable=self.input_number)
        self.entry_number.config(bg=ColorPalette.get_hex("Ligth Grey"), relief="flat")
        self.entry_number.grid(row=0, column=0, padx=5, pady=5)
        
        self.submit_button = tk.Button(self.frame_grid, text="Set size", command=self.get_number)
        self.submit_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Element range selection
        self.range_label = tk.Label(self.frame_range, 
                                   text="Element range (0 to N-1):",
                                   bg=ColorPalette.get_hex("Baby Blue"),
                                   fg=ColorPalette.get_hex("Denim Blue"))
        self.range_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        self.entry_range = tk.Entry(self.frame_range, textvariable=self.range_value)
        self.entry_range.config(bg=ColorPalette.get_hex("Ligth Grey"), relief="flat")
        self.entry_range.grid(row=0, column=1, padx=5, pady=5)
        
        self.range_button = tk.Button(self.frame_range, text="Set Range", command=self.get_range)
        self.range_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Search value input
        self.search_label = tk.Label(self.frame_search, 
                                    text="Enter value to search:",
                                    bg=ColorPalette.get_hex("Baby Blue"),
                                    fg=ColorPalette.get_hex("Denim Blue"))
        self.search_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        self.entry_search = tk.Entry(self.frame_search, textvariable=self.search_value)
        self.entry_search.config(bg=ColorPalette.get_hex("Ligth Grey"), relief="flat")
        self.entry_search.grid(row=0, column=1, padx=5, pady=5)
        
        # Search buttons
        self.linear_button = tk.Button(self.frame_search, text="Linear Search", 
                                      command=self.run_linear_search,
                                      bg=ColorPalette.get_hex("Azalea Pink"))
        self.linear_button.grid(row=1, column=0, padx=5, pady=5)
        
        self.binary_button = tk.Button(self.frame_search, text="Binary Search", 
                                      command=self.run_binary_search,
                                      bg=ColorPalette.get_hex("Spring Green"))
        self.binary_button.grid(row=1, column=1, padx=5, pady=5)
        
        # Clear history button
        self.clear_button = tk.Button(self.frame_search, text="Clear History", 
                                     command=self.clear_history,
                                     bg=ColorPalette.get_hex("Ligth Grey"))
        self.clear_button.grid(row=1, column=2, padx=5, pady=5)
        
        # Results display
        self.result_label = tk.Label(self.frame_results, 
                                    textvariable=self.search_result,
                                    bg=ColorPalette.get_hex("Baby Blue"),
                                    fg=ColorPalette.get_hex("Denim Blue"),
                                    font=("Helvetica", 12, "bold"))
        self.result_label.pack(anchor='w', padx=5, pady=5)
        
        # Initialize plot
        self.init_plot()

    def get_number(self):
        try:
            number = int(self.input_number.get())
            if number not in [100, 1000, 10000, 100000]:
                self.search_result.set("Please enter a valid size: 100, 1000, 10000, or 100000")
                return
                
            self.array_size = number
            self.search_result.set(f"List size set to {number}. Now enter a value to search.")
            print("Selected:", number)
        except ValueError:
            self.search_result.set("Please enter a valid number")
    
    def get_range(self):
        try:
            range_val = int(self.range_value.get())
            if range_val <= 0:
                self.search_result.set("Range must be a positive integer")
                return
                
            self.element_range = range_val
            self.search_result.set(f"Element range set to 0-{range_val-1}")
            print("Range set to:", range_val)
        except ValueError:
            self.search_result.set("Please enter a valid number for range")

    def run_linear_search(self):
        if not hasattr(self, 'array_size'):
            self.search_result.set("Please set the list size first")
            return
            
        if not hasattr(self, 'element_range'):
            self.element_range = 1000  # Valor por defecto si no se ha establecido
            
        try:
            target = int(self.search_value.get())
            if target < 0 or target >= self.element_range:
                self.search_result.set(f"Search value must be between 0 and {self.element_range-1}")
                return
        except ValueError:
            self.search_result.set("Please enter a valid number to search")
            return
            
        # Generate array with the specified range
        arr = [int(x) for x in np.random.randint(0, self.element_range, self.array_size)]
        
        # Run search and measure time
        start_time = time.perf_counter()
        result = algorithms.linear_search(arr, target)
        end_time = time.perf_counter()
        
        # Calculate execution time in milliseconds
        execution_time = (end_time - start_time) * 1000
        
        # Update search history
        self.search_history['linear']['times'].append(execution_time)
        self.search_history['linear']['sizes'].append(self.array_size)
        
        # Update display
        if result != -1:
            self.search_result.set(f"Linear Search: Found at index {result} | Time: {execution_time:.6f} ms | Size: {self.array_size} | Range: 0-{self.element_range-1}")
        else:
            self.search_result.set(f"Linear Search: Not found | Time: {execution_time:.6f} ms | Size: {self.array_size} | Range: 0-{self.element_range-1}")
            
        # Update plot
        self.update_plot()

    def run_binary_search(self):
        if not hasattr(self, 'array_size'):
            self.search_result.set("Please set the list size first")
            return
            
        if not hasattr(self, 'element_range'):
            self.element_range = 1000  # Valor por defecto si no se ha establecido
            
        try:
            target = int(self.search_value.get())
            if target < 0 or target >= self.element_range:
                self.search_result.set(f"Search value must be between 0 and {self.element_range-1}")
                return
        except ValueError:
            self.search_result.set("Please enter a valid number to search")
            return
            
        # Generate and sort array with the specified range
        arr = sorted([int(x) for x in np.random.randint(0, self.element_range, self.array_size)])
        
        # Run search and measure time
        start_time = time.perf_counter()
        result = algorithms.binary_search(arr, 0, len(arr) - 1, target)
        end_time = time.perf_counter()
        
        # Calculate execution time in milliseconds
        execution_time = (end_time - start_time) * 1000
        
        # Update search history
        self.search_history['binary']['times'].append(execution_time)
        self.search_history['binary']['sizes'].append(self.array_size)
        
        # Update display
        if result != -1:
            self.search_result.set(f"Binary Search: Found at index {result} | Time: {execution_time:.6f} ms | Size: {self.array_size} | Range: 0-{self.element_range-1}")
        else:
            self.search_result.set(f"Binary Search: Not found | Time: {execution_time:.6f} ms | Size: {self.array_size} | Range: 0-{self.element_range-1}")
            
        # Update plot
        self.update_plot()

    def clear_history(self):
        # Clear search history
        self.search_history = {
            'linear': {'times': [], 'sizes': []},
            'binary': {'times': [], 'sizes': []}
        }
        self.search_result.set("Search history cleared")
        self.update_plot()

    def init_plot(self):
        # Create initial empty plot
        self.ax.set_title("Algorithm Performance: Time vs Array Size", color=ColorPalette.get_hex("Denim Blue"))
        self.ax.set_xlabel("Array Size", color=ColorPalette.get_hex("Denim Blue"))
        self.ax.set_ylabel("Time (ms)", color=ColorPalette.get_hex("Denim Blue"))
        self.ax.grid(True, color=ColorPalette.get_hex("Baby Blue"), alpha=0.3)
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame_plot)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

    def update_plot(self):
        # Clear previous plot
        self.ax.clear()
        
        # Create scatter plots with array size on X axis and time on Y axis
        if self.search_history['linear']['times']:
            self.ax.scatter(self.search_history['linear']['sizes'], 
                           self.search_history['linear']['times'], 
                           label="Linear Search", color=ColorPalette.get_hex("Azalea Pink"), s=50)
            
            # Add trend line for linear search
            if len(self.search_history['linear']['times']) > 1:
                z = np.polyfit(self.search_history['linear']['sizes'], 
                              self.search_history['linear']['times'], 1)
                p = np.poly1d(z)
                sorted_sizes = sorted(self.search_history['linear']['sizes'])
                self.ax.plot(sorted_sizes, p(sorted_sizes), 
                            color=ColorPalette.get_hex("Azalea Pink"), alpha=0.5, linestyle='--')
        
        if self.search_history['binary']['times']:
            self.ax.scatter(self.search_history['binary']['sizes'], 
                           self.search_history['binary']['times'], 
                           label="Binary Search", color=ColorPalette.get_hex("Spring Green"), s=50)
            
            # Add trend line for binary search
            if len(self.search_history['binary']['times']) > 1:
                z = np.polyfit(self.search_history['binary']['sizes'], 
                              self.search_history['binary']['times'], 1)
                p = np.poly1d(z)
                sorted_sizes = sorted(self.search_history['binary']['sizes'])
                self.ax.plot(sorted_sizes, p(sorted_sizes), 
                            color=ColorPalette.get_hex("Spring Green"), alpha=0.5, linestyle='--')
        
        # Set plot properties
        self.ax.set_title("Algorithm Performance: Time vs Array Size", color=ColorPalette.get_hex("Denim Blue"))
        self.ax.set_xlabel("Array Size", color=ColorPalette.get_hex("Denim Blue"))
        self.ax.set_ylabel("Time (ms)", color=ColorPalette.get_hex("Denim Blue"))
        self.ax.legend()
        self.ax.grid(True, color=ColorPalette.get_hex("Baby Blue"), alpha=0.3)
        
        # Update canvas
        self.canvas.draw()
    
    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = Root()
    app.run()