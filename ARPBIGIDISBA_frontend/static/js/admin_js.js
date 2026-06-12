 (function( $ ) {

    jQuery.fn.doubleScroll = function(userOptions) {

        // Default options
        var options = {
            contentElement: undefined, // Widest element, if not specified first child element will be used
            scrollCss: {
                'overflow-x': 'auto',
                'overflow-y': 'hidden',
                'height': '20px'
            },
            contentCss: {
                'overflow-x': 'auto',
                'overflow-y': 'hidden'
            },
            onlyIfScroll: true, // top scrollbar is not shown if the bottom one is not present
            resetOnWindowResize: false, // recompute the top ScrollBar requirements when the window is resized
            timeToWaitForResize: 30 // wait for the last update event (usefull when browser fire resize event constantly during ressing)
        };

        $.extend(true, options, userOptions);

        // do not modify
        // internal stuff
        $.extend(options, {
            topScrollBarMarkup: '<div class="doubleScroll-scroll-wrapper"><div class="doubleScroll-scroll"></div></div>',
            topScrollBarWrapperSelector: '.doubleScroll-scroll-wrapper',
            topScrollBarInnerSelector: '.doubleScroll-scroll'
        });

        var _showScrollBar = function($self, options) {

            if (options.onlyIfScroll && $self.get(0).scrollWidth <= Math.round($self.width())) {
                // content doesn't scroll
                // remove any existing occurrence...
                $self.prev(options.topScrollBarWrapperSelector).remove();
                return;
            }

            // add div that will act as an upper scroll only if not already added to the DOM
            var $topScrollBar = $self.prev(options.topScrollBarWrapperSelector);

            if ($topScrollBar.length == 0) {

                // creating the scrollbar
                // added before in the DOM
                $topScrollBar = $(options.topScrollBarMarkup);
                $self.before($topScrollBar);

                // apply the css
                $topScrollBar.css(options.scrollCss);
                $(options.topScrollBarInnerSelector).css("height", "20px");
                $self.css(options.contentCss);

                var scrolling = false;

                // bind upper scroll to bottom scroll
                $topScrollBar.bind('scroll.doubleScroll', function() {
                    if (scrolling) {
                        scrolling = false;
                        return;
                    }
                    scrolling = true;
                    $self.scrollLeft($topScrollBar.scrollLeft());
                });

                // bind bottom scroll to upper scroll
                var selfScrollHandler = function() {
                    if (scrolling) {
                        scrolling = false;
                        return;
                    }
                    scrolling = true;
                    $topScrollBar.scrollLeft($self.scrollLeft());
                };
                $self.bind('scroll.doubleScroll', selfScrollHandler);
            }

            // find the content element (should be the widest one)
            var $contentElement;

            if (options.contentElement !== undefined && $self.find(options.contentElement).length !== 0) {
                $contentElement = $self.find(options.contentElement);
            } else {
                $contentElement = $self.find('>:first-child');
            }

            // set the width of the wrappers
            $(options.topScrollBarInnerSelector, $topScrollBar).width($contentElement.outerWidth());
            $topScrollBar.width($self.width());
            $topScrollBar.scrollLeft($self.scrollLeft());

        }

        return this.each(function() {

            var $self = $(this);

            _showScrollBar($self, options);

            // bind the resize handler
            // do it once
            if (options.resetOnWindowResize) {

                var id;
                var handler = function(e) {
                    _showScrollBar($self, options);
                };

                $(window).bind('resize.doubleScroll', function() {
                    // adding/removing/replacing the scrollbar might resize the window
                    // so the resizing flag will avoid the infinite loop here...
                    clearTimeout(id);
                    id = setTimeout(handler, options.timeToWaitForResize);
                });

            }

        });

    }

}( jQuery ));

(function($){

  function refreshDoubleScrollOnce($el) {
    if (!$el || $el.length === 0) return;
    // remove previous wrapper if it exists
    $el.prev('.doubleScroll-scroll-wrapper').remove();
    // remove old handlers
    $el.off('scroll.doubleScroll');
    // re-initialise
    $el.doubleScroll({ resetOnWindowResize: true });
  }

  function refreshDoubleScroll() {
    var $results = $('.results');
    refreshDoubleScrollOnce($results);
  }

  // Initialise when the page has fully loaded
  $(window).on('load', function(){
    refreshDoubleScroll();

    // Quick retry (in case the DOM changes right after load)
    window.requestAnimationFrame(refreshDoubleScroll);
    setTimeout(refreshDoubleScroll, 100);
  });

  // If .results is inside a Bootstrap collapse
  $(document).on('shown.bs.collapse', function() {
    $('.results:visible').each(function(){
      refreshDoubleScrollOnce($(this));
    });
  });

  // If .results is inside Bootstrap tabs
  $(document).on('shown.bs.tab', function() {
    $('.results:visible').each(function(){
      refreshDoubleScrollOnce($(this));
    });
  });

  // Observe dynamic changes inside .results (e.g. django_tables2_column_shifter)
  var resultsNode = document.querySelector('.results');
  if (resultsNode) {
    var mo = new MutationObserver(function(){
      if (window._ds_debounce) clearTimeout(window._ds_debounce);
      window._ds_debounce = setTimeout(function(){
        refreshDoubleScrollOnce($(resultsNode));
      }, 50);
    });
    mo.observe(resultsNode, { childList: true, subtree: true, attributes: true });
  }

})(jQuery);

function abrir_modal(url)
{
    $('#amr_clas_modal').load(url, function()
    {
    $(this).modal({
        backdrop: 'static',
        keyboard: false
    })
    $(this).modal('show');
    });
    return false;
}

function cerrar_modal()
{
$('#amr_clas_modal').modal('hide');
return false;
}

function showDialog() {
  var dialog = document.getElementById("myDialog");
  dialog.show();
}

function closeDialog() {
  var dialog = document.getElementById("myDialog");
  dialog.close();
}

$(document).ready(function() {
    $('.select2').select2({
        placeholder: "Select mutations",
        allowClear: true,
        width: '100%',
        closeOnSelect: false,
        templateResult: function(option) {
            if (!option.id) return option.text;
            return $('<span><input type="checkbox" style="margin-right: 5px;" /> ' + option.text + '</span>');
        },
        templateSelection: function(option) {
            return option.text;
        }
    });

    // Add interactivity: check the checkbox on click
    $('.select2').on('select2:select select2:unselect', function (e) {
        let selectedOptions = $(this).find(':selected').map(function() {
            return $(this).text();
        }).get().join(', ');
        console.log('Selected options:', selectedOptions);
    });
});