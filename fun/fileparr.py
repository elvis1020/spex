import f311.filetypes as ft
import pickle as pkl


class FileLibrary(dict):
    def update(self):
        print("Updatingggggggggggg")


class PlotState(dict):
    pass


class FileParr(ft.DataFile):
    def __init__(self):
        ft.DataFile.__init__(self)
        self.plot_state = PlotState()
        self.file_library = FileLibrary()

    # "override"
    def _do_load(self, filename):
        self.plot_state, self.file_library = pkl.load(open(filename, "rb"))


    def _do_save_as(self, filename):
        a = [self.plot_state, self.file_library]
        with open(filename, "wb") as file:
            s = pkl.dumps(a)
            # print(s)
            # print(type(s))
            pkl.dump(a, file)

