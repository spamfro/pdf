from utils.fn import branch, iflatten, pipe
from utils.parse import (
  date_from_match,
  float_number_from_match,
  init_data,
  number_from_match, 
  once,
  parse_field,
  parse_regex, 
  valid_data
)


parse_kin = pipe(parse_regex(r'КЛИЕНТСКИ НОМЕР:(\d+)'), number_from_match)
parse_invoice = pipe(parse_regex(r'ФАКТУРА ОРИГИНАЛ № (\d+)'), number_from_match)
parse_invoice_date = pipe(parse_regex(r'Дата на издаване (\d+)/(\d+)/(\d+)'), date_from_match)
parse_due_date = pipe(parse_regex(r'Краен срок за плащане (\d+)/(\d+)/(\d+)'), date_from_match)
parse_period_start_date = pipe(parse_regex(r'Период на фактуриране от (\d+)/(\d+)/(\d+) до \d+/\d+/\d+'), date_from_match)
parse_period_end_date = pipe(parse_regex(r'Период на фактуриране от \d+/\d+/\d+ до (\d+)/(\d+)/(\d+)'), date_from_match)
parse_next_report_date = pipe(parse_regex(r'Следващият реален отчет на вашите водомери ще бъде в периода от: (\d+)\.(\d+)\.(\d+) до \d+\.\d+\.\d+'), date_from_match)
parse_supply_price = pipe(parse_regex(r'Доставяне на питейна вода ___ ([\d\.]+) ___ [\d\.]+ ___ [\d\.]+ лв'), float_number_from_match)
parse_supply_quantity = pipe(parse_regex(r'Доставяне на питейна вода ___ [\d\.]+ ___ ([\d\.]+) ___ [\d\.]+ лв'), float_number_from_match)
parse_supply_due = pipe(parse_regex(r'Доставяне на питейна вода ___ [\d\.]+ ___ [\d\.]+ ___ ([\d\.]+) лв'), float_number_from_match)
parse_drain_price = pipe(parse_regex(r'Отвеждане на отпадъчни води ___ ([\d\.]+) ___ [\d\.]+ ___ [\d\.]+ лв'), float_number_from_match)
parse_drain_quantity = pipe(parse_regex(r'Отвеждане на отпадъчни води ___ [\d\.]+ ___ ([\d\.]+) ___ [\d\.]+ лв'), float_number_from_match)
parse_drain_due = pipe(parse_regex(r'Отвеждане на отпадъчни води ___ [\d\.]+ ___ [\d\.]+ ___ ([\d\.]+) лв'), float_number_from_match)
parse_filter_price = pipe(parse_regex(r'Пречистване на отпадъчни води ___ ([\d\.]+) ___ [\d\.]+ ___ [\d\.]+ лв'), float_number_from_match)
parse_filter_quantity = pipe(parse_regex(r'Пречистване на отпадъчни води ___ [\d\.]+ ___ ([\d\.]+) ___ [\d\.]+ лв'), float_number_from_match)
parse_filter_due = pipe(parse_regex(r'Пречистване на отпадъчни води ___ [\d\.]+ ___ [\d\.]+ ___ ([\d\.]+) лв'), float_number_from_match)
parse_due = pipe(parse_regex(r'Сума по сделката: ___ ([\d\.]+) лв'), float_number_from_match)
parse_tax_rate = pipe(parse_regex(r'ДДС  (\d+)% от [\d\.]+ лв: ___ [\d\.]+ лв'), float_number_from_match)
parse_tax_due = pipe(parse_regex(r'ДДС  \d+% от [\d\.]+ лв: ___ ([\d\.]+) лв'), float_number_from_match)
parse_past_due = pipe(parse_regex(r'Старо салдо ___ (-?[\d\.]+) лв'), float_number_from_match)
parse_total_due = pipe(parse_regex(r'ОБЩА ДЪЛЖИМА СУМА ___ (-?[\d\.]+) лв'), float_number_from_match)
parse_account = pipe(parse_regex(r'договорна сметка: (\d+)'), number_from_match)
parse_detail_meter_id = pipe(parse_regex(r'(\d+) ___ [\d\.]+ ___ \d+/\d+/\d+ ___ .+ ___ [\d\.]+ ___ \d+/\d+/\d+ ___ .+ ___ [\d\.]+ \s*m3'), number_from_match)
parse_detail_old_value = pipe(parse_regex(r'\d+ ___ ([\d\.]+) ___ \d+/\d+/\d+ ___ .+ ___ [\d\.]+ ___ \d+/\d+/\d+ ___ .+ ___ [\d\.]+ \s*m3'), float_number_from_match)
parse_detail_old_date = pipe(parse_regex(r'\d+ ___ [\d\.]+ ___ (\d+)/(\d+)/(\d+) ___ .+ ___ [\d\.]+ ___ \d+/\d+/\d+ ___ .+ ___ [\d\.]+ \s*m3'), date_from_match)
parse_detail_new_value = pipe(parse_regex(r'\d+ ___ [\d\.]+ ___ \d+/\d+/\d+ ___ .+ ___ ([\d\.]+) ___ \d+/\d+/\d+ ___ .+ ___ [\d\.]+ \s*m3'), float_number_from_match)
parse_detail_new_date = pipe(parse_regex(r'\d+ ___ [\d\.]+ ___ \d+/\d+/\d+ ___ .+ ___ [\d\.]+ ___ (\d+)/(\d+)/(\d+) ___ .+ ___ [\d\.]+ \s*m3'), date_from_match)
parse_details_complete = pipe(parse_regex(r'ОБЩО ЗА АДРЕС НА КОНСУМАЦИЯ ___ [\d\.]+ m3'), lambda match: True if match else None)


