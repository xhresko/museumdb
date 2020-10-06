FROM python:3.8
WORKDIR /notebooks
COPY requirements.txt /notebooks/
RUN pip install -r requirements.txt
COPY ./src/ /notebooks/
CMD jupyter notebook --ip=0.0.0.0 --port=8585 --allow-root
