# download and use an existing image which already has Conda installed and set up
FROM continuumio/miniconda3

# Dumb init minimal init system intended to be used in Linux containers
RUN wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.0/dumb-init_1.2.0_amd64
RUN chmod +x /usr/local/bin/dumb-init

# Because miniconda3 image releases may sometimes be behind we need to play catchup manually
RUN conda update conda && conda install "conda=4.8.2"

ENV CONDA_ENV_NAME conda-env



# Lets get the environment up to date
RUN apt-get update && apt-get install -y --no-install-recommends

RUN mkdir /app
WORKDIR /app

# Add current directory code to working directory
ADD . /app/

COPY environment.yml .
# Now we want to activate a Conda environment which has the necessary Python version installed and has all the libraries installed required to run our app
RUN conda env create -n mebsutaenv -f environment.yml
RUN echo "source activate mebsutaenv" > /etc/bashrc
ENV PATH=/opt/conda/envs/mebsutaenv/bin:$PATH


# Temporary measure add GAMS to LINUX PATH below, this will break if GAMS version is upgraded, this is an intrim solution
# To be removed once python package is updated with sed logic append new libs to bashrc file global path

ENV PORT=8888   
EXPOSE 8888
#CMD ["python", "/app/manage.py", "runserver", "0.0.0.0:8888"]
CMD gunicorn mebsuta-django.wsgi:application --bind 0.0.0.0:$PORT