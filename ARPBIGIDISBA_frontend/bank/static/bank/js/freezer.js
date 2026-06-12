document.addEventListener('DOMContentLoaded', () => {
  const samples = JSON.parse(document.getElementById('samples-data').textContent);

  const table       = document.getElementById('sample-table');
  const rackSelect  = document.getElementById('rack-select');
  const boxSelect   = document.getElementById('box-select');
  const rackSchemaC = document.getElementById('rack-schema');
  const boxSchemaC  = document.getElementById('box-schema');
  const rackInfo    = document.getElementById('rack-info');
  const boxInfo     = document.getElementById('box-info');

  const backdrop    = document.getElementById('modal-backdrop');
  const editModal   = document.getElementById('edit-modal');
  const deleteModal = document.getElementById('delete-modal');
  const editForm    = document.getElementById('edit-form');
  const deleteForm  = document.getElementById('delete-form');

  const editPk        = document.getElementById('edit-pk');
  const editName      = document.getElementById('edit-name');
  const editStrain    = document.getElementById('edit-strain');
  const editSpecies   = document.getElementById('edit-species');
  const editClone     = document.getElementById('edit-clone');
  const editBox       = document.getElementById('edit-box');
  const editRackRow   = document.getElementById('edit-rack-row');
  const editRackCol   = document.getElementById('edit-rack-col');
  const editBoxRow    = document.getElementById('edit-box-row');
  const editBoxCol    = document.getElementById('edit-box-col');
  const editDesc      = document.getElementById('edit-description');
  const editCloseBtn  = document.getElementById('edit-close-btn');

  const deleteCloseBtn = document.getElementById('delete-close-btn');
  const deleteMessage  = document.getElementById('delete-message');

  let selectedRack = '';
  let selectedBox  = '';

  let currentEditSample = null;
  let currentDeleteId = null;

  function openModal(modal) {
    backdrop.style.display = 'block';
    modal.style.display = 'block';
  }

  function closeModal(modal) {
    modal.style.display = 'none';
    backdrop.style.display = 'none';
  }

  function colToLetter(val) {
    const s = String(val).toUpperCase().trim();
    if (/^\d+$/.test(s)) {
      return String.fromCharCode(64 + parseInt(s, 10));
    }
    return s;
  }

  function rackKey(s) {
    return colToLetter(s.rack_col) + String(s.rack_row).trim();
  }

  function boxKey(s) {
    return colToLetter(s.box_col) + String(s.box_row).trim();
  }

  function sameRack(s, rackId) { return String(s.rack) === String(rackId); }
  function sameBox(s, boxId)   { return String(s.box)  === String(boxId);  }

  function createGrid(container, cols, rows, type) {
    container.innerHTML = '';
    const grid = document.createElement('div');
    grid.className = 'schema-grid';
    grid.style.gridTemplateColumns = `min-content repeat(${cols}, min-content)`;
    grid.style.gridTemplateRows    = `min-content repeat(${rows}, min-content)`;

    const corner = document.createElement('div');
    corner.className = 'schema-header';
    grid.appendChild(corner);

    for (let c = 1; c <= cols; c++) {
      const h = document.createElement('div');
      h.className = 'schema-header';
      h.textContent = String.fromCharCode(64 + c);
      grid.appendChild(h);
    }
    for (let r = 1; r <= rows; r++) {
      const h = document.createElement('div');
      h.className = 'schema-header';
      h.textContent = r;
      grid.appendChild(h);
      for (let c = 1; c <= cols; c++) {
        const cell = document.createElement('div');
        cell.className = 'schema-cell';
        cell.dataset.col = String.fromCharCode(64 + c);
        cell.dataset.row = r;
        cell.setAttribute('role', 'button');
        cell.setAttribute('tabindex', '0');
        cell.setAttribute('aria-label', `${type === 'rack' ? 'Rack' : 'Box'} position ${cell.dataset.col}${cell.dataset.row}`);
        cell.addEventListener('click', () => handleCellClick(cell, type));
        cell.addEventListener('keydown', (e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            handleCellClick(cell, type);
          }
        });
        grid.appendChild(cell);
      }
    }
    container.appendChild(grid);
    return grid;
  }

  function drawRackSchema(rackId) {
    const grid = createGrid(rackSchemaC, 4, 4, 'rack');
    rackInfo.textContent = rackId ? `Selected rack: ${rackId}\nClick on a position to see its box.` : 'Select a rack to display its contents.';
    if (!rackId) return;

    const map = {};
    samples.forEach(s => {
      if (sameRack(s, rackId) && !map[rackKey(s)]) {
        map[rackKey(s)] = String(s.box);
      }
    });

    grid.querySelectorAll('.schema-cell').forEach(cell => {
      const key = cell.dataset.col + cell.dataset.row;
      cell.classList.remove('occupied', 'empty');
      if (map[key]) {
        cell.textContent = `Box ${map[key]}`;
        cell.title = `Box ${map[key]}`;
        cell.dataset.box = map[key];
        cell.classList.add('occupied');
      } else {
        cell.textContent = '';
        cell.title = 'Empty position';
        cell.dataset.box = '';
        cell.classList.add('empty');
      }
    });
  }

  function drawBoxSchema(boxId) {
    const grid = createGrid(boxSchemaC, 9, 9, 'box');
    boxInfo.textContent = boxId ? `Selected box: ${boxId}\nClick on a sample to view its data.` : 'Select a box to display its contents.';
    if (!boxId) return;

    const idMap = {}, tipMap = {}, infoMap = {};
    samples.filter(s => sameBox(s, boxId)).forEach(s => {
      const key    = boxKey(s);
      idMap[key]   = s.id;
      tipMap[key]   = s.strain;
      infoMap[key] = s;
    });

    grid.querySelectorAll('.schema-cell').forEach(cell => {
      const key = cell.dataset.col + cell.dataset.row;
      cell.classList.remove('occupied', 'empty');
      if (idMap[key]) {
        cell.textContent = `Id ${idMap[key]}`;
        cell.title = `Strain: ${tipMap[key]}`;
        cell.dataset.info = JSON.stringify(infoMap[key]);
        cell.classList.add('occupied');
      } else {
        cell.textContent = '';
        cell.title = 'Empty position';
        delete cell.dataset.info;
        cell.classList.add('empty');
      }
    });
  }

  function updateBoxSelect(rackId) {
    boxSelect.innerHTML = '<option value="">Todos</option>';
    const boxes = rackId
      ? [...new Set(samples.filter(s => sameRack(s, rackId)).map(s => String(s.box)))]
      : [...new Set(samples.map(s => String(s.box)))];
    boxes.sort().forEach(b => {
      const o = document.createElement('option');
      o.value = b;
      o.textContent = b;
      boxSelect.appendChild(o);
    });
  }

  function applyFilters() {
    Array.from(table.tBodies[0].rows).forEach(row => {
      const okRack = !selectedRack || row.dataset.rack === String(selectedRack);
      const okBox  = !selectedBox  || row.dataset.box  === String(selectedBox);
      row.style.display = (okRack && okBox) ? '' : 'none';
    });
  }

  function handleCellClick(cell, type) {
    cell.parentElement.querySelectorAll('.schema-cell')
      .forEach(c => c.classList.remove('selected'));
    cell.classList.add('selected');

    if (type === 'rack') {
      const box = cell.dataset.box || '';

      rackInfo.textContent = box
        ? `Rack: ${selectedRack}\nSelected box: ${box}`
        : `Rack: ${selectedRack}\n(empty position)`;

      selectedBox = box;

      if (box) {
        const exists = Array.from(boxSelect.options).some(o => o.value === box);
        if (!exists) {
          const o = document.createElement('option');
          o.value = box;
          o.textContent = box;
          boxSelect.appendChild(o);
        }
      }

      boxSelect.value = box;
      drawBoxSchema(box);
      applyFilters();
    } else {
      if (cell.dataset.info) {
        const s = JSON.parse(cell.dataset.info);
        boxInfo.textContent =
          `Name: ${s.name}\nStrain: ${s.strain}\nSpecies: ${s.species}\nClone: ${s.clone}\nDescription: ${s.description}`;
      } else {
        boxInfo.textContent = '';
      }
    }
  }

  function openEditModal(sample) {
    currentEditSample = sample;
    editForm.action = `/sample/${sample.id}/update/`;

    editPk.value = sample.id;
    editName.value = sample.name || '';
    editStrain.value = sample.strain || '';
    editSpecies.value = sample.species || '';
    editClone.value = sample.clone || '';
    editBox.value = sample.box || '';
    editRackRow.value = sample.rack_row || '';
    editRackCol.value = sample.rack_col || '';
    editBoxRow.value = sample.box_row || '';
    editBoxCol.value = sample.box_col || '';
    editDesc.value = sample.description || '';

    openModal(editModal);
  }

  function openDeleteModal(sample) {
    currentDeleteId = sample.id;
    deleteForm.action = `/sample/${sample.id}/delete/`;
    deleteMessage.textContent = `Are you sure you want to delete the record "${sample.name || sample.strain || sample.id}"?`;
    openModal(deleteModal);
  }

        if (table) {
          table.addEventListener('click', (e) => {
            const editBtn = e.target.closest('.js-edit-sample');
            const deleteBtn = e.target.closest('.js-delete-sample');

            if (editBtn) {
              const id = editBtn.dataset.id;
              const sample = samples.find(s => String(s.id) === String(id));
              if (sample) openEditModal(sample);
              return;
            }

            if (deleteBtn) {
              const id = deleteBtn.dataset.id;
              const sample = samples.find(s => String(s.id) === String(id));
              if (sample) openDeleteModal(sample);
            }
          });
        }

      editCloseBtn.addEventListener('click', () => closeModal(editModal));
      deleteCloseBtn.addEventListener('click', () => closeModal(deleteModal));
      backdrop.addEventListener('click', () => {
    closeModal(editModal);
    closeModal(deleteModal);
  });

  rackSelect.addEventListener('change', () => {
    selectedRack = rackSelect.value;
    selectedBox = '';
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

  drawRackSchema('');
  drawBoxSchema('');
  updateBoxSelect('');
});