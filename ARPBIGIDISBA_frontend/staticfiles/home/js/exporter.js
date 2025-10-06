// exporter.js
(function () {
  'use strict';

  // Selector para detectar enlaces de export.
  // Si prefieres una clase concreta, cámbialo por '.export-btn' o similar.
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
      // No hay enlaces de export en esta página; nada que hacer.
      return;
    }

    // Ajuste: si tienes múltiples tablas y quieres targetear una concreta,
    // pon en la tabla un atributo data-table-index="0" (0-based).
    // Si no hay data-table-index, el plugin sin parámetro devuelve la primera tabla.
    links.forEach(function (link) {
      link.addEventListener('click', function (e) {
        // Interceptamos la navegación para añadir excluded_columns
        e.preventDefault();

        var href = link.getAttribute('href') || '';

        // Si el enlace tiene data-table-index, usamos ese índice
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
          hidden = getHiddenColumnsForTableIndex(); // sin parámetro -> primera tabla
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