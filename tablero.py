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

        # Si hay una casilla seleccionada previamente, limpiar la selección
        if self.casilla_seleccionada:
            fila_anterior, columna_anterior = self.casilla_seleccionada
            id_casilla_anterior = self.obtener_id_casilla(fila_anterior, columna_anterior)
            color_original = "black" if (fila_anterior + columna_anterior) % 2 == 0 else "gray"
            self.tablero.itemconfig(id_casilla_anterior, fill=color_original)
            if (fila_anterior, columna_anterior) != (fila, columna):
                self.limpiar_resaltado()
            self.casilla_seleccionada = None

        # Verificar si hay una ficha en la casilla seleccionada
        if self.estado_tablero[fila][columna] and self.estado_tablero[fila][columna]['tipo'] == "ficha":
            # Resaltar las casillas adyacentes a las esquinas de la ficha
            self.resaltar_movimientos(fila, columna)
            # Actualizar la casilla seleccionada
            self.casilla_seleccionada = (fila, columna)

    def resaltar_movimientos(self, fila, columna):
        # Obtener información de la ficha seleccionada
        ficha = self.estado_tablero[fila][columna]
        color_ficha = ficha['color']
        es_reina = ficha['reina']

        # Definir las direcciones de movimiento permitidas para la ficha
        direcciones = [(1, 1), (-1, 1)] if color_ficha == 'blanca' else [(1, -1), (-1, -1)]
        if es_reina:
            direcciones.extend([(1, -1), (-1, -1), (1, 1), (-1, 1)])

        # Limpiar el resaltado de movimientos anterior
        self.limpiar_resaltado()

        # Resaltar las casillas adyacentes a las esquinas de la ficha
        for dx, dy in direcciones:
            x = columna + dx
            y = fila + dy
            if 0 <= x < 8 and 0 <= y < 8 and not self.estado_tablero[y][x]:
                id_casilla = self.obtener_id_casilla(y, x)
                self.tablero.itemconfig(id_casilla, fill="green")
                self.casillas_resaltadas.append(id_casilla)

    def limpiar_resaltado(self):
        # Limpiar el resaltado de movimientos
        for id_casilla in self.casillas_resaltadas:
            color_original = "black" if '0' in self.tablero.itemcget(id_casilla, 'fill') else "gray"
            self.tablero.itemconfig(id_casilla, fill=color_original)
        self.casillas_resaltadas.clear()

    def obtener_id_casilla(self, fila, columna):
        # Itera sobre todos los elementos en el lienzo y encuentra el ID de la casilla en la posición dada
        for item in self.tablero.find_all():
            # Obtiene las etiquetas asociadas a cada casilla
            tags = self.tablero.gettags(item)
            # Si las etiquetas incluyen la fila y columna, devuelve el ID del elemento
            if 'casilla_{}_{}'.format(fila, columna) in tags:
                return item


# Métodos Loop
if __name__ == "__main__":
    app = Tablero()
    app.mainloop()
