FROM jupyter/datascience-notebook
WORKDIR /notebooks
COPY . /notebooks/
RUN pip install mysql-connector-python SQLAlchemy plotly seaborn
CMD jupyter notebook --ip=* --port=8585
