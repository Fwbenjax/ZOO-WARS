class BaseGrafica:
    def __init__(self, x, y, e):
        self.x, self.y, self.e = x, y, e
        self.color, self.alfa = (255, 255, 255), 0
        
    def setColor(self, color): self.color = color
    def setX(self, x): self.x = x
    def setY(self, y): self.y = y
    def setXY(self, x, y): self.x, self.y = x, y
    def setEscala(self, e): self.e = e
    def getX(self): return self.x
    def getY(self): return self.y
    def getEscala(self): return self.e
    def getColor(self): return self.color

class BaseLogica(BaseGrafica):
    def __init__(self, fila, columna, e):
        super().__init__(columna * e, fila * e, e)
        self.fila, self.columna = fila, columna
        
    def sincronizar_coordenadas(self): 
        self.setXY(self.columna * self.e, self.fila * self.e)
        
    def moverArriba(self): 
        self.fila -= 1; self.sincronizar_coordenadas()
        
    def moverAbajo(self): 
        self.fila += 1; self.sincronizar_coordenadas()
        
    def moverIzquierda(self): 
        self.columna -= 1; self.sincronizar_coordenadas()
        
    def moverDerecha(self): 
        self.columna += 1; self.sincronizar_coordenadas()
        
    def setFila(self, fila): 
        self.fila = fila; self.sincronizar_coordenadas()
        
    def setColumna(self, columna): 
        self.columna = columna; self.sincronizar_coordenadas()
        
    def getFila(self): return self.fila
    def getColumna(self): return self.columna