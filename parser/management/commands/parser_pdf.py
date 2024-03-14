from django.core.management.base import BaseCommand
import pandas as pd
from camelot import read_pdf as camelot_read_pdf
from datetime import datetime
import decimal
from parser.models import Transaction

date_format = "%d/%m/%Y"

def extract_text_from_pdf(pdf_path):
    tables = camelot_read_pdf(pdf_path, pages='all', flavor='stream')
    return tables

class Command(BaseCommand):
    help = 'Parse PDF and insert data into the database'

    def handle(self, *args, **kwargs):
        all_text = extract_text_from_pdf('static/pdfs/test_pdf.pdf')

        all_tables_data = []
        for elem in all_text:
            df = pd.DataFrame(elem.df)
            for i in range(2, len(df)):
                helper_array = []
                for index in df.columns.array:
                    if index == 0:
                        app_id_and_xref = df.iloc[i][index].split()
                        for elem in app_id_and_xref:
                            helper_array.append(int(elem))
                    elif index == 1:
                        date_object = datetime.strptime(df.iloc[i][index], date_format).date()
                        helper_array.append(date_object)
                    elif index == 2:
                        helper_array.append(df.iloc[i][index])
                    elif index == 3:
                        sub_borker = df.iloc[i][index].split('\n')
                        if len(sub_borker) == 2:
                            helper_array.append(sub_borker[0])
                            helper_array.append(sub_borker[1])
                        else:
                            helper_array.append(None)
                            helper_array.append(sub_borker[0])
                    elif index == 4:
                        helper_array.append(df.iloc[i][index])
                    #getting empty value in 8th row
                    elif index == 8:
                        continue
                    else:
                        decimal_string = df.iloc[i][index].replace(',', '')
                        value_decimal = decimal.Decimal(decimal_string)
                        helper_array.append(value_decimal)
                        
                all_tables_data.append(helper_array)

        
        for item in all_tables_data:
            app_id, xref, settlement_date, broker, sub_broker, borrower_name, description, total_loan_amount, commission_rate, upfront, upfront_incl_gst = item

            existing_count = Transaction.objects.filter(xref=xref, total_loan_amount=total_loan_amount).count()

            if existing_count == 0:
                new_transaction = Transaction(
                    app_id=app_id,
                    xref=xref,
                    settlement_date=settlement_date,
                    broker=broker,
                    sub_broker=sub_broker,
                    borrower_name=borrower_name,
                    description=description,
                    total_loan_amount=total_loan_amount,
                    commission_rate=commission_rate,
                    upfront=upfront,
                    upfront_incl_gst=upfront_incl_gst
                )
                if new_transaction.total_loan_amount > 100000:
                    new_transaction.tier_level = 'Tier 1'
                elif new_transaction.total_loan_amount > 50000:
                    new_transaction.tier_level = 'Tier 2'
                elif new_transaction.total_loan_amount > 10000:
                    new_transaction.tier_level = 'Tier 3'
                else:
                    new_transaction.tier_level = 'Tier 4'
                new_transaction.save()
            else:
                print(f"Duplicate found for Xref: {xref} and Total Loan Amount: {total_loan_amount}")

        transactions = Transaction.objects.all()

        for transaction in transactions:
            if transaction.total_loan_amount > 100000:
                transaction.tier_level = 'Tier 1'
            elif transaction.total_loan_amount > 50000:
                transaction.tier_level = 'Tier 2'
            elif transaction.total_loan_amount > 10000:
                transaction.tier_level = 'Tier 3'
            else:
                transaction.tier_level = 'Tier 4'
            transaction.save()

        self.stdout.write(self.style.SUCCESS('Successfully parsed PDF and inserted data into the database'))
