import numpy as np
import pandas as pd
import spark_df_profiling
from flask import Flask
from flask import render_template
from flask import request
from pyspark.sql.types import StructField,IntegerType, StructType,StringType
from pyspark import SparkContext, SparkConf
from flask import send_file
from pyspark.sql import SparkSession
import glob
import re

spark = SparkSession \
    .builder \
    .appName("Data Quality Analyzer") \
    .getOrCreate()

print("------------------------------")
print("[Start] Loaded Spark")

path ='./Dirty-Data/'
csvs = glob.glob(path + "/*.csv")
df = []
p=[]
print("[Start] Loading and profiling Spark data frames...")
dfS=[StructField('CODLINHA',StringType(),True),
       StructField('NOMELINHA',StringType(),True),
       StructField('CODVEICULO',StringType(),True),
       StructField('NUMEROCARTAO',StringType(),True),
       StructField('DATAUTILIZACAO',StringType(),True),
       StructField('COMPLETENESS',IntegerType(),True),
       StructField('CONSISTENCY',IntegerType(),True),
       StructField('CONFORMITY',IntegerType(),True)
       ]
dfStruct=StructType(fields=dfS)
for file_ in csvs:
	s_df = spark.read.csv(file_,header = True,schema=dfStruct)
	df.append(s_df)
	p.append(spark_df_profiling.ProfileReport(s_df).rendered_html())
print("[Start] Loaded and profiled Spark data frames")

print("[Start] Starting Flask...")
app = Flask(__name__)
print("[Start] Started Flask")

print("------------------------------")

def qualityAttrs(query):
	suggested = []
	if re.search("(WHERE)*COMPLETENESS[ *]*>?[ *]*=[ *]*", query):
		suggested.append("COMPLETENESS")
	if re.search("(WHERE)*CONSISTENCY[ *]*>?[ *]*=[ *]*", query):
		suggested.append("CONSISTENCY")
	if re.search("(WHERE)*CONFORMITY[ *]*>?[ *]*=[ *]*", query):
		suggested.append("CONFORMITY")
	return suggested

def leaveQuality(query, dimension):
	dims = ["COMPLETENESS", "CONSISTENCY", "CONFORMITY"]
	dims.remove(dimension)		
	query = re.sub("(AND[ *]*)?("+dims[0]+"|"+dims[1]+")[ *]*>[ *]*=[ *]*[0-9]+([ *]*(AND))?", "", query)
	return query	

@app.route('/compare', methods=['GET', 'POST'])
def compare():
	if request.method == 'POST':
		c=[]
		for idx, dfc in enumerate(df):
			if request.form.get('d'+str(idx)) is not None:
				c.append(idx)
		if len(c)!=2:
			return "ERROR: You must select 2 days to compare"
		reports = {"profile1": p[c[0]], "profile2": p[c[1]]}
		return render_template('compare.html', reports=reports, dfs=df)
	else:
		return render_template('compare.html', dfs=df)

@app.route('/', methods=['GET', 'POST'])
@app.route('/query', methods=['GET', 'POST'])
def query():
	if request.method == 'POST':
		c=[]
		suggested=[]
		for idx, dfc in enumerate(df):
			if request.form.get('d') == str(idx):
				c.append(idx)
		if len(c)!=1:
			return "ERROR: You must select 1 day to query"
		df[c[0]].createOrReplaceTempView("PEOPLE")		
		if request.form.get('query') is not "":
			sqlDF = spark.sql(request.form.get('query'))
			pdf = sqlDF.toPandas().head(20).to_html(classes='table')
			suggested = qualityAttrs(request.form.get('query'))
			if len(suggested) > 1:
				return render_template('query.html', dfs=df, attrs=df[0].columns, pdf=pdf, query=request.form.get('query'), day=c[0], suggested=suggested)
			else:
				return render_template('query.html', dfs=df, attrs=df[0].columns, pdf=pdf, query=request.form.get('query'), day=c[0])
		else:
			query = "SELECT "
			for attr in df[0].columns:
				if  request.form.get('s'+attr) is not None:
					query = query + attr + ','
			query = query[:-1] + " FROM PEOPLE WHERE "
			for attr in df[0].columns:
				if request.form.get('w'+attr) is not "":
					char = '='
					if attr in ['COMPLETENESS', 'CONSISTENCY', 'CONFORMITY']:
						char = '>='
						suggested.append(attr)
					query = query + attr + char + request.form.get('w'+attr) + " AND "
			if query[-6:] == "WHERE ":
				query = query[:-6]
			else:
				query = query[:-4]
			query = query + "GROUP BY "
			for attr in df[0].columns:
				if request.form.get('g'+attr) is not None:
					query = query + attr + ','
			if query[-9:] == "GROUP BY ":
				query = query[:-9]
			else:
				query = query[:-1] + " HAVING count("
				for attr in df[0].columns:
					if request.form.get('h'+attr) is not None:
						query = query + attr + ','
				if query[-6:] == 'count(':
					query = query[:-14]
				else:
					query = query[:-1]+')'
					if request.form.get('op') is not None:
						query = query + request.form.get('op')
					else:
						print("Error on query: " + query)
						return "ERROR building the query: max min or eq must be non null when attrs to count are selected. <br/> Query:" + query
					if request.form.get('count') is not None:
						query = query + request.form.get('count')
					else:
						print("Error on query: " + query)
						return "ERROR building the query: " + query
			print(query)
			sqlDF = spark.sql(query)
			pdf = sqlDF.toPandas().head(20).to_html(classes='table')
			if len(suggested) > 1:
				return render_template('query.html', dfs=df, attrs=df[0].columns, pdf=pdf, query=query, day=c[0], suggested=suggested)
			else:
				return render_template('query.html', dfs=df, attrs=df[0].columns, pdf=pdf, query=query, day=c[0])
	else:
		return render_template('query.html', dfs=df, attrs=df[0].columns)

@app.route('/download', methods=['POST'])
def download():
	df[int(request.form.get('day'))].createOrReplaceTempView("PEOPLE")
	sqlDF = spark.sql(request.form.get('query'))
	sqlDF.toPandas().to_csv('/tmp/out.csv', encoding='utf-8')
	return send_file('/tmp/out.csv', as_attachment=True, attachment_filename='Dataset.csv')

@app.route('/profileQuery', methods=['POST'])
def profileQuery():
	df[int(request.form.get('day'))].createOrReplaceTempView("PEOPLE")
	sqlDF = spark.sql(request.form.get('query'))
	if  len(sqlDF.head(1)) > 0:
		profile = spark_df_profiling.ProfileReport(sqlDF).rendered_html(False)
		return profile
	else:
		return "Can't profile empty dataset"

@app.route('/trySuggestion', methods=['POST'])
def trySuggestion():
	df[int(request.form.get('day'))].createOrReplaceTempView("PEOPLE")
	queryN = leaveQuality(request.form.get('query'),request.form.get('dimension'))
	sqlDF = spark.sql(queryN)
	if  len(sqlDF.head(1)) > 0:
		profile = spark_df_profiling.ProfileReport(sqlDF).rendered_html(False)
		return render_template('suggested.html', queryN=queryN, profile=profile)
	else:
		return "The query did not return any rows."
if __name__ == '__main__':
    app.run()