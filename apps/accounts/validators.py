import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_validate_email


def only_digits(value):
    return re.sub(r'\D', '', value or '')


def validate_cpf(cpf):
    cpf = only_digits(cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for size in (9, 10):
        total = sum(int(cpf[i]) * (size + 1 - i) for i in range(size))
        digit = (total * 10) % 11
        if digit == 10:
            digit = 0
        if digit != int(cpf[size]):
            return False
    return True


def validate_cnpj(cnpj):
    cnpj = only_digits(cnpj)
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False
    def digit(base, weights):
        total = sum(int(n) * w for n, w in zip(base, weights))
        rem = total % 11
        return 0 if rem < 2 else 11 - rem
    d1 = digit(cnpj[:12], [5,4,3,2,9,8,7,6,5,4,3,2])
    d2 = digit(cnpj[:12] + str(d1), [6,5,4,3,2,9,8,7,6,5,4,3,2])
    return cnpj[-2:] == f'{d1}{d2}'


def validate_cpf_cnpj(value):
    digits = only_digits(value)
    if not ((len(digits) == 11 and validate_cpf(digits)) or (len(digits) == 14 and validate_cnpj(digits))):
        raise ValidationError('Informe um CPF ou CNPJ válido.')


def normalize_document(value):
    digits = only_digits(value)
    validate_cpf_cnpj(digits)
    return digits


def format_phone(value):
    digits = only_digits(value)
    if len(digits) == 11:
        return f'({digits[:2]}) {digits[2:7]}-{digits[7:]}'
    if len(digits) == 10:
        return f'({digits[:2]}) {digits[2:6]}-{digits[6:]}'
    raise ValidationError('Informe um telefone válido com DDD.')


def validate_phone(value):
    digits = only_digits(value)
    if len(digits) not in (10, 11) or digits[:2] == '00':
        raise ValidationError('Informe um telefone válido com DDD.')
    if len(digits) == 11 and digits[2] != '9':
        raise ValidationError('Celular deve seguir o padrão (XX) 9XXXX-XXXX.')


def normalize_email(value):
    email = (value or '').strip().lower()
    django_validate_email(email)
    return email
