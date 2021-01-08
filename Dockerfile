FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update
RUN apt-get install wkhtmltopdf -y
RUN apt-get install cron -y
# install cron job
RUN crontab -l > mycron
#echo new cron into cron file
RUN echo "* * * * *   /usr/src/app/update_bids_docker.sh" >> mycron
#install new cron file
RUN crontab mycron
RUN rm mycron


# COPY . .

EXPOSE 5000

CMD [ "flask", "run", "-h", "0.0.0.0" ]
