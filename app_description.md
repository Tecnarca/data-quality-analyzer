# Data Quality Analyzer

## Abstract
This document contains a brief description of the main functionalities, the user interface and a mockup of the software that we want to implement. Other features may be added or reworked in the implementation phase, but none will be removed. 

## Domain Problem
We have a large amount of data generated from a data stream of a transport company. In it there are informations regarding each validated ticket, on which bus and on which line.
The goal is to analyze the quality of this dataset and make some analysis on it and comparisons on portions of it.

## Scope
We want to give users the opportunity to analyze these datasets based on their data quality dimensions and to make queries based on dataset attributes. The entire amount of data will be grouped in different datasets per day or week.

Additionaly, since the dataset is almost perfect, it will be "dirtied" in different ways on the different groups in order to analyze more cases of data quality problems.

---

## Functionalities

The user can choose one of the provided dataset he wants to analyze and build a query for it. Upon selecting a dataset, the application will profile it and plot some informations to the user in order to provide a first understanding of what the dataset is about. 

When provided with the query, the application will return the portion of the dataset which respects the requirements, and the user will be able to download it in CSV format. Some of the data will also be printed in order to provide feedback to the user.

In addition, the user will also receive as suggestions other portions of the dataset that perhaps only respect some of the requirements imposed by him and he will be able to decide whether to download even those or not. 

We also give the user the opportunity to see further details regarding each portion of the dataset obtained from the query (a sort of profiling) before downloading it.

The user can also compare two dataset using the profiling informations or compare two sections of them based on a query of his choice when possible.

##### Profiling Requirements
Upon selecting a dataset, the application will show metadata about each column, including:
- The type (categorical, numerical, datetime etc.)
- The number and percentage of missing values
- The number and percentage of distinct values
- A plot of the values (when possible)

And other information about the dataset itself, including:
- Simple metadata of the dataset (number of variables, size in memory, number of tuples, duplicate rows etc.)
- Mean and standard deviation of the completeness, timeliness and consistency
- Matrix plot of the missing values
- A random sample of the data

##### Query Requirements
- `Completeness > value`: the user can search for data that has a completeness greater than the `value` entered
- `Consistency > value`: the user can search for data that has a consistency greater than the `value` entered
- `Timeliness > value`: the user can search for data that has a timeliness greater than the `value` entered
- `Group by attributes`: the user can group the data based on a selected `attributes`
- `attributes: value`: the user can search for data that has a certain `value` for the `attributes` chosen
  
All queries can be freely combined with each other.

##### Compare Requirements
- The profiling information will be visible for both selected datasets
- The user can perform a query to show the profiling of a portion of the datasets
- The stats of the dataset with higher quality will be highlited in some way (either by color or direct comparison)

##### Other Functionalities
- **Download**: the user can download the portion of the data received from the query
- **More Details**: the user can view a profiling of the portion of the data received from the query
- **Suggest more**: the system suggests to the user portions of data that respect only some of the entered requirements

---

## Mock-up interface
Here we will present a quick and little mock-up interface of what the software will look like. The final software may have additional features.
We also do not show the profiling interface because we do not already have an exact idea of what it will look like (it depends on how we will be dirting the datasets).

**Query interface**:
![QUERY](https://i.ibb.co/DrD9BBr/Query.jpg)

**Compare interface**:
![COMPARE](https://i.ibb.co/92vc8sX/Compare.jpg)

## Software dependecies
We intend to implement this software using `python 3.7`[^1] in order to have the handling of the datasets (with `pandas`[^2], `matplotlib`[^3], `dask`[^4] and similar libraries) and the web interface (with `flask`[^5] or `bottle`[^6]) under the same language. This eases the construction of the software and reduces its complexity (including memory and ram consumption). It can also easily be hosted on some cloud computing platforms like `AWS EC2`[^7] if needed.

If the application will be lightweight enough, it can be hosted on `github pages`[^8].

---

#### Students
**Febbo Leonardo** - <leonardo.febbo@mail.polimi.it>
**Astolfi Giacomo** - <giacomo.astolfi@mail.polimi.it>

[^1]: <https://www.python.org/>
[^2]: <https://pandas.pydata.org/>
[^3]: <https://matplotlib.org/>
[^4]: <https://dask.org/>
[^5]: <http://flask.pocoo.org/>
[^6]: <https://bottlepy.org/docs/dev/>
[^7]: <https://aws.amazon.com/it/ec2/>
[^8]: <https://pages.github.com/>
