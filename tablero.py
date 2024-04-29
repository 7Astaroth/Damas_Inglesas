from tkinter import *


class Tablero(Tk):
    # Método init principal
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dimensiones del canvas
        self.geometry("640x640+500+150")
        self.tablero = Canvas(self)
        self.tablero.pack(fill="both", expand=1)
        self.estado_tablero = [[None for _ in range(8)] for _ in range(8)]
        self.casillas()
        self.piezas()
        self.casilla_seleccionada = None  # Para mantener la casilla seleccionada actualmente
        self.casillas_resaltadas = []  # Para mantener un registro de las casillas adyacentes resaltadas
        self.tablero.bind("<Button-1>", self.clic_pieza)

    # Dimension de tablero y casillas.
    def casillas(self):
        # Iteración para crear las casillas
        for i in range(8):
            for x in range(8):
                if (i + x) % 2 == 0:
                    fill_color = "black"
                else:
                    fill_color = "gray"
                # Crear la casilla
                casilla_id = self.tablero.create_rectangle(i * 80, x * 80, (i + 1) * 80, (x + 1) * 80, fill=fill_color)
                # Etiquetar la casilla con su fila y columna
                self.tablero.itemconfig(casilla_id, tags=('casilla_{}_{}'.format(x, i)))

    def piezas(self):
        
        piezas_blancas = [
            # posiciones de fichas blancas
            (1, 0), (3, 0), (5, 0), (7, 0),
            (0, 1), (2, 1), (4, 1), (6, 1),
            (1, 2), (3, 2), (5, 2), (7, 2),
        ]
        piezas_oscuras = [
            # posiciones de fichas negras
            (0, 5), (2, 5), (4, 5), (6, 5),
            (1, 6), (3, 6), (5, 6), (7, 6),
            (0, 7), (2, 7), (4, 7), (6, 7),
        ]
        size_pos = 80
        radio = size_pos // 2

        for x, y in piezas_blancas:
            x1 = x * size_pos + (size_pos - radio) // 2
            y1 = y * size_pos + (size_pos - radio) // 2

            x2 = x1 + radio
            y2 = y1 + radio
            pieza = self.tablero.create_oval(x1, y1, x2, y2, fill="white")
            self.estado_tablero[y][x] = {'tipo': 'ficha', 'color': 'blanca', 'reina': False, 'id': pieza}

        for x, y in piezas_oscuras:
            x1 = x * size_pos + (size_pos - radio) // 2
            y1 = y * size_pos + (size_pos - radio) // 2

            x2 = x1 + radio
            y2 = y1 + radio
            pieza = self.tablero.create_oval(x1, y1, x2, y2, fill="brown")
            self.estado_tablero[y][x] = {'tipo': 'ficha', 'color': 'oscura', 'reina': False, 'id': pieza}

    def clic_pieza(self, event):
        # Coordenadas del clic en relación con el lienzo
        x, y = self.tablero.canvasx(event.x), self.tablero.canvasy(event.y)
        fila = int(y // 80)
        columna = int(x // 80)

        # Verificar si la casilla contiene una ficha
        if self.estado_tablero[fila][columna] and self.estado_tablero[fila][columna]['tipo'] == "ficha" \
                and self.estado_tablero[fila][columna]['color']:
            # Si hay una casilla seleccionada previamente, limpiar la selección
            if self.casilla_seleccionada:
                fila_anterior, columna_anterior = self.casilla_seleccionada
                id_casilla_anterior = self.obtener_id_casilla(fila_anterior, columna_anterior)
                color_original = "black" if (fila_anterior + columna_anterior) % 2 == 0 else "gray"
                self.tablero.itemconfig(id_casilla_anterior, fill=color_original)
                self.limpiar_resaltado()

            # Resaltar las casillas adyacentes a las esquinas de la ficha
            self.resaltar_movimientos(fila, columna)

            # Verificar si hay fichas enemigas adyacentes y resaltarlas
            self.resaltar_fichas_enemigas(fila, columna)

            # Actualizar la casilla seleccionada
            self.casilla_seleccionada = (fila, columna)

        elif self.casilla_seleccionada:
            # Mover la ficha si se ha seleccionado una casilla adyacente
            fila_origen, columna_origen = self.casilla_seleccionada
            if (fila, columna) in self.obtener_casillas_adyacentes(columna_origen, fila_origen):
                if (fila, columna) in self.casillas_resaltadas:
                    # Si se hace clic en una casilla adyacente resaltada en rojo (ficha enemiga), eliminar la ficha
                    self.eliminar_ficha_enemiga(fila, columna)
                else:
                    # Si se hace clic en una casilla adyacente normalmente, realizar el movimiento
                    self.realizar_movimiento(fila_origen, columna_origen, fila, columna)

                # Limpiar la casilla seleccionada después de realizar la acción
                self.casilla_seleccionada = None

    
    def resaltar_movimientos(self, fila, columna):
        print("Resaltando movimientos")
        # Limpiar el resaltado de movimientos anterior
        self.limpiar_resaltado()

        # Obtener información de la ficha seleccionada
        ficha = self.estado_tablero[fila][columna]
        color_ficha = ficha['color']
        es_reina = ficha['reina']

        # Definir las direcciones de movimiento permitidas para la ficha
        direcciones = [(1, 1), (-1, 1)] if color_ficha == 'blanca' else [(1, -1), (-1, -1)]
        if es_reina:
            direcciones.extend([(1, -1), (-1, -1), (1, 1), (-1, 1)])

        # Resaltar las casillas adyacentes a las esquinas de la ficha
        for dx, dy in direcciones:
            x = columna + dx
            y = fila + dy
            if 0 <= x < 8 and 0 <= y < 8 and not self.estado_tablero[y][x]:
                id_casilla = self.obtener_id_casilla(y, x)
                self.tablero.itemconfig(id_casilla, fill="green")
                self.casillas_resaltadas.append(id_casilla)  # Almacena los identificadores de las casillas





    def realizar_movimiento(self, fila_origen, columna_origen, fila_destino, columna_destino):
        print("Realizando movimiento...")
        
        # Obtener la información de la ficha que se va a mover
        ficha = self.estado_tablero[fila_origen][columna_origen]
        id_ficha = ficha['id']

        # Calcular el cambio en la posición X e Y
        dx = (columna_destino - columna_origen) * 80
        dy = (fila_destino - fila_origen) * 80
        print("Cambio en posición X:", dx)
        print("Cambio en posición Y:", dy)

        # Verificar si la casilla de destino está resaltada en rojo
        if (fila_destino, columna_destino) in self.casillas_resaltadas:
            # Verificar si hay una ficha enemiga en la casilla de destino
            if self.estado_tablero[fila_destino][columna_destino]:
                # Si hay una ficha enemiga, eliminarla del tablero
                self.eliminar_ficha_enemiga(fila_destino, columna_destino)

        # Mover la ficha al centro de la casilla de destino
        self.tablero.move(id_ficha, dx, dy)

        # Actualizar el estado del tablero
        self.estado_tablero[fila_destino][columna_destino] = ficha
        self.estado_tablero[fila_origen][columna_origen] = None

        # Limpiar el resaltado de movimientos
        self.limpiar_resaltado()

        # Limpiar la casilla seleccionada después de realizar el movimiento
        self.casilla_seleccionada = None

        # Actualizar la interfaz gráfica
        self.tablero.update()

        # Verificar si la ficha se movió en diagonal y hay una ficha enemiga entre origen y destino
        if abs(columna_destino - columna_origen) == 1 and abs(fila_destino - fila_origen) == 1:
            # Obtener la posición de la ficha enemiga
            fila_enemiga = (fila_destino + fila_origen) // 2
            columna_enemiga = (columna_destino + columna_origen) // 2
            # Eliminar la ficha enemiga
            self.eliminar_ficha_enemiga(fila_enemiga, columna_enemiga)



    def resaltar_fichas_enemigas(self, fila, columna):
        # Obtener información de la ficha seleccionada
        ficha = self.estado_tablero[fila][columna]
        color_ficha = ficha['color']
        es_reina = ficha['reina']

        # Definir las direcciones de movimiento permitidas para la ficha
        direcciones = [(1, 1), (-1, 1)] if color_ficha == 'blanca' else [(1, -1), (-1, -1)]
        if es_reina:
            direcciones.extend([(1, -1), (-1, -1), (1, 1), (-1, 1)])

        # Resaltar las casillas adyacentes a las esquinas de la ficha
        for dx, dy in direcciones:
            x = columna + dx
            y = fila + dy
            if 0 <= x < 8 and 0 <= y < 8 and self.estado_tablero[y][x]:
                if self.estado_tablero[y][x]['color'] != color_ficha:
                    print("Casilla adyacente contiene una ficha enemiga en fila:", y, "columna:", x)
                    # Casilla adyacente contiene una ficha enemiga, verificar si la siguiente casilla está vacía
                    x_next = x + dx
                    y_next = y + dy
                    if 0 <= x_next < 8 and 0 <= y_next < 8 and not self.estado_tablero[y_next][x_next]:
                        id_casilla = self.obtener_id_casilla(y_next, x_next)
                        print("Resaltando casilla adyacente vacía en fila:", y_next, "columna:", x_next)
                        self.tablero.itemconfig(id_casilla, fill="red")
                        self.casillas_resaltadas.append((y_next, x_next))  # Almacena las coordenadas de las casillas

                        
    def eliminar_ficha_enemiga(self, fila, columna):
        print("Eliminando ficha enemiga en fila:", fila, "columna:", columna)
        # Obtener la información de la ficha enemiga en la posición especificada
        ficha = self.estado_tablero[fila][columna]
        if ficha and ficha['tipo'] == 'ficha':
            print("Ficha enemiga encontrada en fila:", fila, "columna:", columna)
            # Obtener el ID de la ficha enemiga
            id_ficha = ficha['id']

            # Eliminar la ficha enemiga del tablero
            self.tablero.delete(id_ficha)

            # Actualizar el estado del tablero
            self.estado_tablero[fila][columna] = None
            
            
    def limpiar_resaltado(self):
        # Limpiar el resaltado de movimientos
        for id_casilla in self.casillas_resaltadas:
            # Verificar si el ID de la casilla es válido
            if self.tablero.type(id_casilla) == "rectangle":
                # Obtener el color original de la casilla
                color_original = "black" if 'black' in self.tablero.itemcget(id_casilla, 'fill') else "gray"
                # Imprimir el ID de la casilla
                print("ID de casilla:", id_casilla)
                # Restaurar el color original de la casilla
                self.tablero.itemconfig(id_casilla, fill=color_original)
        # Limpiar la lista de casillas resaltadas
        self.casillas_resaltadas.clear()

    def obtener_id_casilla(self, fila, columna):
        # Itera sobre todos los elementos en el lienzo y encuentra el ID de la casilla en la posición dada
        for item in self.tablero.find_all():
            # Obtiene las etiquetas asociadas a cada casilla
            tags = self.tablero.gettags(item)
            # Si las etiquetas incluyen la fila y columna, devuelve el ID del elemento
            if 'casilla_{}_{}'.format(fila, columna) in tags:
                return item

    def obtener_casillas_adyacentes(self, columna, fila):
        # Retorna las coordenadas de las casillas adyacentes a la posición dada
        adyacentes = []
        # Direcciones permitidas para moverse
        direcciones = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dx, dy in direcciones:
            x = columna + dx
            y = fila + dy
            if 0 <= x < 8 and 0 <= y < 8 and not self.estado_tablero[y][x]:
                adyacentes.append((y, x))
        return adyacentes


# Métodos Loop
if __name__ == "__main__":
    app = Tablero()
    app.mainloop()