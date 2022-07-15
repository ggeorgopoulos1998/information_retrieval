import tkinter as tk
root = tk.Tk()
root.title('background image')
# pick a .gif image file you have in the working directory
fname = "1.png"
bg_image = tk.PhotoImage(file=fname)
# get the width and height of the image
w = bg_image.width()
h = bg_image.height()
# size the window so the image will fill it
root.geometry("%dx%d+50+30" % (w, h))
cv = tk.Canvas(width=w, height=h)
cv.pack(side='top', fill='both', expand='yes')
cv.create_image(0, 0, image=bg_image, anchor='nw')
# add canvas text at coordinates x=15, y=20
# anchor='nw' implies upper left corner coordinates
# now add some button widgets
btn1 = tk.Button(cv, text="Login")
btn1.pack(side='left', padx=10, pady=5, anchor='sw')
btn2 = tk.Button(cv, text="Register", command=root.destroy)
btn2.pack(side='left', padx=10, pady=5, anchor='sw')
root.mainloop()