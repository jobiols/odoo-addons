# For copyright and license notices, see __manifest__.py file in module root

from openerp import models
from datetime import datetime, timedelta

RECEIVABLE_ID = 1
PAYABLE_ID = 2
CASH_ID = 3


class CashFlowReport(models.AbstractModel):
    _name = "report.cash_flow.cash_flow_report_template"
    _last_printed = (0.0, 0.0, 0.0, 0.0, 0.0)
    _receivable = []
    _payable = []

    @staticmethod
    def inc_day(day):
        dt = datetime.strptime(day, '%Y-%m-%d')
        dt += timedelta(days=1)
        return datetime.strftime(dt, '%Y-%m-%d')

    def totalize(self, account, date):
        trial_balance = self.env['report.account.report_trialbalance']
        account_res = trial_balance.with_context(date_to=date)._get_accounts(
            account, 'movement')

        total = 0
        for account in account_res:
            total = account['balance']
        return total

    def acc_load(self, acc, accounts, date_from, date_to, state):
        """ Carga en acc las cantidades de dinero que se supone van a
            entrar en las fechas de vencimiento
        """
        # elimina datos anteriores si los hay
        acc.clear()
        aml_obj = self.env['account.move.line']
        domain = [('account_id', 'in', accounts.ids),
                  ('date_maturity', '>=', date_from),
                  ('date_maturity', '<=', date_to)]
        for line in aml_obj.search(domain, order='date_maturity'):
            amount = line.debit if state == 'debit' else line.credit
            acc.append({'date': line.date_maturity, 'value': amount})

    def acc_balance(self, acc, date):
        """ Calcula la suma de todos los items hasta date inclusive
        """
        ret = 0.0
        for item in acc:
            if item['date'] <= date:
                ret += item['value']
            else:
                return ret
        return ret

    def printable(self, receivable, cash, payable, expense, revenue):
        """ Usado para decidir si una linea del reporte debe imprimirse, si
            la linea contiene los cuatro elementos en cero no se imprime.
        """
        if receivable == 0 and cash == 0 and payable == 0 \
            and expense == 0 and revenue == 0:
            return False
        if (receivable, cash, payable, expense, revenue) == self._last_printed:
            return False
        self._last_printed = (receivable, cash, payable, expense, revenue)
        return True

    def expense_forecast(self, date):
        """ Obtener los gastos previstos hasta la fecha date inclusive
        """
        self._cr.execute("""
            SELECT SUM(amount) FROM cash_flow_forecast
            WHERE
              type = 'expenses'
              and forecast_date <= %s
              and state = 'foreseen'
        """, (date,))
        ret = self._cr.fetchall()[0][0]
        return ret if ret else 0

    def revenue_forecast(self, date):
        """ Obtener los ingresos previstos hasta la fecha date inclusive
        """
        self._cr.execute("""
            SELECT SUM(amount) FROM cash_flow_forecast
            WHERE
              type = 'incomes'
              and forecast_date <= %s
              and state = 'foreseen'
        """, (date,))
        ret = self._cr.fetchall()[0][0]
        return ret if ret else 0

    def get_report_values(self, docids, data=None):
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']

        # Calculamos la lista de receivables
        domain = [('user_type_id', '=', RECEIVABLE_ID)]
        receivable_ids = self.env['account.account'].search(domain)
        self.acc_load(self._receivable, receivable_ids, date_from, date_to,
                      'debit')

        # Calculamos la lista de payables
        domain = [('user_type_id', '=', PAYABLE_ID)]
        payable_ids = self.env['account.account'].search(domain)
        self.acc_load(self._payable, payable_ids, date_from, date_to,
                      'credit')

        domain = [('user_type_id', '=', CASH_ID)]
        cash_ids = self.env['account.account'].search(domain)

        docs = []
        trial_balance = self.env['report.account.report_trialbalance']
        while date_from <= date_to:

            # date_from es la variable del loop
            trial = trial_balance.with_context(date_to=date_from)

            # calcular los receivables hasta esta fecha de la lista
            receivable = self.acc_balance(self._receivable, date_from)

            cash = 0
            account_res = trial._get_accounts(cash_ids, 'movement')
            for account in account_res:
                cash += account['balance']

            # calcular los payables hasta esta fecha de la lista
            payable = self.acc_balance(self._payable, date_from)

            # calcular los gastos previstos hasta esta fecha
            expense_forecast = self.expense_forecast(date_from)

            # calcular los ingresos previstos hasta esta fecha
            revenue_forecast = self.revenue_forecast(date_from)

            if self.printable(receivable, cash, payable, expense_forecast,
                              revenue_forecast):
                docs.append({
                    'date': date_from,
                    'receivable': receivable,
                    'cash': cash,
                    'payable': payable,
                    'expense-forecast': expense_forecast,
                    'revenue-forecast': revenue_forecast,
                    'total': receivable + cash - payable + revenue_forecast
                             - expense_forecast},
                )

            date_from = self.inc_day(date_from)

        return {
            'docs': docs,
        }
