import Cell from "./Cell.js"


export default class Grid {
    #cells

    constructor(gridElement) {
        gridElement.style.setProperty("--grid-size", Globals.GRID_SIZE)
        gridElement.style.setProperty("--cell-size", `${Globals.CELL_SIZE}vmin`)
        
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

    getIndexOfCellAbove(cell_index) {
        var cell_above = -1
        let all_cells = this.#cells
        const target_x = all_cells[cell_index].x
        const target_y = all_cells[cell_index].y - 1
        if(target_y > -1){
            cell_above = target_x+(target_y)*Globals.GRID_SIZE
        }
        return cell_above
    }

    getIndexOfCellAtRight(cell_index) {
        var cell_right = -1
        let all_cells = this.#cells
        const target_x = all_cells[cell_index].x + 1
        const target_y = all_cells[cell_index].y 
        if(target_x < 9){
            cell_right = target_x+(target_y)*Globals.GRID_SIZE
        }
        return cell_right
    }

    getIndexOfCellAtLeft(cell_index) {
        var cell_left = -1
        let all_cells = this.#cells
        const target_x = all_cells[cell_index].x - 1
        const target_y = all_cells[cell_index].y 
        if(target_x > -1){
            cell_left = target_x+(target_y)*Globals.GRID_SIZE
        }
        return cell_left
    }

    getIndexOfCellBelow(cell_index) {
        var cell_below = -1
        let all_cells = this.#cells
        const target_x = all_cells[cell_index].x 
        const target_y = all_cells[cell_index].y + 1 
        if(target_y < 9){
            cell_below = target_x+(target_y)*Globals.GRID_SIZE
        }
        return cell_below
    }

    clearAllHighlighting() {
        let all_cells = this.#cells
        const cells_collection = document.getElementsByClassName("cell");
        //clear any previous highlighting
        for (let j = 0; j < all_cells.length; j++) {
            let elem_to_clear = all_cells[j].cellElement
            elem_to_clear.style.setProperty("--cell-background-colour", Globals.NORMAL_CELL_COLOR)
            //clear the clicked flag as well
            all_cells[j].isClicked = false
        }
    }


    highlightCell(cell_index){
        let all_cells = this.#cells
        let elem_clicked = all_cells[cell_index].cellElement
        elem_clicked.style.setProperty("--cell-background-colour", Globals.HIGHLIGHTED_CELL_COLOR)
        //set as clicked
        all_cells[cell_index].isClicked = true
    }

    clearCellValue(cell_index){
        let all_cells = this.#cells
        all_cells[cell_index].value = undefined //back to undefined value
        //restore size and colour, in case it was a provisional
        all_cells[cell_index].isProvisional = false;
        //reset the multline flag
        all_cells[cell_index].isMultiLine = false;
        all_cells[cell_index].cellElement.style.setProperty("--text-size", "100%")
        all_cells[cell_index].cellElement.style.setProperty("--number-color",Globals.NUMBER_COLOR_OF_USER_NUMBERS)
    }
        
    
    highlightRelatedCells(cell_index){
        let all_cells = this.#cells
        let on_same_row = this.getIndicesOnSameRow(cell_index)
        let on_same_column = this.getIndicesOnSameColumn(cell_index)
        let on_same_quadrant = this.getIndicesOnSameQuadrant(cell_index)
        for (let k = 0; k < on_same_row.length; k++){
            let elem_same_row = all_cells[on_same_row[k]].cellElement
            let elem_same_col = all_cells[on_same_column[k]].cellElement
            let elem_same_quad = all_cells[on_same_quadrant[k]].cellElement
                        
            elem_same_row.style.setProperty("--cell-background-colour", Globals.HIGHLIGHTED_RELATED_CELL_COLOR)
            elem_same_col.style.setProperty("--cell-background-colour", Globals.HIGHLIGHTED_RELATED_CELL_COLOR)
            elem_same_quad.style.setProperty("--cell-background-colour", Globals.HIGHLIGHTED_RELATED_CELL_COLOR)
        }
    }

    highlightEqualValues(cell_index){
        let all_cells = this.#cells
        //highlight equal values elsewhere
        for (let j = 0; j < all_cells.length; j++) {
            if (all_cells[j].value==all_cells[cell_index].value && typeof all_cells[j].value != 'undefined') {
                let elem_to_highlight = all_cells[j].cellElement
                elem_to_highlight.style.setProperty("--cell-background-colour", Globals.HIGHLIGHTED_CELL_COLOR_SAME_NUMBER)
            }
        }
    }

    insertDigitIntoCell(cell_index,value_to_insert){
        let all_cells = this.#cells
        if (all_cells[cell_index].isProvisional == false) {
            all_cells[cell_index].value = value_to_insert;//record new values
        } else {//it is provisional
            var existing = all_cells[cell_index].value
            if (existing == undefined) {//nothing in there
                all_cells[cell_index].value = value_to_insert;//record new values
            } else {//provisional cell with other values in it already
                console.log(existing)
                const existing_numbers = existing.toString().split(Globals.SEPARATING_CHARACTER_FOR_PROVISIONAL_NUMBERS)
                if (existing_numbers.includes(value_to_insert) == false) {//we do nothing if it is already there
                    const how_many = existing_numbers.length
                    if (how_many > 1) {
                        all_cells[cell_index].cellElement.style.setProperty("--text-size", "23%")
                    }
                    if (how_many > 3 && all_cells[cell_index].isMultiLine == false) {
                        existing = existing + "\n"
                        all_cells[cell_index].isMultiLine = true
                    }
                    all_cells[cell_index].value = existing.toString().concat(Globals.SEPARATING_CHARACTER_FOR_PROVISIONAL_NUMBERS, value_to_insert);//concatenate new values
                }
            }
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


