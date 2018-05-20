
-- hay un conjunto de diarios por cajera que son los medios
-- de pago, cada diario apunta a una cuenta separada

-- salvo las de banco que no se puede


SELECT name,* from account_journal
where (type = 'bank' or type ='cash')
      and account_journal.cashier_id = 50

