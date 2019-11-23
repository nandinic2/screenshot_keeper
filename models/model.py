import pyautogui
import time
#import tkMessageBox








#top = Tkinter.Tk()

#def helloCallBack():
 #  tkMessageBox.showinfo( "Hello Python", "Hello World")

#B = Tkinter.Button(top, text ="Hello", command = helloCallBack)

#B.pack()
#top.mainloop()


def screenshot():
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    pyautogui.screenshot('/Users/2020nchakravorty/Desktop/screenshot/app/pictures/img.png')
    time.sleep(2)
