// exporter.js
(function () {
  'use strict';

  // Selector para detectar enlaces de export.
  var EXPORT_LINK_SELECTOR = 'a[href*="_export"], a[data-export]';

  function onDomReady(fn) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn);
    } else {
      fn();
    }
  }

  function getHiddenColumnsForTableIndex(index) {
    try {
      if (typeof $ !== 'undefined' && $.django_tables2_column_shifter_hidden) {
        // plugin API: devuelve array de nombres de columnas ocultas
        return $.django_tables2_column_shifter_hidden(index) || [];
      }
      console.warn('django_tables2_column_shifter API no disponible (jQuery o plugin no cargado).');
      return [];
    } catch (err) {
      console.warn('Error obteniendo columnas ocultas desde column-shifter:', err);
      return [];
    }
  }

  function buildUrlWithExcludedColumns(href, hiddenCols) {
    var parts = href.split('?');
    var base = parts[0];
    var params = new URLSearchParams(parts[1] || '');
    if (hiddenCols && hiddenCols.length) {
      params.set('excluded_columns', hiddenCols.join(','));
    } else {
      // Remove param if no hidden columns
      params.delete('excluded_columns');
    }
    var qs = params.toString();
    return base + (qs ? ('?' + qs) : '');
  }

  onDomReady(function () {
    // Encuentra todos los enlaces de export actuales
    var links = document.querySelectorAll(EXPORT_LINK_SELECTOR);

    if (!links || links.length === 0) {
      return;
    }

    links.forEach(function (link) {
      link.addEventListener('click', function (e) {
        // Intercept navigation to add excluded_columns
        e.preventDefault();

        var href = link.getAttribute('href') || '';

        // If the link has data-table-index, use that index
        var tableIndexAttr = link.getAttribute('data-table-index');
        var tableIndex = null;
        if (tableIndexAttr !== null) {
          var idx = parseInt(tableIndexAttr, 10);
          if (!Number.isNaN(idx)) tableIndex = idx;
        }

        // Obtener columnas ocultas del plugin (si tableIndex es null, la API toma la primera tabla)
        var hidden = [];
        if (tableIndex !== null) {
          hidden = getHiddenColumnsForTableIndex(tableIndex);
        } else {
          hidden = getHiddenColumnsForTableIndex(); // no parameter -> first table
        }

        // Si no hay columnas ocultas, redirigimos tal cual
        if (!hidden || hidden.length === 0) {
          window.location = href;
          return;
        }

        // Construir nueva URL con excluded_columns
        var url = buildUrlWithExcludedColumns(href, hidden);
        window.location = url;
      });
    });
  });
})();