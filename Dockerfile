FROM python:3

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "loremricksum.py" ]
