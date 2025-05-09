// bank/static/bank/js/freezer.js

document.addEventListener('DOMContentLoaded', () => {
  const table = document.getElementById('sample-table');
  const rackSchema = document.getElementById('rack-schema');
  const boxSchema = document.getElementById('box-schema');
  const rackSelect = document.getElementById('rack-select');
  const boxSelect = document.getElementById('box-select');
  const rackInfo = document.getElementById('rack-info');
  const boxInfo = document.getElementById('box-info');

  let selectedRack = '';
  let selectedBox = '';

  function clearGrid(container, cols, rows) {
    container.innerHTML = '';
    for (let r = 1; r <= rows; r++) {
      for (let c = 0; c < cols; c++) {
        const cell = document.createElement('div');
        cell.className = 'schema-cell';
        container.appendChild(cell);
      }
    }
  }

  function drawRackSchema(rackId) {
    clearGrid(rackSchema, 4, 4);
    rackInfo.textContent = '';
    if (!rackId) return;

    // Filtrar muestras de este rack
    const rackSamples = samples.filter(s => s.rack === rackId);
    rackInfo.textContent = `Rack: ${rackId}`;

    const map = {};
    rackSamples.forEach(s => {
      const label = s.rackCol + s.rackRow;
      map[label] = s.box;
    });

    rackSchema.querySelectorAll('.schema-cell').forEach((cell, i) => {
      const col = String.fromCharCode(65 + (i % 4));
      const row = 1 + Math.floor(i / 4);
      const key = col + row;
      if (map[key]) cell.textContent = `Caja ${map[key]}`;
    });
  }

  function drawBoxSchema(boxId) {
    clearGrid(boxSchema, 9, 9);
    boxInfo.textContent = '';
    if (!boxId) return;

    const boxSamples = samples.filter(s => s.box === boxId);
    if (boxSamples.length > 0) {
      const { name, strain, description } = boxSamples[0];
      boxInfo.textContent = `Name: ${name}\nStrain: ${strain}\nDescription: ${description}`;
    }

    const map = {};
    boxSamples.forEach(s => {
      const label = s.boxCol + s.boxRow;
      map[label] = s.id;
    });

    boxSchema.querySelectorAll('.schema-cell').forEach((cell, i) => {
      const col = String.fromCharCode(65 + (i % 9));
      const row = 1 + Math.floor(i / 9);
      const key = col + row;
      if (map[key]) cell.textContent = `Muestra Id ${map[key]}`;
    });
  }

  function updateBoxSelect(rackId) {
    boxSelect.innerHTML = '<option value="">-- Selecciona una caja --</option>';
    const boxesInRack = [...new Set(samples.filter(s => s.rack === rackId).map(s => s.box))];
    boxesInRack.forEach(box => {
      const opt = document.createElement('option');
      opt.value = box;
      opt.textContent = box;
      boxSelect.appendChild(opt);
    });
  }

  function applyFilters() {
    const rows = table.tBodies[0].rows;
    for (let row of rows) {
      const rackMatch = !selectedRack || row.dataset.rack === selectedRack;
      const boxMatch = !selectedBox || row.dataset.box === selectedBox;
      row.style.display = (rackMatch && boxMatch) ? '' : 'none';
    }
  }

  rackSelect.addEventListener('change', () => {
    selectedRack = rackSelect.value;
    selectedBox = ''; // reset caja al cambiar rack
    boxSelect.value = '';
    drawRackSchema(selectedRack);
    drawBoxSchema('');
    updateBoxSelect(selectedRack);
    applyFilters();
  });

  boxSelect.addEventListener('change', () => {
    selectedBox = boxSelect.value;
    drawBoxSchema(selectedBox);
    applyFilters();
  });

  // INIT: todo vacío
  clearGrid(rackSchema, 4, 4);
  clearGrid(boxSchema, 9, 9);
});





