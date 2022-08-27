

export default class Cell {
    
    #x /* x coordinate in the grid*/
    #y /* y coordinate in the grid*/

    #quadrant /*The sudoku quadrant this cell is in*/
    #value /*The value of this cell*/
    #isHint/*Whether or not this cell is a hint*/
    #isClicked/*Whether or not this cell is "active" or clikced*/
    #isProvisional/*Whether or not the user is inputting provisional numbers in this cell*/
    #isMultiLine /*whether or not we had to insert a newline character because of too many provisional numbers*/
    constructor(cellElement, x, y){
        this.cellElement = cellElement
        this.#x = x
        this.#y = y
        this.#isHint = false
        this.#isClicked = false
        this.#isProvisional = false
        this.#isMultiLine = false
        let quad_x = Math.floor(this.#y / (Globals.GRID_SIZE/3))
        let quad_y = Math.floor(this.#x / (Globals.GRID_SIZE/3))
        this.#quadrant =  quad_y + (Globals.GRID_SIZE/3)*quad_x
        
        cellElement.style.setProperty("--cell-background-colour",Globals.NORMAL_CELL_COLOR)
        cellElement.style.setProperty("--cell-border-color",Globals.CELL_BORDER_COLOR)

        cellElement.style.setProperty("--cell-border-style-bottom",Globals.NORMAL_CELL_BORDER_STYLE)
        cellElement.style.setProperty("--cell-border-style-top",Globals.NORMAL_CELL_BORDER_STYLE)
        cellElement.style.setProperty("--cell-border-style-left",Globals.NORMAL_CELL_BORDER_STYLE)
        cellElement.style.setProperty("--cell-border-style-right",Globals.NORMAL_CELL_BORDER_STYLE)

        cellElement.style.setProperty("--cell-border-width-bottom",Globals.NORMAL_CELL_BORDER_WIDTH)
        cellElement.style.setProperty("--cell-border-width-top",Globals.NORMAL_CELL_BORDER_WIDTH)
        cellElement.style.setProperty("--cell-border-width-left",Globals.NORMAL_CELL_BORDER_WIDTH)
        cellElement.style.setProperty("--cell-border-width-right",Globals.NORMAL_CELL_BORDER_WIDTH)

        if (this.#y == 8){
            cellElement.style.setProperty("--cell-border-style-bottom",Globals.QUADRANT_CELL_BORDER_STYLE)
            cellElement.style.setProperty("--cell-border-width-bottom",Globals.BOARD_BORDER_WIDTH)
        }
        if (this.#y == 2 || this.#y == 5){
            cellElement.style.setProperty("--cell-border-style-bottom",Globals.QUADRANT_CELL_BORDER_STYLE)
            cellElement.style.setProperty("--cell-border-width-bottom",Globals.QUADRANT_CELL_BORDER_WIDTH)
        }
        if (this.#x == 8){
            cellElement.style.setProperty("--cell-border-style-right",Globals.QUADRANT_CELL_BORDER_STYLE)
            cellElement.style.setProperty("--cell-border-width-right",Globals.BOARD_BORDER_WIDTH)
        }
        if (this.#x == 2 || this.#x == 5){
            cellElement.style.setProperty("--cell-border-style-right",Globals.QUADRANT_CELL_BORDER_STYLE)
            cellElement.style.setProperty("--cell-border-width-right",Globals.QUADRANT_CELL_BORDER_WIDTH)
        }
        if (this.#y == 0){
            cellElement.style.setProperty("--cell-border-style-top",Globals.QUADRANT_CELL_BORDER_STYLE)
            cellElement.style.setProperty("--cell-border-width-top",Globals.BOARD_BORDER_WIDTH)
        }
        if (this.#y == 3 || this.#y == 6){
            cellElement.style.setProperty("--cell-border-style-top",Globals.QUADRANT_CELL_BORDER_STYLE)
            cellElement.style.setProperty("--cell-border-width-top",Globals.QUADRANT_CELL_BORDER_WIDTH)
        }
        if (this.#x == 0){
            cellElement.style.setProperty("--cell-border-style-left",Globals.QUADRANT_CELL_BORDER_STYLE)
            cellElement.style.setProperty("--cell-border-width-left",Globals.BOARD_BORDER_WIDTH)
        }  
        if (this.#x == 3 || this.#x == 6){
            cellElement.style.setProperty("--cell-border-style-left",Globals.QUADRANT_CELL_BORDER_STYLE)
            cellElement.style.setProperty("--cell-border-width-left",Globals.QUADRANT_CELL_BORDER_WIDTH)
        }  

        //set default text color as the color user input. The grid will override for the hints
        cellElement.style.setProperty("--number-color",Globals.NUMBER_COLOR_OF_USER_NUMBERS)
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
    get isHint() {
        return this.#isHint;
    }
    get value() {
        return this.#value
    }

    get isClicked() {
        return this.#isClicked
    }

    get isProvisional() {
        return this.#isProvisional
    }

    get isMultiLine() {
        return this.#isMultiLine
    }

    set value(v){
        this.#value = v
        this.cellElement.textContent = v //useful for debugging game logic
    }

    set isHint(flag) {
        this.#isHint = flag
    }

    set isClicked(flag) {
        this.#isClicked = flag
    }

    set isProvisional(flag) {
        this.#isProvisional = flag
    }

    set isMultiLine(flag) {
        this.#isMultiLine = flag
    }
}