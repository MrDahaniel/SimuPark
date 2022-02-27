# Simulación Digital: Avance Proyecto Final

-   Paula Catalina Hernández Ramírez 2180048 - Moderador
-   Juan Pablo Claro Pérez – 2181707 - Relator
-   Daniel David Delgado Cervantes - 2182066 - Expositor

## Resumen

El presente documento examina una problemática que se presenta en cualquier lugar donde se encuentre una cantidad excesiva de personas y haya la necesidad de hacer filas. La teoría de colas es un estudio matemático que busca entender el comportamiento de las líneas de espera dentro de un sistema, donde el cliente presenta una solicitud para que se le presten un servicio y este a su vez dependerá de una variante, la demanda, ya que con esta se determina el tiempo de espera que debe tener la persona hasta obtener lo que requiere. El ecosistema a estudiar se presenta dentro
de los parques de diversiones, en los cuales se presentan problemas a la hora de ingresar a diferentes atracciones, donde las personas pueden durar mucho mas tiempo realizando las colas que divirtiéndose en los juegos. Siuación que además de desafortunada para el cliente, también lo será para el parque de diversiones, pues entre más cómoda sea la espera a las atracciones, mayores serán las probabilidades de que la persona quiera volver al parque. Es por ello que se plantea: ¿Existirá alguna forma para que las personas puedan divertirse más y así disminuir el tiempo de espera en las diferentes atracciones?

## Introducción

La teoría de líneas de espera inicia con el trabajo de Agner Krarup Erlang matemático Danés, el cual en el estudio de líneas telefónicas obtuvo la fórmula para la distribución del número de líneas de espera, a partir de aquí la teoría de colas se aplica en un sinfín de estudios encargados del comportamiento de sistemas como el tráfico automovilístico, las filas de un banco o el flujo de mensaje.

El objetivo principal de la teoría de colas es modelar el sistema que presenta estas líneas de
espera, con el fin de observar el comportamiento y posibles alternativas de solución para obtener el resultado más optimo según el estudio que se realice. Teniendo esto presente, la teoría de colas será fundamental para el desarrollo del estudio, este se centrará en el sistema que conforma un parque de diversiones, donde se concentra una población grande de personas, las cuales desean probar cada atracción presente.

Este sistema a estudiar presenta múltiples variables ya que no se van a presentar los mismos
escenarios, puede influir ya sea la hora del día, un fecha especial en el año, el clima, los precios de cada una de las atracciones, la fama de cada juego, entre otras. Las ferias encargadas de los
parques de diversiones han aplicado una transformación al sistema donde se usa el Fast Pass, este es un método para agilizar las colas, pero ¿Es efectivo? ¿Las personas invierten menos tiempo en esperas y más en divertirse?

## Formulación Del Problema

Uno de los principales problemas que se presentan en cualquier tipo de cola, o fila, está en el tiempo de espera que implica estar en estas. Este tiempo de espera depende de 2 variables: la tasa de servicio, o el tiempo en el cual sale gente de la fila; y la tasa de llegada, que se refiere a la velocidad con la que ingresan personas a la fila. Es a partir de esto que funcionan todas las colas.

Los parques de diversiones son centros de recreación que atraen a multitudes de personas que desean disfrutar de las distintas gamas de atracciones que se manejan. Siendo así, uno de los problemas a los que tienen que enfrentarse tanto los visitantes son las largas colas que se pueden presentar en muchas de las atracciones. Esto, en el peor de los casos, puede generar descontento en los visitantes debido a la gran cantidad de tiempo que perdieron esperando, lo que a la larga, podría afectar la reputación del parque y las ganancias del mismo.

Partiendo de esto, el problema que se busca solucionar son estas mismas colas, y las diferentes técnicas que se pueden emplear para poder reducir el tiempo de espera promedio de los visitantes. De esta manera, se busca mejorar la experiencia general del público asistente que, en respuesta, implicaría una mejora de los ingresos generados por el parque.

