def mark_required_fields(form):
    for field in form.fields.values():
        if field.required and not str(field.label).endswith(' *'):
            field.label = f'{field.label} *'