//document.addEventListener('DOMContentLoaded', function() {
//    const tableElement = document.getElementById('sample-table');
//    const rackSelector = document.getElementById('rack-selector');
//    const boxSelector = document.getElementById('box-selector');
//    const rackSchema = document.getElementById('rack-schema');
//    const boxSchema = document.getElementById('box-schema');
//    const rackInfo = document.getElementById('rack-info');
//    const boxInfo = document.getElementById('box-info');
//    const rackCells = rackSchema.querySelectorAll('.rack-cell');
//    const boxCells = boxSchema.querySelectorAll('.box-cell');
//
//    let currentSelectedRow = null;
//
//    function resetHighlights() {
//        rackCells.forEach(cell => cell.classList.remove('highlight', 'rack-linked'));
//        boxCells.forEach(cell => cell.classList.remove('highlight', 'box-linked'));
//        if (tableElement) {
//            tableElement.querySelectorAll('tbody tr').forEach(row => row.classList.remove('highlight'));
//        }
//    }
//
//    function updateSchemas(row) {
//        resetHighlights();
//        rackInfo.textContent = '';
//        boxInfo.textContent = '';
//        rackSelector.value = '';
//        boxSelector.value = '';
//
//        if (row) {
//            const rack = row.dataset.rack;
//            const rackCol = row.dataset.rackCol;
//            const rackRow = row.dataset.rackRow;
//            const box = row.dataset.box;
//            const boxCol = row.dataset.boxCol;
//            const boxRow = row.dataset.boxRow;
//
//            if (rack) {
//                rackSelector.value = rack;
//                rackInfo.textContent = `Rack: ${rack}`;
//                const rackPos = rackCol + rackRow;
//                const rackCell = rackSchema.querySelector(`.rack-cell[data-rack-pos="${rackPos}"]`);
//                if (rackCell) {
//                    rackCell.classList.add('highlight');
//                    rackInfo.textContent += `, Posición: ${rackPos}`;
//                }
//            }
//
//            if (box) {
//                boxSelector.value = box;
//                boxInfo.textContent = `Caja: ${box}`;
//                const boxPos = boxCol + boxRow;
//                const boxCell = boxSchema.querySelector(`.box-cell[data-box-pos="${boxPos}"]`);
//                if (boxCell) {
//                    boxCell.classList.add('highlight');
//                    boxInfo.textContent += `, Posición: ${boxPos}`;
//                }
//            }
//        }
//    }
//
//    function filterTableBySelector(column, value) {
//        const rows = tableElement.querySelectorAll('tbody tr');
//        resetHighlights();
//        rows.forEach(row => {
//            if (value === '' || row.dataset[column] === value) {
//                row.style.display = '';
//            } else {
//                row.style.display = 'none';
//            }
//        });
//        currentSelectedRow = null;
//        updateSchemas(null);
//    }
//
//    function highlightSchemaByFilter(schema, cellSelector, filterValue, infoElement, linkedSchema, linkedCellSelector, linkedDataAttr) {
//        schema.querySelectorAll(cellSelector).forEach(cell => {
//            cell.classList.remove('highlight', 'rack-linked', 'box-linked');
//            if (cell.dataset.rackPos && filterValue && cell.dataset.rackPos.startsWith(filterValue)) {
//                cell.classList.add('highlight');
//                infoElement.textContent = `Rack: ${filterValue}, Posición: ${cell.dataset.rackPos}`;
//            } else if (cell.dataset.boxPos && filterValue && cell.dataset.boxPos.startsWith(filterValue)) {
//                cell.classList.add('highlight');
//                infoElement.textContent = `Caja: ${filterValue}, Posición: ${cell.dataset.boxPos}`;
//            }
//        });
//
//        // Logic to highlight linked schema based on the filter
//        if (linkedSchema && filterValue) {
//            linkedSchema.querySelectorAll(linkedCellSelector).forEach(linkedCell => {
//                linkedCell.classList.remove('highlight', 'rack-linked', 'box-linked');
//                if (tableElement) {
//                    tableElement.querySelectorAll('tbody tr:not([style*="display: none"])').forEach(visibleRow => {
//                        const linkedValue = visibleRow.dataset[linkedDataAttr];
//                        if (linkedCell.dataset.rackPos && linkedValue === linkedCell.dataset.rackPos.substring(0, 1)) {
//                            linkedCell.classList.add('rack-linked');
//                        } else if (linkedCell.dataset.boxPos && linkedValue === linkedCell.dataset.boxPos.substring(0, 1)) {
//                            linkedCell.classList.add('box-linked');
//                        }
//                    });
//                }
//            });
//        } else if (linkedSchema) {
//            linkedSchema.querySelectorAll(linkedCellSelector).forEach(cell => cell.classList.remove('rack-linked', 'box-linked'));
//        }
//    }
//
//    // Event listener para la selección de una fila en la tabla
//    if (tableElement && tableElement.querySelector('tbody')) {
//        tableElement.querySelector('tbody').addEventListener('click', function(event) {
//            const row = event.target.closest('tr');
//            if (row) {
//                resetHighlights();
//                row.classList.add('highlight');
//                currentSelectedRow = row;
//                updateSchemas(row);
//            }
//        });
//    }
//
//    // Event listeners para los selectores de Rack y Caja
//    if (rackSelector) {
//        rackSelector.addEventListener('change', function() {
//            filterTableBySelector('rack', this.value);
//            highlightSchemaByFilter(rackSchema, '.rack-cell', this.value, rackInfo, boxSchema, '.box-cell', 'box');
//            if (!this.value) rackInfo.textContent = '';
//            if (boxSelector) boxSelector.value = ''; // Reset the other selector
//            if (boxSchema && !boxSelector.value) boxSchema.querySelectorAll('.box-cell').forEach(cell => cell.classList.remove('highlight', 'box-linked'));
//            if (boxInfo) boxInfo.textContent = '';
//        });
//    }
//
//    if (boxSelector) {
//        boxSelector.addEventListener('change', function() {
//            filterTableBySelector('box', this.value);
//            highlightSchemaByFilter(boxSchema, '.box-cell', this.value, boxInfo, rackSchema, '.rack-cell', 'rack');
//            if (!this.value) boxInfo.textContent = '';
//            if (rackSelector) rackSelector.value = ''; // Reset the other selector
//            if (rackSchema && !rackSelector.value) rackSchema.querySelectorAll('.rack-cell').forEach(cell => cell.classList.remove('highlight', 'rack-linked'));
//            if (rackInfo) rackInfo.textContent = '';
//        });
//    }
//
//    // Event listeners para la selección de celdas en los esquemas
//    if (rackSchema) {
//        rackSchema.addEventListener('click', function(event) {
//            const cell = event.target.closest('.rack-cell');
//            if (cell) {
//                const rackValue = cell.dataset.rackPos ? cell.dataset.rackPos.substring(0, 1) : '';
//                if (rackSelector) rackSelector.value = rackValue;
//                filterTableBySelector('rack', rackValue);
//                resetHighlights();
//                cell.classList.add('highlight');
//                if (rackInfo) rackInfo.textContent = `Rack: ${rackValue}, Posición: ${cell.dataset.rackPos}`;
//                if (boxSelector) boxSelector.value = ''; // Reset the other selector
//                if (boxSchema) boxSchema.querySelectorAll('.box-cell').forEach(c => c.classList.remove('highlight', 'box-linked'));
//                if (boxInfo) boxInfo.textContent = '';
//            }
//        });
//    }
//
//    if (boxSchema) {
//        boxSchema.addEventListener('click', function(event) {
//            const cell = event.target.closest('.box-cell');
//            if (cell) {
//                const boxValue = cell.dataset.boxPos ? cell.dataset.boxPos.substring(0, 1) : '';
//                if (boxSelector) boxSelector.value = boxValue;
//                filterTableBySelector('box', boxValue);
//                resetHighlights();
//                cell.classList.add('highlight');
//                if (boxInfo) boxInfo.textContent = `Caja: ${boxValue}, Posición: ${cell.dataset.boxPos}`;
//                if (rackSelector) rackSelector.value = ''; // Reset the other selector
//                if (rackSchema) rackSchema.querySelectorAll('.rack-cell').forEach(c => c.classList.remove('highlight', 'rack-linked'));
//                if (rackInfo) rackInfo.textContent = '';
//            }
//        });
//    }
//});

