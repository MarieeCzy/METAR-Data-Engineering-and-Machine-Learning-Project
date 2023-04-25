![Progress](https://camo.githubusercontent.com/46884dbe2b094a29e9fa03bed9985b0710df347f39dad448fd0799138b109eea/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374617475732d576f726b5f696e5f70726f67726573732d79656c6c6f77)
![Stage1](https://img.shields.io/badge/Phase1-completed-green)

<h1 align="center">🌦️ METAR Data Engineering and Machine Learning Project 🛫</h1>

<p align="center">
  <a href="#technologies">Technologies</a> •
  <a href="#about-the-project">About the project</a> •
  <a href="#conceptual-architecture">Conceptual architecture</a> •
  <a href="#👉-phase-1">Phase 1</a> •
  <a href="#👉-phase-2">Phase 2</a> •
  <a href="#👉-phase-3-final-stage">Phase 3 - Final Stage</a> •
  <a href="#data-source">Data source</a> 
</p>

---

## Technologies

 ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
 ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
 ![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)
 ![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)

- [Dataproc](https://cloud.google.com/dataproc)
- [Apache Spark](https://spark.apache.org/)
- [PySpark](https://spark.apache.org/docs/latest/api/python/)
- [Streamlit](https://streamlit.io/)

---

## About the project

An educational project to build an end-to-end pipline for near real-time and batch processing of data further used for visualisation 👀 and a machine learning model 🧠.

The project is designed to enable the preparation of an analytical summary of the variability of METAR weather reports over the years for airports of European countries. 

Read more about METAR here ➡️ [METAR](https://www.dronepilotgroundschool.com/reading-aviation-routine-weather-metar-report/)

In addition, the aim is to prepare a web application using the Streamlit library and machine learning algorithms to predict the trend of change of upcoming METAR reports.

---

## Conceptual architecture

![view1][Conceptual]

---

The project is divided into 3 phases according to the attached diagrams:

## 👉 Phase 1

Retrieval of archive data from source. Initial transformation.
Transfer of data to Data Lake - Google Cloud Storage. Transfer of data to Data Warehouse. Transformations using data build tools. Visualisation of aggregated data on an interactive dashboard in Looker.

![view2][Milestone_1_platform]

---

## 👉 Phase 2

Preparing the environment for near-real-time data retrieval. 
Transformations of archived and live data using PySpark, preparation of data for machine learning model. 
Training and tuning stage of the model.

![view3][Milestone_2_platform]

---

## 👉 Phase 3 - Final stage 🥳

Collection of analytical reports for historical data, preparation of web dashboard with the ability to display the prediction of the nearest METAR report for a given airport and the likely trend of change.

![view4][Final_platform]

---

## Data source

💿 [IOWA STATE UNIVERSITY ASOS-AWOS-METAR Data](https://mesonet.agron.iastate.edu/request/download.phtml?network=PL__ASOS)

---

## 📊 Looker report

The report generated in Looker provides averages of METAR data, broken down by temperature, winds, directions, and weather phenomena, with accompanying charts. The data was scraped via URL and stored in raw form in Cloud Storage. PySpark and Dataproc were then used to prepare SQL tables with aggregation functions, which were saved in BigQuery. The Looker report directly utilizes these tables from BigQuery.

Additionally, it's possible to prepare a similar report for other networks. 
Below is an example for PL__ASOS. 

Check: [PL__ASOS](https://lookerstudio.google.com/reporting/ef5cab41-deeb-498e-95de-c29cf52a3fe6)

For more information, please refer to the <b>"How to contribute"</b> section.

![view5][Looker_report]


<!-- MARKDOWN LINKS & IMAGES -->
[Conceptual]: docs/images/Conceptual.jpg
[Final_platform]: docs/images/Final_platform.jpg
[Milestone_1_platform]: docs/images/Milestone_1_platform.jpg
[Milestone_2_platform]: docs/images/Milestone_2_platform.jpg
[Looker_report]: docs/report/Looker_report.jpg

