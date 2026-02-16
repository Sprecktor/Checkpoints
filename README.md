# Sudoku con Checkpoints

Pequeña aplicación de Sudoku con interfaz gráfica en Tkinter y soporte de "checkpoints" (guardado automático del progreso) mediante `pickle`.

**Características**
- Generador simple de tableros Sudoku 9x9.
- Interfaz gráfica con `tkinter` para introducir números.
- Sistema de vidas (3 vidas) que decrementa al introducir un número incorrecto.
- Guardado automático de checkpoint en `sudoku_checkpoint.pkl` cada vez que se hace una jugada (exitosa o no).
- Recuperación automática de la partida desde el checkpoint al arrancar la aplicación.

**Requisitos**
- Python 3.8+ (probado con Python 3.x)
- Biblioteca estándar: `tkinter`, `pickle`, `random`, `os` (no se requieren paquetes externos)

**Instalación y ejecución**
1. Asegúrate de tener Python instalado.
2. Desde la carpeta del proyecto ejecuta:

```bash
python sudoku.py
```

En Windows puedes ejecutar directamente el script haciendo doble clic si tu sistema está configurado para ejecutar archivos `.py` con Python.

**Cómo funciona**
- Al iniciar, la aplicación busca `sudoku_checkpoint.pkl`. Si existe, intenta cargar la partida guardada (tablero, solución y vidas).
- Si no existe checkpoint o la carga falla, se genera un nuevo tablero y se crea el checkpoint inicial.
- Cada entrada válida se compara con la solución; si es correcta, el número queda bloqueado y se guarda un checkpoint.
- Si la entrada es incorrecta, se resta una vida, se guarda un checkpoint y se borra la entrada. Al perder todas las vidas, la partida se reinicia.

**Personalización rápida**
- Dificultad: la función `generate_sudoku()` elimina actualmente 40 números para crear el reto. Ajusta el número `for _ in range(40):` para cambiar la dificultad.
