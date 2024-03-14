Dependecies :
pip install rest_framework, pandas, camelot-py


Start project :
python manage.py makemigrations
python manage.py migrate
python manage.py parser_pdf (to run the pdf_parser and save the parsed data in the database)
python manage.py runserver (starts the server, make api calls to retrive data)
