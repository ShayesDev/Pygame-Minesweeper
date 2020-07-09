from cx_Freeze import setup, Executable

setup(name="Minesweeper",
      version="0.1",
      description="A remake of the original Minesweeper game",
      executables = [Executable("main.py",base="Win32GUI")])
