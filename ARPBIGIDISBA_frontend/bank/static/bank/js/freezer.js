// bank/static/bank/js/freezer.js

document.addEventListener('DOMContentLoaded', () => {
  // Leemos el JSON embebido
  const samples = JSON.parse(document.getElementById('samples-data').textContent);

  const table          = document.getElementById('sample-table');
  const rackSelect     = document.getElementById('rack-select');
  const boxSelect      = document.getElementById('box-select');
  const rackSchemaC    = document.getElementById('rack-schema');
  const boxSchemaC     = document.getElementById('box-schema');
  const rackInfo       = document.getElementById('rack-info');
  const boxInfo        = document.getElementById('box-info');

  let selectedRack = '';
  let selectedBox  = '';

  // Crea una rejilla cols×rows dentro de "container", tipo 'rack' o 'box'
  function createGrid(container, cols, rows, type) {
    container.innerHTML = '';
    const grid = document.createElement('div');
    grid.className = 'schema-grid';
    grid.style.gridTemplateColumns = `min-content repeat(${cols}, min-content)`;
    grid.style.gridTemplateRows    = `min-content repeat(${rows}, min-content)`;

    // Esquina vacía
    grid.appendChild(document.createElement('div')).className = 'schema-header';
    // Cabeceras de columnas
    for (let c = 1; c <= cols; c++) {
      const h = document.createElement('div');
      h.className = 'schema-header';
      h.textContent = String.fromCharCode(64 + c);
      grid.appendChild(h);
    }
    // Filas
    for (let r = 1; r <= rows; r++) {
      // Encabezado de fila
      const h = document.createElement('div');
      h.className = 'schema-header';
      h.textContent = r;
      grid.appendChild(h);

      for (let c = 1; c <= cols; c++) {
        const cell = document.createElement('div');
        cell.className = 'schema-cell';
        cell.dataset.col = String.fromCharCode(64 + c);
        cell.dataset.row = r;
        // click handler
        cell.addEventListener('click', () => handleCellClick(cell, type));
        grid.appendChild(cell);
      }
    }
    container.appendChild(grid);
    return grid;
  }

function drawRackSchema(rackId) {
  const grid = createGrid(rackSchemaC, 4, 4, 'rack');
  rackInfo.textContent = rackId ? `Rack: ${rackId}` : '';
  if (!rackId) return;

  // Normalizamos claves a formato "A1", "B2", etc.
  const map = {};
  samples.forEach(s => {
    if (s.rack === rackId) {
      console.log('rack match:', s.rack_col, s.rack_row, '→ box:', s.box);
      const col = String(s.rack_col).toUpperCase().trim();
      const row = String(s.rack_row).trim();
      const key = col + row;
      map[key] = s.box;
    }
  });

  grid.querySelectorAll('.schema-cell').forEach(cell => {
    const key = cell.dataset.col + cell.dataset.row;
    if (map[key]) {
      cell.textContent = `Caja ${map[key]}`;
      cell.title = `Caja ${map[key]}`;
    } else {
      cell.textContent = '';
      cell.title = '';
    }
  });
}

  function drawBoxSchema(boxId) {
    const grid = createGrid(boxSchemaC, 9, 9, 'box');
    boxInfo.textContent = '';
    if (!boxId) return;

    // Mapas para id, tooltip y info
    const idMap      = {};
    const tipMap     = {};
    const infoMap    = {};
    samples.filter(s => s.box === boxId).forEach(s => {
      const key = s.box_col + s.box_row;
      idMap[key]   = s.id;
      tipMap[key]  = s.strain;
      infoMap[key] = s;
    });

    grid.querySelectorAll('.schema-cell').forEach(cell => {
      const key = cell.dataset.col + cell.dataset.row;
      if (idMap[key]) {
        cell.textContent = `Id ${idMap[key]}`;
        cell.title = `Strain: ${tipMap[key]}`;
        cell.dataset.info = JSON.stringify(infoMap[key]);
      } else {
        cell.textContent = '';
        cell.title = '';
        delete cell.dataset.info;
      }
    });
  }

  function updateBoxSelect(rackId) {
    boxSelect.innerHTML = '<option value="">Todos</option>';
    let boxes = rackId
      ? [...new Set(samples.filter(s => s.rack === rackId).map(s => s.box))]
      : [...new Set(samples.map(s => s.box))];
    boxes.sort().forEach(b => {
      const o = document.createElement('option');
      o.value = b; o.textContent = b;
      boxSelect.appendChild(o);
    });
  }

  function applyFilters() {
    Array.from(table.tBodies[0].rows).forEach(row => {
      const okRack = !selectedRack || row.dataset.rack === selectedRack;
      const okBox  = !selectedBox  || row.dataset.box  === selectedBox;
      row.style.display = (okRack && okBox) ? '' : 'none';
    });
  }

  function handleCellClick(cell, type) {
    // Eliminar selección previa
    cell.parentElement.querySelectorAll('.schema-cell').forEach(c => c.classList.remove('selected'));
    cell.classList.add('selected');

    if (type === 'rack') {
      const key = cell.dataset.col + cell.dataset.row;
      const box = samples.find(s => s.rack===selectedRack && (s.rack_col+s.rack_row)===key)?.box;
      selectedBox = box || '';
      boxSelect.value = selectedBox;
      drawBoxSchema(selectedBox);
      applyFilters();
    } else {
      if (cell.dataset.info) {
        const s = JSON.parse(cell.dataset.info);
        boxInfo.textContent = `Name: ${s.name}\nStrain: ${s.strain}\nDescription: ${s.description}`;
      } else {
        boxInfo.textContent = '';
      }
    }
  }

  // Listeners
  rackSelect.addEventListener('change', () => {
    selectedRack = rackSelect.value;
    selectedBox  = '';
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

  // Init
  drawRackSchema('');
  drawBoxSchema('');
  updateBoxSelect('');
});