
export default class Cell {
    
    #x /* x coordinate in the grid*/
    #y /* y coordinate in the grid*/

    #quadrant /*The sudoku quadrant this cell is in*/
    #value /*The value of this cell*/

    constructor(cellElement, x, y){
        this.cellElement = cellElement
        this.#x = x
        this.#y = y
        let quad_x = Math.floor(this.#y / (Globals.GRID_SIZE/3))
        let quad_y = Math.floor(this.#x / (Globals.GRID_SIZE/3))
        this.#quadrant =  quad_y + (Globals.GRID_SIZE/3)*quad_x
        cellElement.style.setProperty("--cell-background-colour",Globals.NORMAL_CELL_COLOR)
        cellElement.style.setProperty("--cell-border-bottom",Globals.NORMAL_CELL_BORDER)
        cellElement.style.setProperty("--cell-border-top",Globals.NORMAL_CELL_BORDER)
        cellElement.style.setProperty("--cell-border-left",Globals.NORMAL_CELL_BORDER)
        cellElement.style.setProperty("--cell-border-right",Globals.NORMAL_CELL_BORDER)
        if (this.#y == 2 || this.#y == 5){
            cellElement.style.setProperty("--cell-border-bottom",Globals.QUADRANT_CELL_BORDER)
        }
        if (this.#x == 2 || this.#x == 5){
            cellElement.style.setProperty("--cell-border-right",Globals.QUADRANT_CELL_BORDER)
        }
        if (this.#y == 3 || this.#y == 6){
            cellElement.style.setProperty("--cell-border-top",Globals.QUADRANT_CELL_BORDER)
        }
        if (this.#x == 3 || this.#x == 6){
            cellElement.style.setProperty("--cell-border-left",Globals.QUADRANT_CELL_BORDER)
        }  
    }
    get x(){
        return this.#x;
    }
    get y(){
        return this.#y
    }
    get quadrant() {
        return this.#quadrant
    }

    get value() {
        return this.#value
    }

    set value(v){
        this.#value = v
        this.cellElement.textContent = v //useful for debugging game logic
    }
}