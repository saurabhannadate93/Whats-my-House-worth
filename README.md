# Property-Valuation-Estimation

## Project Charter

### Vision
It is often expensive, and sometimes impossible for a real estate company/agency to send down someone to inspect a property to determine its intrinsic value. Our vision is to develop a platform which would help estimate the true value of a property based on certain property characteristics to help drive investment decisions and reduce costs.


### Mission
The mission is to build an algorithm which would help accurately predict the intrinsic value of a property based on certain characteristics like property type, no. of floors, age etc. and develop a user interface to administer the solution.

### Success Criteria

**Model Criterion**: Our model is successful if the R-square evaluation metric exceeds 60%. 

**Desired Business Outcomes**: A long term indication of the model's impact on the business would be a simultaneous reduction in the operating costs by the virtue of the reduced requirement for personnel to visit the properties in person while maintaining or improving the percentage of bad investment decisions.  

## Project Plan

### Theme: Develop and deploy a platform that helps estimate the valuation of a property based on certain characteristics. 

1. __EPIC 1: Model Building and Optimization__
    * Data Cleaning and missing value imputation
    * Feature Generation
    * Exploratory Data Analysis
    * Testing different model architectures and parameter tuning
    * Model performance tests
   
2. __EPIC 2: Model Deployment Pipeline Development__
    * Set up S3 instance
    * Initialize RDS database
    * Deploy model using Flask
    * Development of unit tests and integrated tests
    * Setup usage logs
    * Solution reproducibility tests
    
3. __EPIC 3: User Interface Development__
    * Develop a basic form to input data and output results
    * Add styling/colors to make the interface more visually appealing  

## Backlog
* EPIC 1 : Data Cleaning and missing value imputation (2) : Sprint 1
* EPIC 1 : Feature Generation (2) : Sprint 1
* EPIC 1 : Exploratory Data Analysis (4) : Sprint 1
* EPIC 1 : Testing different model architectures and parameter tuning (8) : Sprint 1
* EPIC 1 : Model performance tests (2) : Sprint 1
* EPIC 2 : Set up a S3 instance (1)
* EPIC 3 : Develop a basic form to input data and output results (4)

## IceBox 
* EPIC 3 : Add styling/colors to make the interface more visually appealing
* EPIC 2 : Initialize RDS database
* EPIC 2 : Deploy model using Flask
* EPIC 2 : Development of unit tests and integrated tests
* EPIC 2 : Setup usage logs
* EPIC 2 : Solution reproducibility tests

