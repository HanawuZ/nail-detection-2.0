from multiprocessing import *
from tkinter import *
import time

def main():
    main = UIClass()


class UIClass:
    def __init__(self):
        self.queue = Queue()
        self.create_gui()

    def create_gui(self):
        self.ui_root = Tk()
        btn = Button(self.ui_root, text="Button", command=self.button_pressed)
        btn.pack()
        self.ui_root.mainloop()

    def button_pressed(self):
        print("Button pressed")
        self.ui_root.after(1000, self.check_results)
        self.dummy_processing()

    def dummy_processing(self):
        nr_list = [1, 2, 3, 4, 5]
        for secs in nr_list:
            process = TestProcess(self.queue, secs)
            process.start()

    def check_results(self):
        print("Checking results")
        try:
            result = self.queue.get(timeout=0.1)
            print("Result is " + str(result))
        except Exception as e:
            print("No results yet, waiting again")
        self.ui_root.after(1000, self.check_results)


class TestProcess(Process):
    def __init__(self, queue, secs):
        Process.__init__(self)
        self.queue = queue
        self.secs = secs

    def run(self):
        print("Run in process")
        result = self.process(self.secs)
        self.queue.put(result)

    def process(self, secs):
        time.sleep(secs)
        print("Done sleeping")
        return secs


if __name__ == '__main__':
    main()