## Objetivos

### Objetivo General

-   Analizar el comportamiento de las filas de las atracciones de un parque de diversiones a partir de simulaciones computacionales para determinar qué estrategias son más efectivas para la reducción del tiempo de espera promedio.

### Objetivos Específicos

-   Determinar qué estrategia conlleva la mayor reducción del tiempo de espera en las colas del parque.
-   Identificar los diferentes factores que se relacionan con el tiempo de espera promedio de cada una de las atracciones del parque.
-   Determinar las diferentes limitaciones que presenta el parque en cuanto el manejo de las colas de cada una de sus atracciones.
-   Analizar qué tanto se puede incrementar el flujo de visitantes a un parque de diversiones y si la cantidad de atracciones en las que se subieron aumentó con un cambio de estrategia FastPass.

## Plan General Del Proyecto

### Justificación Del Problema

Los parques temáticos y sus diferentes atracciones y actividades son disfrutadas cada año por millones de turistas de todas partes. Un problema al cual se enfrentan los parques temáticos es la espera en las largas filas para ingresar a cada atracción, y estas son incluso peores cuando se trata de dias fesivos o vacaciones. El presente proyecto busca entonces la determinación de la efectividad de diferentes estrategias en la reducción de los tiempos de espera promedio en las colas de las atracciones de un parque. A partir de esto se espera encontrar las maneras más óptimas de reducir las colas en un parque con el fin de proveer una mejor experiencia a los visitantes del mismo. De igual manera, se espera que tras el desarrollo del presente proyecto, los datos recolectados en el mismo permitan la adopción de estas estrategias en otros campos en los cuales la teoría de colas toma lugar.

### Modelos Alternos

Dentro del proyecto, se busca el evaluar diferentes escenarios con el fin de realizar determinación de cuales estrategias dentro del manejo de las filas del parque, permite la mayor reducción del tiempo de espera promedio para los visitates del parque.

#### FastPass de Disney

El primer modelo se basa en la implementación de filas alternas para cada una de las atracciones del parque. Estas filas se destacan por ser filas virtuales en las cuales el lugar dentro de esta está determinada por un intervalo de tiempo. Estos lugares son repartidos durante el transcurso del día a los visitantes del parque los cuales únicamente pueden tener un FastPass.

#### FastPass Salitre

Así mismo, tenemos el caso de una fila alterna constante en la cual hay que realizar un pago adicional en el momento de realizar la compra del tiquete para poder entrar. En este caso, los visitantes que hayan realizado la compra, podrán ignorar la fila principal y hacer una fila más corta la cual les permitirá subierse a más atracciones debido al tiempo de espera menor.

#### Tiempos Falsos

Finalmente, tenemos la estrategia de tiempos falsos. Esta estrategia busca el mostrar tiempos de espera diferentes a los reales, normalmente superiores, con el fin de interesar o disuadir a los visitantes de unirse a las filas de ciertas atracciones con el fin de repartir mejor la carga de los visitantes a través de todo el parque.

### Cronograma

-   ¿Qué actividades se van a realizar y en qué fechas van a ser realizadas?

