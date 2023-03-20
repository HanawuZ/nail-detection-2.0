# Python GUI 

We use python(3.10.6) to show GUI, create Servo to press nail, and use camera to detect nail area when blood is restore to nail and plot graph interval time and desity of blood in nail

## MultipleProcessing

in this case we using `class ___(mp.Process)` to Multiple Processing to process video in file and record video (i use this because `class View(Tk)` is using Single processing only so we should create new class to using multiple processing [reference How To using Processing from stackoverflow solution](https://stackoverflow.com/questions/70318766/tkinter-and-multiprocessing-cannot-pickle-tkinter-tkapp-object))

so i hope this code is working....
