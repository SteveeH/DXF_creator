from tkinter import *
import tkinter as tk
import os


from tkinter.filedialog import askopenfilename
from tkinter import messagebox

from point import Point
import ezdxf


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # nastaveni minimalni sirky prvniho radku a sloupce
        self.master.columnconfigure(0, minsize=10)
        self.master.columnconfigure(2, minsize=10)
        self.master.rowconfigure(0, minsize=10)

        # promenne GUI
        self.var_row_count = StringVar(value="1")
        self.var_text_size = StringVar(value="0.1")
        self.var_space_before = IntVar(value=0)
        self.var_use_prefix = IntVar(value=0)
        self.var_dot_or_space = IntVar(value=0)
        self.var_show_zero_height = IntVar(value=0)
        self.var_input_file_name = StringVar(value="soubor nevybrán")
        self.var_output_file_name = StringVar(value="")
        self.input_file_name = ""
        self.dir_path = ""

        # promenne zpracovani
        self.points = []
        self.used_layers = []

        # po spusteni
        self.create_widgets()

    def create_widgets(self):

        frame_entry = Frame(self.master)

        frame_entry.grid(
            row=1, column=1, columnspan=3, sticky='W', padx=5)

        entry0 = Entry(
            frame_entry, width=4, textvariable=self.var_row_count, justify='center')
        entry0.grid(row=0, column=1,)

        label0 = Label(frame_entry, text=": počet řádků hlavičky",)
        label0.grid(row=0, column=3, sticky=W,)

        entry1 = Entry(frame_entry, width=4,
                       textvariable=self.var_text_size, justify='center')
        entry1.grid(row=1, column=1,)

        label1 = Label(frame_entry, text=": velikost všech textů",)
        label1.grid(row=1, column=3, sticky=W,)

        # Cislo bodu

        frame_number = LabelFrame(self.master, text="číslo bodu", width=180)
        frame_number.grid(row=2, column=1, columnspan=3, sticky='W', padx=5)

        rdb0 = Radiobutton(frame_number, text="mezera před číslem bodu",
                           variable=self.var_space_before, value=0)
        rdb0.grid(row=0, column=1, sticky=W,)

        rdb1 = Radiobutton(frame_number, text="bez mezery před číslem bodu",
                           variable=self.var_space_before, value=1)
        rdb1.grid(row=1, column=1, sticky=W,)

        chbtn0 = Checkbutton(
            frame_number, text="doplnit předčíslí bodu", variable=self.var_use_prefix)

        chbtn0.grid(row=2, column=1, sticky=W,)

        # Vyska bodu

        frame_height = LabelFrame(self.master, text="výška bodu", width=180)
        frame_height.grid(row=3, column=1, columnspan=3, sticky='W', padx=5)

        rdb2 = Radiobutton(frame_height, text="mezera místo tečky",
                           variable=self.var_dot_or_space, value=0)
        rdb2.grid(row=0, column=1, sticky=W,)

        rdb3 = Radiobutton(frame_height, text="desetinná tečka",
                           variable=self.var_dot_or_space, value=1)
        rdb3.grid(row=1, column=1, sticky=W,)

        chbtn1 = Checkbutton(
            frame_height, text="zobrazit nulovou výšku", variable=self.var_show_zero_height)

        chbtn1.grid(row=2, column=1, sticky=W,)

        # Vyber souboru

        frame_file = Frame(self.master)
        frame_file.grid(row=4, column=1, columnspan=3, sticky='W', padx=5)

        label2 = Label(frame_file, text="vyber soubor *.stx",)
        label2.grid(row=0, column=1, sticky=W,)

        entry2 = Entry(frame_file, width=25, textvariable=self.var_input_file_name, justify='right',
                       state=DISABLED)
        entry2.grid(row=1, column=1,)

        button0 = Button(frame_file, text=" ... ", relief=RAISED, border=1,
                         command=self.choose_input_file)
        button0.grid(row=1, column=3,)

        label3 = Label(frame_file, text="ulož jako *.dxf",)
        label3.grid(row=2, column=1, sticky=W,)

        entry3 = Entry(frame_file, width=25,
                       textvariable=self.var_output_file_name, justify='right')
        entry3.grid(row=3, column=1,)

        # ovladaci tlacitka

        frame_buttons = Frame(self.master)
        frame_buttons.grid(row=5, column=1, columnspan=6, sticky=W, padx=5)

        button1 = Button(frame_buttons, text="spustit", relief=RAISED, border=1,
                         font=("Verdana", 9), command=self.process_data)

        button1.grid(row=0, column=1,)

        frame_buttons.columnconfigure(2, minsize=10)

        button2 = Button(frame_buttons, text="konec", relief=RAISED, border=1,
                         command=self.close_app, font=("Verdana", 9))
        button2.grid(row=0, column=3, pady=5,)

    def choose_input_file(self):

        input_file_name = askopenfilename()

        dir_path, file_name = os.path.split(input_file_name)

        self.input_file_name = input_file_name
        self.dir_path = dir_path

        self.var_input_file_name.set(file_name)
        self.var_output_file_name.set(file_name.split(".")[0] + ".dxf")

    def process_data(self):

        # reinicializace promennych
        self.points = []
        self.used_layers = []

        if os.path.exists(self.input_file_name):
            print("Zpracovávám soubor : {}".format(
                self.input_file_name))

            with open(self.input_file_name, "r") as file:
                for line in file.readlines():
                    self.points.append(Point(line))

            valid_points = [point for point in self.points if point.is_valid]
            print("Načteno {} validních bodů".format(len(valid_points)))

            # vytvoreni odkazu na DXF soubor
            drawing = ezdxf.new(dxfversion='AC1018')
            # nastaveni jednotek vykresu 0 - bez jednotek, 1 - inche, 6 - metry
            drawing.header['$INSUNITS'] = 0
            modelspace = drawing.modelspace()

            for p in valid_points:

                point_layer = p.get_layer()

                if point_layer not in self.used_layers:
                    drawing.layers.new(point_layer, dxfattribs={'color': 2})
                    self.used_layers.append(point_layer)

                # prohozeni kvadrantu souradnic z S-JTSK do matematickeho
                modelspace.add_point((-p.get_y(), -p.get_x()), dxfattribs={
                                     'layer': point_layer})
                modelspace.add_text(str(p.get_z()), dxfattribs={'layer': point_layer}).set_pos(
                    (-p.get_y(), -p.get_x()), align='CENTER')

            # ulozeni
            drawing.saveas(os.path.join(
                self.dir_path, self.var_output_file_name.get()))

        else:
            messagebox.showerror(
                "Chyba", "Zadej korektní cestu ke vstupnímu souboru!")

    def close_app(self):
        print("Ukončuji aplikaci")
        # TODO uložení předchozího nastavení nebo něco dalšího
        self.master.destroy()


if __name__ == "__main__":

    program_version = "2021.1"

    root = tk.Tk()
    root.title("DXF creator - version {}".format(program_version))
    root.resizable(width=False, height=False)
    root.geometry("210x380+40+40")

    app = Application(master=root)
    app.mainloop()
