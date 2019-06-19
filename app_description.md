# Data Quality Analyzer

## Abstract
What we will discuss in this document, who we are, why are we doing this.
(our mails and names go here too)

This document represents a brief description of the main functionalities, the user interface and software used for the project.

## Domain Problem
Brief description of the problem we must solve.

We have a large amount of data (grouped by days or weeks) generated from a data stream of a transport company. 
In it there are informations regarding each ticket validated, on which bus and on which line.


## Scope
What dataset we'll analyze, why and how

We want to give users the opportunity to analyze datasets based on data quality dimensions and to make queries based on dataset attributes.

The entire amount of data will be grouped in different datasets per day or week and will be "dirtyed" in different ways to be able to analyze more cases of data quality problem.

The user can choose the dataset he wants to analyze and compile the query to be done. At the end of the query the user will receive the portion of the dataset, which respects the requirements imposed by him, and will be able to download it.
In addition to this portion of the dataset, the user will also receive as suggestions other portions of the dataset that perhaps only respect some of the requirements imposed by him and he will be able to decide whether to download even those or not.
We also give the user the opportunity to see further details regarding each portion of the dataset obtained from the query (a sort of profiling) before downloading it.


## Functionalities

#### Core Functionalities
What the application will perform, 

*Query Requirements*:
  - **Completeness>[value]** : the user can search for data that has a completeness greater than the [value] entered
  - **Consistency>[value]** : the user can search for data that has a consistency greater than the [value] entered
  - **Timeness>[value]** : the user can search for data that has a timeness greater than the [value] entered
  - **[Attribute]:[value]** : the user can search for data that has a certain [value] for the [attribute] chosen
  - **Group by [Attribute]** : the user can group the data based on a selected [attribute]
  
N.B. all queries can be combined each other

*Other Functionalities*:
  - **Download** : the user can download the portion of the data received from the query
  - **More Details** : the user can view a profiling of the portion of the data received from the query
  - **Suggest more** : the system also suggests to the user portions of data that respect only some of the requirements entered by him.

#### Mock-up interface
Image and description of the interface (local web interface)

#### Software dependecies
What software are we going to use in order to implement the application

## Other aspects
If we need to write something specifical but unrelated to the app
(maybe the link to the github repo? but now it is private)

---
Syntax di markdown utile:
**Grassetto**

*corsivo*

> quote in a gray box
> another line in the gray box

1. Ordered
2. List

- Lista (non ordinata)
- quella con i
- pallini neri

![Titolo dell'immagine](/url/della/immagine/caricala/su/github/)

`testo in monospazio, come su telegram`

`uuuh molto carino`

Dopo di qui c'è una linea separatrice
---
E questa è la riga immediatamente dopo

[Hyperlink al mio sito preferito](http://link.al/sito)

Se invece vuoi mostrare l'url per intero o una mail: <fake@example.com>

Invece qua metto una referenza[^1] a piè pagina

| Volendo  | Possiamo   |
| -------- | ------     |
|Fare      | le tabelle |
|Le pipes non devono | essere necessariamente allineate, obv |
|Guarda | tu |
|questo | che |
|crede | di |
|avere | a |
|che |fare |
|con | uno |
|sprovveduto | gne gne|
|ahaha | ihihihi |

[^1]: in stile wikipedia
