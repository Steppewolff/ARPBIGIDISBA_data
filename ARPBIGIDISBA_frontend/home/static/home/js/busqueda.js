function createDualListbox(selectName, leftLabel, rightLabel) {
    const $select = $('select[name="' + selectName + '"]').hide();
    const options = $select.find('option').map(function() {
        return { value: $(this).val(), text: $(this).text() };
    }).get().filter(o => o.value);

    const html = `
        <div class="dual-listbox row no-gutters border rounded" style="overflow:hidden">
            <div class="col-5">
                <div class="select2-header">${leftLabel}</div>
                <div class="p-2 border-bottom">
                    <input type="text" class="form-control form-control-sm search-left" placeholder="Search...">
                </div>
                <div class="items-container left-items"></div>
                <div class="count-badge left-count">0 items</div>
            </div>
            <div class="col-2 d-flex flex-column align-items-center justify-content-center border-left border-right" style="gap:8px;padding:10px">
                <button type="button" class="btn btn-primary btn-sm btn-right" style="width:36px">&#8250;</button>
                <button type="button" class="btn btn-outline-secondary btn-sm btn-left" style="width:36px">&#8249;</button>
            </div>
            <div class="col-5">
                <div class="select2-header">${rightLabel}</div>
                <div class="p-2 border-bottom">
                    <input type="text" class="form-control form-control-sm search-right" placeholder="Search...">
                </div>
                <div class="items-container right-items"></div>
                <div class="count-badge right-count">0 items</div>
            </div>
        </div>`;

    const $box = $(html);
    $select.after($box);

    const $left  = $box.find('.left-items');
    const $right = $box.find('.right-items');

    function makeRow(opt) {
        return $(`<div class="item-row" data-value="${opt.value}">
                    <input type="checkbox"> ${opt.text}
                  </div>`);
    }

    function updateCounts() {
        $box.find('.left-count').text($left.find('.item-row').length + ' items');
        $box.find('.right-count').text($right.find('.item-row').length + ' items');
    }

    function syncSelect() {
        $select.find('option').prop('selected', false);
        $right.find('.item-row').each(function() {
            $select.find('option[value="' + $(this).data('value') + '"]').prop('selected', true);
        });
        updateCounts();
    }

    options.forEach(opt => $left.append(makeRow(opt)));
    updateCounts();
    let lastChecked = null;

    $box.on('click', '.item-row', function(e) {
        const $rows = $(this).closest('.items-container').find('.item-row:visible');
        const $checkbox = $(this).find('input');

        if (!$(e.target).is('input')) {
            $checkbox.prop('checked', !$checkbox.prop('checked'));
        }

        // Shift+click: seleccionar rango
        if (e.shiftKey && lastChecked) {
            const $lastRow = $(lastChecked);
            const lastIndex = $rows.index($lastRow);
            const currentIndex = $rows.index($(this));

            const from = Math.min(lastIndex, currentIndex);
            const to   = Math.max(lastIndex, currentIndex);
            const checked = $checkbox.prop('checked');

            $rows.slice(from, to + 1).each(function() {
                $(this).find('input').prop('checked', checked);
                $(this).toggleClass('checked', checked);
            });
        }

        $(this).toggleClass('checked', $checkbox.prop('checked'));
        lastChecked = this;
    });

    $box.find('.btn-right').on('click', function() {
        $left.find('.item-row input:checked').closest('.item-row').each(function() {
            $(this).find('input').prop('checked', false);
            $(this).removeClass('checked');
            $right.append($(this));
        });
        syncSelect();
    });

    $box.find('.btn-left').on('click', function() {
        $right.find('.item-row input:checked').closest('.item-row').each(function() {
            $(this).find('input').prop('checked', false);
            $(this).removeClass('checked');
            $left.append($(this));
        });
        syncSelect();
    });

    $box.find('.search-left').on('input', function() {
        const t = $(this).val().toLowerCase();
        $left.find('.item-row').each(function() {
            $(this).toggle($(this).text().toLowerCase().includes(t));
        });
    });

    $box.find('.search-right').on('input', function() {
        const t = $(this).val().toLowerCase();
        $right.find('.item-row').each(function() {
            $(this).toggle($(this).text().toLowerCase().includes(t));
        });
    });
}

$(document).ready(function() {
    createDualListbox('isolate_name', 'Available isolates', 'Selected isolates');
    createDualListbox('project_name', 'Available projects', 'Selected projects');

    // WGS genes: Select2 pill-style multi-select
    $('#wgs_genes_select').select2({
        placeholder: '— Select genes to add as columns in Results —',
        allowClear: true,
        width: '100%',
        closeOnSelect: false,
    });

    $('#wgs_select_all').on('click', function() {
        const $sel = $('#wgs_genes_select');
        const allVals = $sel.find('option').map(function() { return $(this).val(); }).get();
        $sel.val(allVals).trigger('change');
    });
});