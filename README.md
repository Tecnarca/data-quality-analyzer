# Data Quality Analyzer

This program aim is to show how it is possible to analyze the quality of a [provided datasets](https://github.com/Tecnarca/data-quality-analyzer/tree/master/Orginal-Data) and make some preliminary analysis and comparisons on chunks of data, in order to prepare the data for data mining tasks.

We were provided with an almost perfect dataset (no missing values, no duplicated rows etc.) so we had to dirty it a little bit before feeding it to the web application for the analysis. 

See:
- [Project presentation](https://github.com/Tecnarca/data-quality-analyzer/blob/master/presentation.pdf)
- [Data quality Profiler webapp](https://github.com/Tecnarca/data-quality-analyzer/blob/master/webapp.py)
- [Data quality check](https://github.com/Tecnarca/data-quality-analyzer/blob/master/Orginal-Data/File%20Conversion.ipynb)

## Usage

To see how we dirtyied our datasets and how we created the quality attributes, run this notebook:
```
jupyter notebook Orginal-Data/File\ Conversion.ipynb 
```

To start the webapp that contains the Data Quality Analyzer, simply run: 
```
python webapp.py
```
Note: This command will also start a flask server on port 5000. To access it, open on your browser the page:
```
http://localhost:5000/query
```

## Built with
* [Java 9](https://www.oracle.com/java/java9.html)
* [Python 3.7](https://www.python.org/downloads/release/python-374/)
* [PySpark](https://spark.apache.org/docs/2.2.0/api/python/pyspark.html)
* [Pandas](https://pandas.pydata.org/)
* [Jupyter](https://jupyter.org/)
* [Bootstrap 3.6.6](http://bootstrapdocs.com/v3.3.6/docs/)
* [Spark DF profiler](https://github.com/julioasotodv/spark-df-profiling)
---
***Students Giacomo Astolfi, Leonardo Febbo. Project for the course on 'Data and Information Quality' held at Politecnico di Milano by Prof. Cinzia Cappiello, A.Y. 2018/2019***
