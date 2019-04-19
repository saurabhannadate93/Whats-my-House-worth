# Property-Valuation-Estimation

Project owner: Saurabh Annadate
QA: Tanya Tandon 

## Project Charter

### Vision
Real estate agencies require accurate estimation of the intrinsic value of a property to decide whether it is undervalued or not before making an investment decision. It is often expensive, and sometimes impossible to send down someone to inspect a property to do the same. Our vision is to develop a platform which would help estimate the true value of a property based on certain property characteristics to help drive investment decisions, increase profits and reduce costs.


### Mission
The mission is to build an algorithm which would help accurately predict the intrinsic value of a property based on certain characteristics like property type, no. of floors, age etc. and develop a user interface to administer the solution so that real estate agents can use it to estimate the intrinsic value of a property.

### Success Criteria

**Model Criterion**: Our model is successful if the R-square evaluation metric exceeds 60%. 

**Desired Business Outcomes**: A long term indication of the model's impact on the business would be a simultaneous reduction in the operating costs by the virtue of the reduced requirement for personnel to visit the properties in person while reducing the percentage of bad investment decisions.  

## Project Plan

### Theme: Develop and deploy a platform that helps estimate the valuation of a property based on certain characteristics. 

1. __EPIC 1: Model Building and Optimization__
    * Story 1 : Data Cleaning and missing value imputation
    * Story 2 : Feature Generation
    * Story 3 : Exploratory Data Analysis
    * Story 4 : Testing different model architectures and parameter tuning
    * Story 5 : Model performance tests to check the model run times
   
2. __EPIC 2: Model Deployment Pipeline Development__
    * Story 1 : Environment Setup : requirement.txt files
    * Story 2 : Set up S3 instance
    * Story 3 : Initialize RDS database
    * Story 4 : Deploy model using Flask
    * Story 5 : Development of unit tests and integrated tests
    * Story 6 : Setup usage logs
    * Story 7 : Solution reproducibility tests
    
3. __EPIC 3: User Interface Development__
    * Story 1 : Develop a basic form to input data and output results
    * Story 2 : Add styling/colors to make the interface more visually appealing  

## Backlog

Sprint Sizing Legend:

* 0 points - quick chore
* 1 point ~ 1 hour (small)
* 2 points ~ 1/2 day (medium)
* 4 points ~ 1 day (large)
* 8 points - big and needs to be broken down more when it comes to execution (okay as placeholder for future work though)
------------------
* EPIC 1 : Story 1 : Data Cleaning and missing value imputation (2) : Sprint 1
* EPIC 1 : Story 2 : Feature Generation (2) : Sprint 1
* EPIC 1 : Story 3 : Exploratory Data Analysis (4) : Sprint 1
* EPIC 1 : Story 4 : Testing different model architectures and parameter tuning (8) : Sprint 1
* EPIC 1 : Story 5 : Model performance tests (2) : Sprint 1
* EPIC 2 : Story 1 : Environment Setup : requirement.txt files
* EPIC 2 : Story 2 : Set up a S3 instance
* EPIC 2 : Story 3 : Initialize RDS database
* EPIC 2 : Story 4 : Deploy model using Flask
* EPIC 2 : Story 5 : Development of unit tests and integrated tests
* EPIC 3 : Story 1 : Develop a basic form to input data and output results
* EPIC 2 : Story 6 : Setup usage logs
* EPIC 2 : Story 7 : Solution reproducibility tests

## IceBox 
* EPIC 3 : Story 2 : Add styling/colors to make the interface more visually appealing