//document.addEventListener('DOMContentLoaded', () => {
//  const table = document.getElementById('sample-table');
//  const rackSchema = document.getElementById('rack-scheme');
//  const boxSchema = document.getElementById('box-scheme');
//  const rackSelect = document.getElementById('rack-select');
//  const boxSelect = document.getElementById('box-select');
//
//  // Estado de filtros actuales
//  let selectedRack     = '';
//  let selectedBox      = '';
//  let selectedRackPos  = '';
//  let selectedBoxPos   = '';
//
//  // Dibuja una cuadrícula cols×rows, resaltando highlightLabel
//  function drawGrid(container, cols, rows, highlightLabel) {
//    container.innerHTML = '';
//    for (let r = 1; r <= rows; r++) {
//      for (let c = 0; c < cols; c++) {
//        const cell = document.createElement('div');
//        cell.className = 'schema-cell';
//        const label = String.fromCharCode(65 + c) + r;
//        cell.textContent = label;
//        if (label === highlightLabel) cell.classList.add('highlight');
//        cell.addEventListener('click', () => {
//          onSchemaClick(container.id, label);
//        });
//        container.appendChild(cell);
//      }
//    }
//  }
//
//  // Aplica todos los filtros combinados a la tabla
//  function applyFilters() {
//    const rows = Array.from(table.tBodies[0].rows);
//    rows.forEach(row => {
//      const rck   = row.dataset.rack;
//      const rpos  = row.dataset.rackCol + row.dataset.rackRow;
//      const bx    = row.dataset.box;
//      const bpos  = row.dataset.boxCol + row.dataset.boxRow;
//
//      // Chequeo de cada filtro (si está vacío, pasa)
//      const okRack       = !selectedRack    || rck   === selectedRack;
//      const okBox        = !selectedBox     || bx    === selectedBox;
//      const okRackPos    = !selectedRackPos || rpos  === selectedRackPos;
//      const okBoxPos     = !selectedBoxPos  || bpos  === selectedBoxPos;
//
//      // Para mostrarse, debe cumplir TODAS las condiciones activas
//      row.style.display = (okRack && okBox && okRackPos && okBoxPos)
//                          ? '' : 'none';
//    });
//  }
//
//  // Cuando cambias el select de rack
//  rackSelect.addEventListener('change', () => {
//    selectedRack    = rackSelect.value;
//    selectedRackPos = '';         // reset posición concreta
//    drawGrid(rackSchema, 4, 4, '');
//    applyFilters();
//  });
//
//  // Cuando cambias el select de box
//  boxSelect.addEventListener('change', () => {
//    selectedBox     = boxSelect.value;
//    selectedBoxPos  = '';         // reset posición concreta
//    drawGrid(boxSchema, 9, 9, '');
//    applyFilters();
//  });
//
//  // Cuando haces click en una celda de rack o box
//  function onSchemaClick(containerId, label) {
//    if (containerId === 'rack-scheme') {
//      selectedRackPos = label;
//      // si no había seleccionado rack, no filtramos por rack id,
//      // solo por la posición dentro del rack.
//      drawGrid(rackSchema, 4, 4, label);
//    } else {
//      selectedBoxPos = label;
//      drawGrid(boxSchema, 9, 9, label);
//    }
//    applyFilters();
//  }
//
//  // Al clicar en una fila de la tabla: sincroniza selectores
//  table.addEventListener('click', e => {
//    const tr = e.target.closest('tr[data-id]');
//    if (!tr) return;
//
//    // Extraemos datos
//    selectedRack    = tr.dataset.rack;
//    selectedBox     = tr.dataset.box;
//    selectedRackPos = tr.dataset.rackCol + tr.dataset.rackRow;
//    selectedBoxPos  = tr.dataset.boxCol  + tr.dataset.boxRow;
//
//    // Actualizamos selects y esquemas
//    rackSelect.value = selectedRack;
//    boxSelect.value  = selectedBox;
//    drawGrid(rackSchema, 4, 4, selectedRackPos);
//    drawGrid(boxSchema, 9, 9, selectedBoxPos);
//
//    applyFilters();
//  });
//
//  // INIT: dibuja esquemas vacíos y aplica filtro (para mostrar todo)
//  drawGrid(rackSchema, 4, 4, '');
//  drawGrid(boxSchema, 9, 9, '');
//  applyFilters();
//});





