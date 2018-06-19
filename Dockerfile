FROM python:3

ADD . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "loremricksum.py" ]
