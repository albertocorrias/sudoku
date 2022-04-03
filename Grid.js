
import Cell from "./Cell.js"


export default class Grid {
    #cells
    #onerow
    #onecolumn
    #onequadrant

    constructor(gridElement) {
        gridElement.style.setProperty("--grid-size", Globals.GRID_SIZE)
        gridElement.style.setProperty("--cell-size", `${Globals.CELL_SIZE}vmin`)
        gridElement.style.setProperty("--board-border", `${Globals.BOARD_BORDER_WIDTH}vmin`)
        
        /*Create the cells*/
        this.#cells = createCellElements(gridElement).map((cellElement, index) => {
            return new Cell(cellElement, 
                index % Globals.GRID_SIZE, 
                Math.floor(index / Globals.GRID_SIZE))
        })
    }

    get cells() {
        return this.#cells;
    }

    getIndicesOnSameRow(idx) {
        let ret = [Globals.GRID_SIZE]
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
        let ret = [Globals.GRID_SIZE]
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
        let ret = [Globals.GRID_SIZE]
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
                    elem_to_clear.style.setProperty("--cell-background-colour", Globals.NORMAL_CELL_COLOR)
                }
                //highlight same row, same column and same quadrant
                for (let k = 0; k < on_same_row.length; k++){
                    let elem_same_row = all_cells[on_same_row[k]].cellElement
                    let elem_same_col = all_cells[on_same_column[k]].cellElement
                    let elem_same_quad = all_cells[on_same_quadrant[k]].cellElement
                    
                    elem_same_row.style.setProperty("--cell-background-colour", Globals.HIGHLIGHTED_CELL_COLOR)
                    elem_same_col.style.setProperty("--cell-background-colour", Globals.HIGHLIGHTED_CELL_COLOR)
                    elem_same_quad.style.setProperty("--cell-background-colour", Globals.HIGHLIGHTED_CELL_COLOR)
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

function createCellElements(gridElement) {
    const cells = []
    for (let i = 0; i < Globals.GRID_SIZE * Globals.GRID_SIZE; i++){
        var cell = document.createElement("div")
        cell.setAttribute('id', `divcell-${i}`);
        cell.classList.add("cell")
        cells.push(cell)
        gridElement.append(cell)
    }
    return cells
}


