## integrantes
juancarlos saldarriaga urrea  


valeria avila nieto
## Installations:
The following installations are required to run this project:
- __Virtual environment__ (preferible)
Use of `python -m venv venv` to set up a virtualenv into your system, then procceed to activate it with:
  - __Windows:__ `source venv/Scripts/activate.bat`
  - __Linux:__ `source venv\bin\activate`

- __Pandas__
Use of `python -m pip install pandas` to get pandas into your virtual environment.
Or use `python -m pip install -r requirements.txt` to install all the requirements for this project.

To run the app after the project setup you need to access with `cd app/` to the `app/` folder and run `python main.py` in your terminal.

# Project Definition
## Problema: Introducción
Se reciben _n_ muestras que ingresará el usuario, donde cada muestra cuenta con datos que provienen de _m_ canales (inicialmente valores binarios):

Se tienen _30_ muestras que provienen de _3_ canales:
|               | T1  | T2  | T3  | T4  | T5  | T6  | T7  | T8  | T9  | T10 | T11 | T12 | T13 | T14 | T15 | T16 | T17 | T18 | T19 | T20 | T21 | T22 | T23 | T24 | T25 | T26 | T27 | T28 | T29 | T30 |
| ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| _**Canal A**_ | 0   | 1   | 1   | 0   | 1   | 1   | 0   | 0   | 0   | 1   | 0   | 1   | 0   | 0   | 1   | 0   | 1   | 0   | 0   | 0   | 1   | 1   | 0   | 0   | 0   | 1   | 1   | 1   | 0   | 0   |
| _**Canal B**_ | 0   | 0   | 0   | 1   | 1   | 0   | 0   | 1   | 0   | 0   | 1   | 0   | 0   | 0   | 1   | 1   | 0   | 0   | 1   | 0   | 0   | 1   | 0   | 0   | 0   | 0   | 1   | 1   | 1   | 0   |
| _**Canal C**_ | 0   | 1   | 0   | 1   | 0   | 0   | 1   | 0   | 0   | 1   | 1   | 0   | 0   | 0   | 0   | 1   | 1   | 0   | 0   | 0   | 0   | 1   | 0   | 0   | 1   | 1   | 1   | 0   | 0   | 0   |
|               | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10  | 11  | 12  | 13  | 14  | 15  | 16  | 17  | 18  | 19  | 20  | 21  | 22  | 23  | 24  | 25  | 26  | 27  | 28  | 29  | 30  |

1. A partir de los datos deben generar la matriz **EstadoCanalF** que describe cuantas veces el estado actual de un sistema especifica los posibles estados próximos de cada canal en un tiempo inmeditamente siguiente. Este valor básicamente se calculará como la probabilidad de que el estado próximo este en un valor, dado que el estado actual está en algún valor determinado. Por ejemplo, la entrada superior izquierda de la matriz es _(3/4)_, que representa la cantidad de veces que el _Canal A_ estará en 1 en el tiempo _Ti+1_ (para este ejemplo 3) dado que los canales _ABC_ estuvieron en _000_ en el tiempo _Ti_ (para este ejemplo 4);

    | __ABC__ | __Canal A__ | __Canal B__ | __Canal C__ |
    | ------- | ----------- | ----------- | ----------- |
    | 000     | 3/4         |             |             |
    | 100     |             |             |             |
    | 010     |             |             |             |
    | 110     |             |             |             |
    | 001     |             |             |             |
    | 101     |             |             |             |
    | 011     |             |             |             |
    | 111     |             |             |             |


2. A partir de los datos de entrada deben generar la matriz __EstadoEstadoF__, que describe cuantas veces el estado actual de un sistema especifica los posibles estados próximos de todo el sistema en un tiempo siguiente. Este valor básicamente se calculará como la probabilidad de que el estado próximo esté en un valor,  dado que el estado actual está en algún valor determinado. Por ejemplo, la entrada superior izquierda de la matriz es _0_, que representa la cantidad de veces que los canales _ABC_ estarán en _000_ en el tiempo _Ti+1_, dado que los canales _ABC_ estuvieron en _000_ en el tiempo _Ti_.  Se aprecia que después de los estados _000_ resaltados en amarillo no aparece inmediatamente después ninguna tupla con _000_;

    | ABC\CBA | 000 | 100 | 010 | 110 | 001 | 101 | 011 | 111 |
    | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
    | 000     | 0   | 1/4 | 0   | 0   | 0   | 1/4 | 0   | 2/4 |
    | 100     |     |     |     |     |     |     |     |     |
    | 010     |     |     |     |     |     |     |     |     |
    | 110     |     |     |     |     |     |     |     |     |
    | 001     |     |     |     |     |     |     |     |     |
    | 101     |     |     |     |     |     |     |     |     |
    | 011     |     |     |     |     |     |     |     |     |
    | 111     |     |     |     |     |     |     |     |     |


3. 	Se debe generar la matriz __EstadoCanalP__ que describe cuantas veces el estado de un sistema es especificado por los posibles estados previos de cada canal en un tiempo inmediatamente anterior. Este valor básicamente se calculará como la probabilidad de que el estado previo esté en un valor, dado que el canal actual está en algún valor determinado.

4.	Se debe generar la matriz __EstadoEstadoP__ que describe cuantas veces el estado de un sistema es especificado por los posibles estados previos del sistema en un tiempo anterior. Este valor básicamente se calculará como la probabilidad de que el estado previo esté en un valor, dado que el estado actual está en algún valor determinado.


