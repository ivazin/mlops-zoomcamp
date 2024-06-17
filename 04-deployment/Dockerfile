FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

WORKDIR /app

RUN pip install -U pip
RUN pip install pipenv

# COPY Pipfile* /app/
# COPY Pipfile* ./

RUN pipenv install "scikit-learn==1.5.0" "pandas" "pyarrow"
RUN pipenv install --system --deploy

COPY main.py ./

# ENTRYPOINT [ "python", "main.py" ]
CMD [ "python", "main.py" ]