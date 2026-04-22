import django_tables2 as tables
from .models import Sample


class SampleTable(tables.Table):
    actions = tables.TemplateColumn(
        verbose_name='Acciones',
        orderable=False,
        template_code='''
            <div class="row-actions">
              <button type="button" class="js-edit-sample" data-id="{{ record.id }}">Editar</button>
              <button type="button" class="js-delete-sample" data-id="{{ record.id }}">Borrar</button>
            </div>
        '''
    )

    class Meta:
        model = Sample
        template_name = "django_tables2/bootstrap5.html"
        fields = (
            'id', 'species', 'name', 'strain', 'clone', 'description',
            'rack', 'rack_col', 'rack_row', 'box', 'box_col', 'box_row',
        )
        attrs = {
            "id": "sample-table",
            'class': 'table table-dark table-striped table-hover table-responsive results'
        }
        row_attrs = {
            'data-id': lambda r: r.id,
            'data-strain': lambda r: r.strain,
            'data-species': lambda r: r.species,
            'data-clone': lambda r: r.clone,
            'data-rack': lambda r: r.rack,
            'data-rack-row': lambda r: r.rack_row,
            'data-rack-col': lambda r: r.rack_col,
            'data-box': lambda r: r.box,
            'data-box-row': lambda r: r.box_row,
            'data-box-col': lambda r: r.box_col,
        }