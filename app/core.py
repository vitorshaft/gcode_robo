from mainwin import MainWin
from commander import Commander

view = MainWin()
commander = Commander(view)

view.mainloop()