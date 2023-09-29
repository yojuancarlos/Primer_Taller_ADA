from constants.const import *
from content.wsi import WSI


class UI:
    ''' Class Ui is used to view the retrieved data from the workshops. '''

    def __init__(self) -> None:
        self._wsi: WSI = WSI()

    def setup(self) -> bool:
        ''' Function to set the channels data. '''
        print(CANALM)

        # ? Toggle if you want the deffault data ? #
        self._wsi.set_canales(CANALM)  # !
        return True

    def cmd(self) -> None:
        ''' Function to display the needed matrix '''
        if not self.setup():
            print('Error (setup): Channels couldn\'t be set.')
            return

        if not self._wsi.setup()[0]:
            print(f'Error (setup): {self._wsi.setup()[1]}')
            return

        options: tuple[str] = (
            1, 2, 3, 4,
            11, 22, 33, 44
        )

        while True:
            question: tuple[str] = (
                '\n|1) Ver estado del canal Forward   |11) Llenar A |'
                '\n|2) Ver estado del estado Forward  |22) Llenar B |'
                '\n|3) Ver estado del canal Previous  |33) Llenar C |'
                '\n|4) Ver estado del estado Previous |44) Llenar D |'
                '\n|0) Salir                          |             |'
                '\n'
                '\n|> Select a matrix to display: '
            )
            try:
                data: str = int(input(question))

                if data == 0:
                    self.salir()

                if data not in options:
                    print(f'Error (ui): Invalid selector, only {options}.')

                if data > 10:
                    if not self._wsi.fill_matrixes(data):
                        print(f'Error (wsi): Matrix couldn\'t be filled.')
                        pass
                    else:
                        print('Matrix filled successfully.')
                else:
                    view = self._wsi.view_matrixes(data)
                    print(view)

            except ValueError:
                print('Error (ui): Invalid integer selector.')

    def salir(self) -> None:
        ''' Function to exit the program. '''
        print('Thanks for using this program.')
        exit(0)
