# Machine Learning for Housing in Sweden: A Complete Guide from Data Collection to Deployment 

The detailed blog can be found here. 

This project provides valuable insights for users looking to understand the housing market in Sweden and serves as a comprehensive guide for anyone interested in the full spectrum of a ML lifecycle, from data collection to deployment.

The project encompasses several critical steps: data collection, data cleaning, exploratory data analysis (EDA), model building, cloud deployment and CI/CD. 

Before we begin, let's have a look at the [app](https://swedenhomepredict.azurewebsites.net/): 

![sweden](https://github.com/user-attachments/assets/c559ed53-a037-4753-92e0-d805eee446f3)



As you can see, the app enables users to input specific parameters and submit them. Upon submission, it generates and displays a predicted property price based on the provided inputs.


To build this application, here was the process:
- Data Collection
- Data Cleaning + Feature Engineering
- Data Migration to Azure MySQL Database
- Integration of Language Model (LLM) with MySQL Database
- Exploratory Data Analysis (EDA)
- Model Training
- Local + Cloud Deployment
- Continuous Integration (CI)/ Continuous Deployment (CD) pipeline

---
### To run the app locally 
1) Ensure docker is installed 

2) Build the docker image 
```
docker build -t mlapp:1.0 .
```
3) Run a container 
```
docker run -e FLASK_RUN_HOST=0.0.0.0 -e FLASK_RUN_PORT=5000 -p 5000:5000 mlapp:1.0 
```

---
## Repository Structure:

- .github/workflows: CI/CD pipeline configuration
- Jupyter_Notebooks: Contains notebooks for Scraping, EDA, and Modeling
- Text_to_SQL: Integration of Language Model (LLM) with MySQL Database
- static: Front-end files (HTML, CSS, JavaScript)
- .gitignore: Specifies files/folders to ignore when pushing to GitHub
- Dockerfile: Docker configuration file
- Scraper.py: Script for data scraping
- app.py: Main application script
- encoding_dict.pkl: Stores target encoding for the "Municipality" attribute
- metrics.json: Model performance metrics
- model.pkl: Trained model file
- requirements.txt: Dependencies for the training script
- requirements_doc.txt: Dependencies for Docker
- requirements_scrape.txt: Dependencies for the scraping script
- scaler.pkl: Stores numeric scaling for training data
- train.py: Training script
- data.csv: Newly collected data from each scraping round

---

The repository is publicly accessible, so if you have ideas or features to suggest, feel free to fork the repo and submit a pull request. 

Should you encounter any issues while using the application, please report them [here](https://github.com/Siddhesh19991/sweden_property_prediction/issues). 

For questions or feedback about the project, don't hesitate to reach out to me on [LinkedIn](https://www.linkedin.com/in/siddhesh-sreedar/).

---
### LICENSE 

[MIT](https://opensource.org/license/mit) 
