import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation


class GraphPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.create_graph()

    def create_graph(self):
        # Create a figure and axis for the graph
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        # Generate some initial data
        self.x_data = [1, 2, 3, 4, 5]
        self.y_data = [1, 4, 9, 16, 25]

        # Create a line plot
        self.line, = self.ax.plot(self.x_data, self.y_data)

        # Create a canvas to display the graph
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def animate(self, i):
        # Generate new data for animation
        self.x_data.append(self.x_data[-1] + 1)
        self.y_data.append((self.x_data[-1] + 1) ** 2)

        # Update the line plot with new data
        self.line.set_data(self.x_data, self.y_data)

        # Adjust the plot limits if needed
        self.ax.relim()
        self.ax.autoscale_view()

    def on_enter(self):
        # Start the animation when entering the page
        self.animation = animation.FuncAnimation(self.fig, self.animate, interval=100)
        self.canvas.draw()

    def on_leave(self):
        # Stop the animation when leaving the page
        self.animation.event_source.stop()


class MainPage(tk.Frame):
    def __init__(self, parent, graph_page):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.graph_page = graph_page
        self.create_button()

    def create_button(self):
        button = tk.Button(self, text="Go to Graph Page", command=self.go_to_graph_page)
        button.pack()

    def go_to_graph_page(self):
        self.parent.show_frame(GraphPage)
        self.graph_page.on_enter()


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Tkinter Animated Graph Example")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.graph_page = GraphPage(self.container)
        self.add_frame(MainPage)

    def add_frame(self, frame_class):
        frame = frame_class(self.container, self.graph_page)
        self.frames[frame_class] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
