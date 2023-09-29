from constants.const import *
import pandas as pd
from itertools import product


def init_check(self) -> callable:
    ''' Function to check if all attributes are initialized. '''
    pass


class WSI:
    ''' Class Workshop is used to learn. '''

    def __init__(self, canales=None) -> object:
        self._canales: dict = canales
        self._estado_canal_f: pd.DataFrame = None
        self._estado_estado_f: pd.DataFrame = None
        self._estado_canal_p: pd.DataFrame = None
        self._estado_estado_p: pd.DataFrame = None

    def setup(self) -> tuple[bool, KeyError]:
        ''' Function to create the multiples matrixes. '''
        try:
            # Inicializar las matrices
            self.set_ecanales()
            self.set_eestados()
            return (True, None)
        except Exception as e:
            return (False, e)

    def fill_matrixes(self,  selector: int) -> bool:
        ''' Function to fill the matrixes. '''

        matrixes: dict[str: function] = {
            11: self.llenar_ecanal_f,
            22: self.llenar_eestado_f,
            
            33: self.llenar_ecanal_p, 
            44: self.llenar_eestado_p, 
        }
        return matrixes[selector]()

    def view_matrixes(self, selector: str) -> tuple[None, pd.DataFrame]:
        ''' Function to display the needed matrix '''

        matrixes = {
            1: self._estado_canal_f,
            2: self._estado_estado_f,
            3: self._estado_canal_p,
            4: self._estado_estado_p,
        }
        return matrixes[selector]

    # - Setters - #

    # ? TODO: Maybe a decorator can check this parameter and change the function att set ? #[00].

    def set_ecanales(self, estado: pd.DataFrame = None) -> None:
        ''' Function to initialize channel state f matrix.  '''

        canales: list[str] = list(self._canales.keys())
        filas: int = len(canales)

        big_key = ''.join(canales)
        perms = self.char_perm(bin_set, filas)

        matriz: dict[str:str] = {
            big_key: perms,
        }

        for i in range(filas):
            matriz[f'{canales[i]} (1)'] = ['' for _ in range(len(perms))]

        self._estado_canal_f = pd.DataFrame(matriz)
        self._estado_canal_f.set_index(big_key, inplace=True)
        
        self._estado_canal_p = pd.DataFrame(matriz)
        self._estado_canal_p.set_index(big_key, inplace=True)

        if estado is not None:
            self._estado_canal_f = estado

    def set_eestados(self, estado: pd.DataFrame = None) -> None:
        ''' Function to initialize the composed states matrix. '''

        canales: list[str] = list(self._canales.keys())
        filas: int = len(canales)

        perms = self.char_perm(bin_set, filas)
        big_key = ''.join(canales)

        matriz: dict = {
            big_key: perms,
        }

        for i in range(len(perms)):
            matriz[perms[i]] = ['' for _ in range(base**filas)]

        self._estado_estado_f = pd.DataFrame(matriz)
        self._estado_estado_f.set_index(big_key, inplace=True)

        self._estado_estado_p = pd.DataFrame(matriz)
        self._estado_estado_p.set_index(big_key, inplace=True)

        if estado is not None:
            self._estado_canal_f = estado

    def set_ecanal_p(self, estado: pd.DataFrame = None) -> None:
        ''' Function to initialize previous channel state matrix. '''

    def set_eestado_p(self, estado: pd.DataFrame = None) -> None:
        ''' Function to initialize the previous composed states matrix. '''

    # - Logic - #

    def llenar_ecanal_f(self) -> bool:
        ''' Function to get the full probability matrix. '''
        if self._canales is None:
            print('Error: Canales no inicializados.')
            return False

        canales: list[str] = list(self._canales.keys())
        rows: int = len(self._canales)
        cols: int = len(self._canales[canales[0]])

        # Crear diccionario de tamaño IN y asignarlo al conteo
        perms: list[str] = self.char_perm(bin_set, rows)
        conteo: dict[str: list[dict, int]] = {}

        for perm in perms:
            conteo[perm] = [{c: 0 for c in canales}, 0]

        # Range() toma un dominio semiabierto; [filas).
        # Si es la última clave, no se puede ver el siguiente.
        for i in range(cols):

            estado: str = ''  # Reinicio del estado (importante).

            # Concatenar los valores de cada canal en el ESTADO actual.
            for canal in canales:
                estado += f'{self._canales[canal][i]}'

            # Aumentar el conteo del estado actual (denominador).
            conteo[estado][1] += 1

            # No podemos evaluar el siguiente estado si es el último.
            if i != cols-1:
                for llave in canales:
                    conteo[estado][0][llave] += self._canales[llave][i+1]

        for perm in conteo:
            registros: list = [
                f'{conteo[perm][0][canal]}/{conteo[perm][1]}' for canal in canales
            ]
            self._estado_canal_f.loc[perm] = registros
        return True

    def llenar_eestado_f(self) -> bool:
        ''' Function to get the full probability matrix for the estado f. '''
        if self._canales is None:
            print('Error: Canales no inicializados.')
            return False

        canales: list[str] = list(self._canales.keys())
        rows: int = len(self._canales)
        cols: int = len(self._canales.get(canales[0]))

        perms: list[str] = self.char_perm(bin_set, rows)

        conteo: dict[str: list[dict[str: int], int]] = {}

        for perm in perms:
            conteo[perm] = [{p: 0 for p in perms}, 0]

        for i in range(cols):

            e_actual: str = ''
            for canal in canales:
                e_actual += f'{self._canales[canal][i]}'

            conteo[e_actual][1] += 1

            if i != cols-1:
                e_siguiente: str = ''
                for canal in canales:
                    e_siguiente += f'{self._canales[canal][i+1]}'
                conteo[e_actual][0][e_siguiente] += 1

        for estado in conteo:
            # (generar, reiniciar) lista de valores asignables al índex del dataf|matriz.
            valores: list = []
            estado_adj = conteo[estado][0]  # comodidad
            # Del sub-diccionario concatenamos los valores en cada fila de cada columnas
            for clave in estado_adj:
                self._estado_estado_f.at[
                    estado, clave
                ] = f'{estado_adj[clave]}/{conteo[estado][1]}'
        return True



    def llenar_ecanal_p(self) -> bool:
        ''' Function to get the full probability matrix. '''
        if self._canales is None:
            print('Error: Canales no inicializados.')
            return False

        canales: list[str] = list(self._canales.keys())
        rows: int = len(self._canales)
        cols: int = len(self._canales[canales[0]])

        # Crear diccionario de tamaño IN y asignarlo al conteo
        perms: list[str] = self.char_perm(bin_set, rows)
        conteo: dict[str: list[dict, int]] = {}

        for perm in perms:
            conteo[perm] = [{c: 0 for c in canales}, 0]

        # Range() toma un dominio semiabierto; [filas).
        # Si es la última clave, no se puede ver el siguiente.
        for i in range(cols):

            estado: str = ''  # Reinicio del estado (importante).

            # Concatenar los valores de cada canal en el ESTADO actual.
            for canal in canales:
                estado += f'{self._canales[canal][i]}'

            # Aumentar el conteo del estado actual (denominador).
            conteo[estado][1] += 1

            # No podemos evaluar el siguiente estado si es el último.
            # conteo = { ['a': 0, 'b': 0, ...], 0 } 
            if i != 0 :
                for llave in canales:
                    conteo[estado][0][llave] += self._canales[llave][i-1]

        for perm in conteo:
            registros: list = [
                f'{conteo[perm][0][canal]}/{conteo[perm][1]}' for canal in canales
            ]
            self._estado_canal_p.loc[perm] = registros
        return True
    


    def llenar_eestado_p(self) -> bool:

        ''' Function to get the full probability matrix for the estado f. '''
        if self._canales is None:
            print('Error: Canales no inicializados.')
            return False

        canales: list[str] = list(self._canales.keys())
        rows: int = len(self._canales)
        cols: int = len(self._canales.get(canales[0]))

        perms: list[str] = self.char_perm(bin_set, rows)

        conteo: dict[str: list[dict[str: int], int]] = {}

        for perm in perms:
            #dictionary comprehension
            #list comprehension
            conteo[perm] = [{p: 0 for p in perms}, 0]

        for i in range(cols):

            e_actual: str = ''
            for canal in canales:
                e_actual += f'{self._canales[canal][i]}'

            conteo[e_actual][1] += 1

            if i != 0:
                e_anterior: str = ''
                for canal in canales:
                    e_anterior += f'{self._canales[canal][i-1]}'

                conteo[e_actual][0][e_anterior] += 1

        for estado in conteo:
            # (generar, reiniciar) lista de valores asignables al índex del dataf|matriz.
            valores: list = []
            estado_adj = conteo[estado][0]  # comodidad
            # Del sub-diccionario concatenamos los valores en cada fila de cada columnas
            for clave in estado_adj:
                self._estado_estado_p.at[
                    estado, clave
                ] = f'{estado_adj[clave]}/{conteo[estado][1]}'

        return True

    # * libreria para ver 
    def char_perm(self, elements: list, size: int):
        ''' Function to permutate a set of characters '''
        combinaciones = list(product(elements, repeat=size))
        combinaciones_cadenas = [''.join(c) for c in combinaciones]
        return combinaciones_cadenas

   # ! matriz de prueba
    """
    {'A': (1, 1, 1, 1, 0, 0, 0, 1),
     'B': (1, 0, 0, 1, 1, 0, 1, 0),
    """
     # - Getters - #
    def set_canales(self, data):
        ''' Function to set the channels data. '''
        self._canales = data
  