![](https://i.imgur.com/k9jftka.png)

## Conceptualización del modelo

El modelo empleado como punto de partida en el estudio de la simulación del comportamiento de las colas de espera presentadas en un parque de atracciones se puede ver simplificado en el siguiente diseño, el cual cuenta con ciertos componentes en los que se involucra la conducta o 'arquetipo' de cada persona a la hora de recurrir a las diferentes atracciones, las actividades que la persona podría elegir, las atracciones, y muchas más variables que influirán en la ejecución de la simulación:

![diseño_base](https://imgur.com/D80tmov.png)

Se inicia con el estudio de las diferentes personas, sus gustos y arquetipos para obtener una lectura que permita crear un mapa global de cada una de las distintas opciones que puede elegir las personas, tomando el arquetipo como punto de partida para obtener los gustos que pueden presentar los visitantes en el modelo.

El parque de atracciones contará con la entidad de actividades que determina cada una de las opciones que pueden seleccionar las personas, teniendo en consideración que cada actividad presente puede ser una atracción distinta, la cual cuenta con tiempo de espera y un tiempo de servicio en la que cada persona puede participar.

El concepto estudiado en modelo parte desde un caso base presente en cada uno de los parque de atracciones en el cual no se emplean técnicas para mejorar la conducta de las colas sino empleando el sistema FIFO, este caso base se centra en un flujo donde la persona al ingresar al parque selecciona si desea realizar una actividad o si por el contrario decide emplear tiempo en la cola de espera de una de las atracciones para disfrutar de ella, luego de esto la persona decide si desea realizar otra actividad o ingresar a otra atracción hasta que esta decida irse, teniendo como resultado el siguiente diagrama:

![](https://imgur.com/gCywLid.png)

A su vez se desea comparar este modelo tradicional del funcionamiento de los parques de atracciones con otros modelos que emplean tácticas para que sus sistemas de espera faciliten la movilidad de los usuarios, teniendo presente esto, el modelo con un diseño como el del SalitrePass presenta una modificación en los tiempos de espera presente en cada una de las atracciones. La persona puede elegir si entrar a una fila normal o la fila perteneciente al SalitePass, esto depende del tiempo de espera presentante en cada una y de la decisión de la persona.

![](https://imgur.com/uJwzvGn.png)

Otro modelo de comparación es el empleado en los parques de diversiones de Disney donde presentan una facilidad llamada FastPass donde la persona que presenta el FastPass debe presentarse frente a la atracción a la hora especificada en el comprobante, esto con el fin de que la persona no realice filas sino que ingrese directamente a la atracción o actividad, de lo contrario decidirá si quiere unirse a la fila, comprar un FastPass para la atracción o realizar otra actividad, teniendo como resultado el siguiente flujo:

![](https://imgur.com/LNKBfEc.png)

## Recoleción de datos

La recolección de cada uno de los datos se realiza tomando los diferentes gustos de las distintas personas que desean asistir a un parque de diversiones, tomando en cuenta el nivel de tiempo que deseen emplear dentro del mismo y agregando el tiempo de espera que desean gastar en cada una de las colas para ingresar a cada actividad o atracción esto con el fin de estimar lo más cercano posible lo que sucedería en diferentes situaciones presenten en el parque.

Estos datos serán recolectados por medio de encuestas donde las personas elegirán los diferentes rasgos que los caracterizan y así poder agruparlos, para tener una lectura global del comportamiento de cada una, de este modo se desea poner a prueba la implementación del modelo y los diferentes métodos que los modelos alternativos presentan.

Los datos obtenidos serán empleados en el modelo con el fin de obtener una lectura de lo que sucedería en cada caso presentando el caso base y las diferentes alternativas que pretenden solucionar el problema de los tiempos de espera dentro de cada atracción.

## Prototipo Implementado

El primer prototípo del parque a simular tiene varios componentes. El primero de estos componentes son las personas. Estas se encargan, en escencia de visitar el parque, tomar decisiones de lo que harán dentro del parque, y hacer tanto como actividades como hacer filas para las atracciones. Estas personas están definidas por un arquetipo, el cual define 3 componentes: la probabilidad de escoger hacer una actividad o buscar una atracción, el tiempo de estadía en el parque y el tiempo máximo que esperará en una fila. Pueden verse estos 2 módulos [aquí](https://gitlab.com/MrDahaniel/proyecto-simulacion/-/blob/main/simuPark/person.py).

Seguidamente, tendremos la parte de la infraestructura la cual se refiere a el parque, las atracciones, actividades y las filas. El parque está definido como el contenedor de todas las partes que lo contienen, contiene la información de todos los visitantes, atracciones y actividades; debido a esto es el que se encarga de realizar como tal la simulación de las personas y la actulización de todas las partes que contiene. Las actividades y las atracciones se refieren a las cosas que las personas pueden hacer en el parque, las actividades tienen una popularidad y una duración las cuales determinen la probabilidad de que una persona decida hacer esa actividad y el tiempo que estará ocupado dentro de la fila, respectivamente.

Finalmente, las filas se refiere a los lugares en los cuales las personas esperan a subierse a las atracciones. Estas son nuestro principal interés pues es dentro de las filas que los tiempos de espera son aumentados y determinan, dependiendo de la velocidad del servicio, la cantidad de atracciones que las personas pueden disfruta. Pueden verse estos 4 módulos [aquí](https://gitlab.com/MrDahaniel/proyecto-simulacion/-/blob/main/simuPark/park.py).

Ahora, podemos ver un ejemplo de la simulación del parque.

```python=
# Importamos nuestras librería para la simulación
from simuPark.park import Activity, Attraction, Park
from simuPark.person import Person, Archetype

# Creamos nuestra instancia de Park
park = Park()

# Iniciamos la simulación de un día
park.startDayBase(100000)

print(len(park.guests))

y = [guest.arrivalTime for guest in park.guests]

hist(y, bins=40);

print([i.name for i in park.activities])
print([i.name for i in park.attractions])
print([i.name for i in park.guestArchetypes])
```

```python=
7852
['Walk15', 'Walk10', 'ShopGifts', 'EatRestaurant', 'BathroomBreak', 'TakePictures']
['Dropper', 'Tornado', 'BumpCars', 'SlowRiver', 'StarWarsRide', 'SpaceMountain']
['Tourist']
```

![](https://i.imgur.com/4H3J6sf.png)

Aquí podemos ver la entrada de las personas al parque dentro de la simulación. Esta está definidas por la función de entrada. En este caso, entraron un total de `7852` personas al parque.

```python=
attrExp = [guest.attractionsExperienced for guest in park.guests]
attrExp
hist(attrExp, bins=12, density=True);
```

![](https://i.imgur.com/P8UAlPN.png)

Así mismo, podemos ver el histograma de la cantidad de atracciones que las personas experimenteron en su visita. En este caso, debido a la poca cantidad de asistentes, la moda es mayor que 5 lo cual es bastante positivo.

```python=
avgWaitTime = []

for guest in park.guests:
    if guest.attractionsExperienced == 0:
        continue

    avgWaitTime.append(guest.totalWaitTime / guest.attractionsExperienced)

print(np.mean(avgWaitTime))
hist(avgWaitTime, density=True);
```

```python=
34.4957767876566
```

![](https://i.imgur.com/ACCQvzk.png)

Y finalmente podemos ver el tiempo de espera de los visitantes del parque. En este caso, la moda está por encima de los 40 minutos aunque el tiempo promedio de espera es de `34.4957767876566`.

## Bibliografía

-   Predecir los tiempos de espera de Disneyland a través de simulaciones de población. (s.f.). Ichi Pro. Disponible [aquí](https://ichi.pro/es/predecir-los-tiempos-de-espera-de-disneyland-a-traves-de-simulaciones-de-poblacion-36233626878710).
-   Datos sobre tiempos de espera en parque de diversiones. (s.f.). Minitab. Disponible [aquí](https://support.minitab.com/es-mx/datasets/quality-tools-data-sets/amusement-park-wait-times/).
-   Disney World Wait Times Available for Data Science and Machine Learning. (s.f.). touringplans. Disponible [aquí](https://touringplans.com/blog/disney-world-wait-times-available-for-data-science-and-machine-learning/).
-   Análisis De Líneas De Espera A Través De Teoría De Colas Y Simulación. (2010). Portilla, L. et al.
-   Managing Capacity And Flow At Theme Parks. (1996). Reza H. Ahmadi.