//document.addEventListener('DOMContentLoaded', () => {
//  const table = document.getElementById('sample-table');
//  const rackSchema = document.getElementById('rack-scheme');
//  const boxSchema = document.getElementById('box-scheme');
//  const rackSelect = document.getElementById('rack-select');
//  const boxSelect = document.getElementById('box-select');
//  const infoRack = document.getElementById('rack-info');
//  const infoBox = document.getElementById('box-info');
//
//  // Dibuja cuadrícula y resalta
//  function drawGrid(container, cols, rows, highlightLabel) {
//    container.innerHTML = '';
//    for (let r = 1; r <= rows; r++) {
//      for (let c = 0; c < cols; c++) {
//        const cell = document.createElement('div');
//        cell.className = 'schema-cell';
//        const label = String.fromCharCode(65 + c) + r;
//        cell.textContent = label;
//        if (label === highlightLabel) cell.classList.add('highlight');
//        cell.addEventListener('click', () => onCellClick(container.id, label));
//        container.appendChild(cell);
//      }
//    }
//  }
//
//  // Cuando clicas en fila de la tabla
//  table.addEventListener('click', e => {
//    const tr = e.target.closest('tr[data-id]');
//    if (!tr) return;
//
//    // Extraigo datos del dataset
//    const rack = tr.dataset.rack;
//    const rackRow = tr.dataset.rackRow;
//    const rackCol = tr.dataset.rackCol;
//    const box = tr.dataset.box;
//    const boxRow = tr.dataset.boxRow;
//    const boxCol = tr.dataset.boxCol;
//    const strain = tr.dataset.strain;  // ¡necesitamos este dataset!
//
//    // Actualizo selects
//    rackSelect.value = rack;
//    boxSelect.value = box;
//
//    // Dibujo esquemas
//    drawGrid(rackSchema, 4, 4, rackCol + rackRow);
//    drawGrid(boxSchema, 9, 9, boxCol + boxRow);
//
//    // Muestro info debajo de cada esquema
//    infoRack.textContent = `Rack ${rack}: Caja ${rackCol}${rackRow}`;
//    infoBox.textContent = `Caja ${box}: Cepa ${strain} (${boxCol}${boxRow})`;
//  });
//
//  // Filtrado por rack / box
//  rackSelect.addEventListener('change', () => {
//    const val = rackSelect.value;
//    filterRows(r => !val || r.dataset.rack === val);
//    drawGrid(rackSchema, 4, 4, '');
//  });
//  boxSelect.addEventListener('change', () => {
//    const val = boxSelect.value;
//    filterRows(r => !val || r.dataset.box === val);
//    drawGrid(boxSchema, 9, 9, '');
//  });
//
//  function filterRows(fn) {
//    Array.from(table.tBodies[0].rows).forEach(r => {
//      r.style.display = fn(r) ? '' : 'none';
//    });
//  }
//
//  // Click en celdas de esquema
//  function onCellClick(containerId, label) {
//    if (containerId === 'rack-scheme') {
//      // Si clic rack: filtramos tabla por rackRow+rackCol = label
//      filterRows(r => (r.dataset.rackCol + r.dataset.rackRow) === label);
//      // También marcamos la celda
//      drawGrid(rackSchema, 4, 4, label);
//    } else {
//      // Si clic caja:
//      filterRows(r => (r.dataset.boxCol + r.dataset.boxRow) === label);
//      drawGrid(boxSchema, 9, 9, label);
//    }
//  }
//
//  // Inicializo con esquemas vacíos
//  drawGrid(rackSchema, 4, 4, '');
//  drawGrid(boxSchema, 9, 9, '');
//});