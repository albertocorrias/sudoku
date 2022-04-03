
const GRID_SIZE = 9
const CELL_SIZE = 8
const BOARD_BORDER_WIDTH = 0.9


const HIGHLIGHTED_CELL_COLOR = "#fbd7d0"
const NORMAL_CELL_COLOR = "#F0FFFF"
const NORMAL_CELL_BORDER = "thin dotted black"
const QUADRANT_CELL_BORDER = "medium solid black"

export default class Grid {
    #cells
    #onerow
    #onecolumn
    #onequadrant

    constructor(gridElement) {
        gridElement.style.setProperty("--grid-size", GRID_SIZE)
        gridElement.style.setProperty("--cell-size", `${CELL_SIZE}vmin`)
        gridElement.style.setProperty("--board-border", `${BOARD_BORDER_WIDTH}vmin`)
        
        /*Create the cells*/
        this.#cells = createCellElements(gridElement).map((cellElement, index) => {
            return new Cell(cellElement, 
                index % GRID_SIZE, 
                Math.floor(index / GRID_SIZE))
        })
    }

    get cells() {
        return this.#cells;
    }

    getIndicesOnSameRow(idx) {
        let ret = [GRID_SIZE]
        let y_ref = this.#cells[idx].y
        let counter = 0
        for (let i = 0; i < this.#cells.length; i++) {
            if (this.#cells[i].y == y_ref) {
                ret[counter] = i
                counter = counter +1
            }
        }
        return ret;
    }

    getIndicesOnSameColumn(idx) {
        let ret = [GRID_SIZE]
        let x_ref = this.#cells[idx].x
        let counter = 0
        for (let i = 0; i < this.#cells.length; i++) {
            if (this.#cells[i].x == x_ref) {
                ret[counter] = i
                counter = counter +1
            }
        }
        return ret;
    }

    getIndicesOnSameQuadrant(idx) {
        let ret = [GRID_SIZE]
        let quad_ref = this.#cells[idx].quadrant
        let counter = 0
        for (let i = 0; i < this.#cells.length; i++) {
            if (this.#cells[i].quadrant == quad_ref) {
                ret[counter] = i
                counter = counter +1
            }
        }
        return ret;
    }

    setUpEventListeners() {
        const cells_collection = document.getElementsByClassName("cell");
        let all_cells = this.#cells
        for (let i = 0; i < cells_collection.length; i++) {
            //this.#cells[i].value = this.#cells[i].quadrant //Debug line -REMOVE later
           
            let on_same_row = this.getIndicesOnSameRow(i)
            let on_same_column = this.getIndicesOnSameColumn(i)
            let on_same_quadrant = this.getIndicesOnSameQuadrant(i)
            cells_collection[i].addEventListener("click", function() {
                //clear any previous highlighting
                for (let j = 0; j < cells_collection.length; j++) {
                    let elem_to_clear = all_cells[j].cellElement
                    elem_to_clear.style.setProperty("--cell-background-colour", NORMAL_CELL_COLOR)
                }
                //highlight same row, same column and same quadrant
                for (let k = 0; k < on_same_row.length; k++){
                    let elem_same_row = all_cells[on_same_row[k]].cellElement
                    let elem_same_col = all_cells[on_same_column[k]].cellElement
                    let elem_same_quad = all_cells[on_same_quadrant[k]].cellElement
                    
                    elem_same_row.style.setProperty("--cell-background-colour", HIGHLIGHTED_CELL_COLOR)
                    elem_same_col.style.setProperty("--cell-background-colour", HIGHLIGHTED_CELL_COLOR)
                    elem_same_quad.style.setProperty("--cell-background-colour", HIGHLIGHTED_CELL_COLOR)
                }
            })

            //For each cell, create its input field
            var cell_input = document.createElement("input")
            cell_input.type = "number"
            cell_input.name = `${i}-inputcell`
            cell_input.classList.add("cell_inputs")
            cells_collection[i].appendChild(cell_input)
            document.getElementById(`divcell-${i}`).appendChild(cell_input)

            cell_input.addEventListener('keydown', (e) => {
                //console.log(e.code) //DEBUG LINE.
                //restrict to digit only
                if ((e.code.includes("Numpad") == true || e.code.includes("Digit") == true) == false) {
                    e.preventDefault();
                    return false;//do no more
                }
                var this_cell = document.getElementsByName(`${i}-inputcell`)
                this_cell[0].value = '';//clear previous values
                all_cells[i].value=e.key;//record new value
            });
        }
    }
} //end of Grid class


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
        cellElement.style.setProperty("--cell-background-colour",NORMAL_CELL_COLOR)
        cellElement.style.setProperty("--cell-border-bottom",NORMAL_CELL_BORDER)
        cellElement.style.setProperty("--cell-border-top",NORMAL_CELL_BORDER)
        cellElement.style.setProperty("--cell-border-left",NORMAL_CELL_BORDER)
        cellElement.style.setProperty("--cell-border-right",NORMAL_CELL_BORDER)
        if (this.#y == 2 || this.#y == 5){
            cellElement.style.setProperty("--cell-border-bottom",QUADRANT_CELL_BORDER)
        }
        if (this.#x == 2 || this.#x == 5){
            cellElement.style.setProperty("--cell-border-right",QUADRANT_CELL_BORDER)
        }
        if (this.#y == 3 || this.#y == 6){
            cellElement.style.setProperty("--cell-border-top",QUADRANT_CELL_BORDER)
        }
        if (this.#x == 3 || this.#x == 6){
            cellElement.style.setProperty("--cell-border-left",QUADRANT_CELL_BORDER)
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
        //this.cellElement.textContent = v
    }
}
function createCellElements(gridElement) {
    const cells = []
    for (let i = 0; i < GRID_SIZE * GRID_SIZE; i++){
        var cell = document.createElement("div")
        cell.setAttribute('id', `divcell-${i}`);
        cell.classList.add("cell")
        cells.push(cell)
        gridElement.append(cell)
    }
    return cells
}


