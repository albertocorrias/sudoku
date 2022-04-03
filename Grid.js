
const GRID_SIZE = 9
const CELL_SIZE = 8
const CELL_GAP = 0.2
const CORNER_RADIUS = 0.2

const HIGHLIGHTED_CELL_COLOR = "#fbd7d0"
const NORMAL_CELL_COLOR = "#aaa"
export default class Grid {
    #cells
    #onerow
    #onecolumn
    #onequadrant

    constructor(gridElement) {
        gridElement.style.setProperty("--grid-size", GRID_SIZE)
        gridElement.style.setProperty("--cell-size", `${CELL_SIZE}vmin`)
        gridElement.style.setProperty("--cell-gap", `${CELL_GAP}vmin`)
        gridElement.style.setProperty("--cell-corner-radius", `${CORNER_RADIUS}vmin`)
        gridElement.style.setProperty("--cell-background-colour",NORMAL_CELL_COLOR)
        /*Create the cells*/
        this.#cells = createCellElements(gridElement).map((cellElement, index) => {
            return new Cell(cellElement, 
                index % GRID_SIZE, 
                Math.floor(index / GRID_SIZE))
        })

        this.#onerow = [GRID_SIZE]
        this.#onecolumn = [GRID_SIZE]
        this.#onequadrant = [GRID_SIZE]
    }

    get cells() {
        return this.#cells;
    }

    getIndicesOnSameRow(idx) {
        let y_ref = this.#cells[idx].y
        let counter = 0
        for (let i = 0; i < this.#cells.length; i++) {
            if (this.#cells[i].y == y_ref) {
                this.#onerow[counter] = i
                counter = counter +1
            }
        }
    }

    getIndicesOnSameColumn(idx) {
        let x_ref = this.#cells[idx].x
        let counter = 0
        for (let i = 0; i < this.#cells.length; i++) {
            if (this.#cells[i].x == x_ref) {
                this.#onecolumn[counter] = i
                counter = counter +1
            }
        }
    }

    getIndicesOnSameQuadrant(idx) {
        let quad_ref = this.#cells[idx].quadrant
        let counter = 0
        for (let i = 0; i < this.#cells.length; i++) {
            if (this.#cells[i].quadrant == quad_ref) {
                this.#onequadrant[counter] = i
                counter = counter +1
            }
        }
    }

    setUpEventListeners() {
        const cells_collection = document.getElementsByClassName("cell");

        for (let i = 0; i < cells_collection.length; i++) {

            let elem = this.#cells[i].cellElement
            this.#cells[i].value = this.#cells[i].quadrant
            this.getIndicesOnSameRow(i)
            this.getIndicesOnSameColumn(i)
            this.getIndicesOnSameQuadrant(i)
            for (let j = 0; j < this.#onerow.length; j++) {
                let idx_row = this.#onerow[j]
                cells_collection[idx_row].addEventListener("mouseover", function() {
                    elem.style.setProperty("--cell-background-colour", HIGHLIGHTED_CELL_COLOR)
                })
                cells_collection[idx_row].addEventListener("mouseout", function() {
                    elem.style.setProperty("--cell-background-colour", NORMAL_CELL_COLOR)
                })
                
                let idx_col = this.#onecolumn[j]
                cells_collection[idx_col].addEventListener("mouseover", function() {
                    elem.style.setProperty("--cell-background-colour", HIGHLIGHTED_CELL_COLOR)
                })
                cells_collection[idx_col].addEventListener("mouseout", function() {
                    elem.style.setProperty("--cell-background-colour", NORMAL_CELL_COLOR)
                })

                let idx_quad = this.#onequadrant[j]
                cells_collection[idx_quad].addEventListener("mouseover", function() {
                    elem.style.setProperty("--cell-background-colour", HIGHLIGHTED_CELL_COLOR)
                })
                cells_collection[idx_quad].addEventListener("mouseout", function() {
                    elem.style.setProperty("--cell-background-colour", NORMAL_CELL_COLOR)
                })
            }

        }

    }


}

class Cell {
    
    #x /* x coordinate in the grid*/
    #y /* y coordinate in the grid*/

    #quadrant /*The sudoku quadrant this cell is in*/
    #value /*The value of this cell*/

    constructor(cellElement, x, y){
        this.cellElement = cellElement
        this.#x = x
        this.#y = y
        let quad_x = Math.floor(this.#y / (GRID_SIZE/3))
        let quad_y = Math.floor(this.#x / (GRID_SIZE/3))
        this.#quadrant =  quad_y + (GRID_SIZE/3)*quad_x
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


    set value(v){
        this.#value = v
        this.cellElement.textContent = v
    }
}
function createCellElements(gridElement) {
    const cells = []
    for (let i = 0; i < GRID_SIZE * GRID_SIZE; i++){
        const cell = document.createElement("div")
        cell.classList.add("cell")
        cells.push(cell)
        gridElement.append(cell)
    }
    return cells
}