class detail_parser():
  def __init__(self):
    self.data = init_data(['meter_id', 'old_value', 'old_date', 'new_value', 'new_date'])
    self.parse_detail = pipe(
      branch(
        parse_field('meter_id', parse_detail_meter_id),
        parse_field('old_value', parse_detail_old_value),
        parse_field('old_date', parse_detail_old_date),
        parse_field('new_value', parse_detail_new_value),
        parse_field('new_date', parse_detail_new_date),
      ),
      iflatten
    )
    
  def parse_line(self, line):
    self.data.update(self.parse_detail(line))
    return valid_data(self.data)


class details_parser():
  def __init__(self):
    self.data = []
    self.parse_detail = detail_parser().parse_line
    
  def parse_line(self, line):
    if (detail := self.parse_detail(line)):
      self.data.append(detail)
      self.parse_detail = details_parser().parse_line
    return self.data if parse_details_complete(line) else None


class digest_parser():
  def __init__(self):
    self.data = init_data([
      'kin',
      'invoice',
      'invoice_date',
      'due_date',
      'period_start_date',
      'period_end_date',
      'next_report_date',
      'supply_price',
      'supply_quantity',
      'supply_due',
      'drain_price',
      'drain_quantity',
      'drain_due',
      'filter_price',
      'filter_quantity',
      'filter_due',
      'due',
      'tax_rate',
      'tax_due',
      'past_due',
      'total_due',
      'account',
      'details'
    ])
    self.parse_digest = pipe(
      branch(
        once(parse_field('kin', parse_kin)),
        once(parse_field('invoice', parse_invoice)),
        once(parse_field('invoice_date', parse_invoice_date)),
        once(parse_field('due_date', parse_due_date)),
        once(parse_field('period_start_date', parse_period_start_date)),
        once(parse_field('period_end_date', parse_period_end_date)),
        once(parse_field('next_report_date', parse_next_report_date)),
        once(parse_field('supply_price', parse_supply_price)),
        once(parse_field('supply_quantity', parse_supply_quantity)),
        once(parse_field('supply_due', parse_supply_due)),
        once(parse_field('drain_price', parse_drain_price)),
        once(parse_field('drain_quantity', parse_drain_quantity)),
        once(parse_field('drain_due', parse_drain_due)),
        once(parse_field('filter_price', parse_filter_price)),
        once(parse_field('filter_quantity', parse_filter_quantity)),
        once(parse_field('filter_due', parse_filter_due)),
        once(parse_field('due', parse_due)),
        once(parse_field('tax_rate', parse_tax_rate)),
        once(parse_field('tax_due', parse_tax_due)),
        once(parse_field('past_due', parse_past_due)),
        once(parse_field('total_due', parse_total_due)),
        once(parse_field('account', parse_account)),
        once(parse_field('details', details_parser().parse_line))
      ),
      iflatten
    )
  def parse_line(self, line):
    self.data.update(self.parse_digest(line))
    return valid_data(self.data)


def parse_digest(digest):
  parser = digest_parser()
  for line in digest:
    if parser.parse_line(line) is not None:
      break
  return parser.data
  