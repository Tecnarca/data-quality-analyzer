import numpy as np
import pandas as pd
import spark_df_profiling
from flask import Flask
from flask import render_template
from flask import request
from pyspark import SparkContext, SparkConf
from flask import send_file
from pyspark.sql import SparkSession
import glob
import json

spark = SparkSession \
    .builder \
    .appName("pySpark Quality Analyzer") \
    .getOrCreate()

print("------------------------------")
print("[Start] Loaded Spark")

path ='./Dati/'
csvs = glob.glob(path + "/*.csv")
df = []
p=[]
print("[Start] Loading and profiling Spark data frames...")
for file_ in csvs:
	s_df = spark.read.csv(file_,header = True)
	df.append(s_df)
	p.append(spark_df_profiling.ProfileReport(s_df).rendered_html())
print("[Start] Loaded and profiled Spark data frames")

print("[Start] Starting Flask...")
app = Flask(__name__)
print("[Start] Started Flask")

print("------------------------------")

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
		for idx, dfc in enumerate(df):
			if request.form.get('d'+str(idx)) is not None:
				c.append(idx)
		if len(c)!=1:
			return "ERROR: You must select 1 day to query"
		df[c[0]].createOrReplaceTempView("PEOPLE")		
		if request.form.get('form2') is not None:
			if request.form.get('query') is not None:
				sqlDF = spark.sql(request.form.get('query'))
				profile = spark_df_profiling.ProfileReport(sqlDF).rendered_html(False)
				pdf = sqlDF.toPandas().head(20).to_html()
				return render_template('query.html', report=profile, dfs=df, attrs=df[0].columns, pdf=pdf, query=request.form.get('query'), day=c[0])
			else:
				return "ERROR: Query cannot be empty"
		elif request.form.get('form1') is not None:
			query = "SELECT "
			for attr in df[0].columns:
				if  request.form.get('s'+attr) is not None:
					query = query + attr + ','
			query = query[:-1] + " FROM PEOPLE WHERE "
			for attr in df[0].columns:
				if request.form.get('w'+attr) is not "":
					query = query + attr + '=' + request.form.get('w'+attr) + " AND "
			if query[-6] == "WHERE ":
				query = query[:-6]
			else:
				query = query[:-4]
			query = query + "GROUP BY "
			for attr in df[0].columns:
				if request.form.get('g'+attr) is not None:
					query = query + attr + ','
			if query[-9] == "GROUP BY ":
				query = query[:-9]
			else:
				query = query[:-1] + " HAVING count("
				for attr in df[0].columns:
					if request.form.get('h'+attr) is not None:
						query = query + attr + ','
				if query[-6] == 'count(':
					query = query[:-14]
				else:
					query = query[:-1]+')'
					if request.form.get('min') is not None:
						query = query + '<'
					elif request.form.get('max') is not None:
						query = query + '>'
					elif request.form.get('eq') is not None:
						query = query + '='
					else:
						return "ERROR building the query"
					if request.form.get('count') is not None:
						query = query + request.form.get('count')
					else:
						return "ERROR building the query"
			print(query)
			sqlDF = spark.sql(query)
			profile = spark_df_profiling.ProfileReport(sqlDF).rendered_html(False)
			pdf = sqlDF.toPandas().head(20).to_html()
			return render_template('query.html', report=profile, dfs=df, attrs=df[0].columns, pdf=pdf, query=query, day=c[0])
		else:
			return "Valid form not received"
	else:
		return render_template('query.html', dfs=df, attrs=df[0].columns)

@app.route('/download', methods=['POST'])
def download():
	df[int(request.form.get('day'))].createOrReplaceTempView("PEOPLE")
	sqlDF = spark.sql(request.form.get('query'))
	sqlDF.toPandas().to_csv('/tmp/out.csv', encoding='utf-8')
	return send_file('/tmp/out.csv', as_attachment=True, attachment_filename='Dataset.csv')

if __name__ == '__main__':
    app.run()