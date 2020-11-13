FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY wkhtmltox_0.12.5-1.bionic_amd64.deb ./
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


# COPY . .

EXPOSE 5000

CMD [ "flask", "run", "-h", "0.0.0.0" ]