## Metodología
Se manejarán los siguientes dataframes para el almacenamiento y análisis de los datos:

Para la inserción de data en **EstadoCanalF** se trabajará una tabla con valores de _0_ o '' (vacío):
| ABC | A (1) | B (1) | C (1) |
| --- | ----- | ----- | ----- |
| 000 | 0     | 0     | 0     |
| 100 | 0     | 0     | 0     |
| 010 | 0     | 0     | 0     |
| 110 | 0     | 0     | 0     |
| 001 | 0     | 0     | 0     |
| 101 | 0     | 0     | 0     |
| 011 | 0     | 0     | 0     |
| 111 | 0     | 0     | 0     |

Para la inserción de data en **EstadoEstadoF** se trabajará una tabla con valores de _0_ o '' (vacío):
| ABC\ABC | 000 | 100 | 010 | 110 | 001 | 101 | 011 | 111 |
| ------- | --- | --- | --- | --- | --- | --- | --- | --- |
| 000     | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   |
| 100     | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   |
| 010     | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   |
| 110     | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   |
| 001     | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   |
| 101     | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   |
| 011     | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   |
| 111     | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   |

### Planteamientos:
Hemos de definir un estado como la combinación concatenada de caracteres en una posición _i_ del máximo de canales disponibles.

Este es un problema de conteo, por lo que se debe tener en cuenta que:
__Primer enunciado:__
- Iteraremos sobre cada muestra de cada canal (iteramos los estados) un total de _i_ veces hasta _i=m_ fuera _m_ el número de muestras común a todo canal.
En el proceso se formará un estado, cual adicionará _1_ a su estado respectivo.
- Iteramos además sobre los canales siguientes al estado actual, definido como _i+1_ siempre y cuando sea menor a _m_. El dato seleccionado será adicionado al conteo del estado actual en su canal específico.
- Asignaremos a la tabla __EstadoCanalF__ la relación de los conteos de cada estado _i_ y los conteos respectivos a cada canal _i+1_.

__Segundo enunciado:__
- Iteraremos sobre cada muestra de cada canal (iteramos los estados) un total de _i_ veces hasta _i=m_ fuera _m_ el número de muestras comunes a todo canal.
- Se da un conteo lineal de los estados, donde se adiciona _1_ al estado actual.
-  Se tendrá por cada estado actual el listado permutacional de estados siguientes (estado _i+1_),  se les asignará _1_ al respectivo estado siguiente del estado actual.
-  La relación del conteo entre el total de cada estado siguiente y el total de llamadas al estado actual.
-  La relación dicha será asignada en la tabla __EstadoEstadoF__.

## Resultados
Tabla __EstadoCanalF__ resultante:
|  ABC  | A (1) | B (1) | C (1) |
| :---: | :---: | :---: | :---: |
|  000  |  3/4  |  2/4  |  4/4  |
|  100  |  0/2  |  1/2  |  1/2  |
|  010  |  3/4  |  1/4  |  4/4  |
|  110  |  1/3  |  2/3  |  3/3  |
|  001  |  2/3  |  2/3  |  0/3  |
|  101  |  2/5  |  4/5  |  2/5  |
|  011  |  3/4  |  2/4  |  2/4  |
|  111  |  1/5  |  2/5  |  1/5  |

Tabla __EstadoEstadoF__ resultante:
| ABC\ABC | 000 | 100 | 010 | 110 | 001 | 101 | 011 | 111 |
| ------- | --- | --- | --- | --- | --- | --- | --- | --- |
| 000     | 0/4 | 0/4 | 0/4 | 0/4 | 1/4 | 1/4 | 0/4 | 2/4 |
| 100     | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 1/2 | 0/2 |
| 010     | 0/4 | 0/4 | 0/4 | 0/4 | 1/4 | 2/4 | 0/4 | 1/4 |
| 110     | 0/3 | 0/3 | 0/3 | 0/3 | 0/3 | 1/3 | 2/3 | 0/3 |
| 001     | 0/3 | 1/3 | 1/3 | 1/3 | 0/3 | 0/3 | 0/3 | 0/3 |
| 101     | 0/5 | 1/5 | 2/5 | 0/5 | 0/5 | 0/5 | 1/5 | 1/5 |
| 011     | 1/4 | 0/4 | 0/4 | 1/4 | 0/4 | 1/4 | 0/4 | 1/4 |
| 111     | 2/5 | 0/5 | 1/5 | 1/5 | 1/5 | 0/5 | 0/5 | 0/5 |

Nótese la diferencia fundamental en el orden de las variables, puesto en este caso he decidido tomar _A_ como la variable más significativa. En el planteamiento se tomo _C_ como la más significativa, _A_ como la menos.

## Conclusiones
Se puede apreciar que la probabilidad de que el estado próximo esté en un valor, dado que el estado actual está en algún valor determinado es mayor en el caso de la tabla __EstadoCanalF__ que en la tabla __EstadoEstadoF__. Esto se debe a que en la tabla __EstadoCanalF__ se toma en cuenta el estado actual de un canal, mientras que en la tabla __EstadoEstadoF__ se toma en cuenta el estado actual de todo el sistema.
Se puede dar por satisfactorio el resultado obtenido, hay coincidencia con los valores esperados en la tabla de ejemplo.