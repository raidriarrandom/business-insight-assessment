# Business Insight Assessment — Requirements Walkthrough (Raw Transcript)

> Raw, unedited transcript of the assessment requirements video. Source of truth — do not treat the summary file as more accurate than this.

**Them:** Hello all, and welcome to this short descriptive video on business insight assessment.

**Them:** And how to proceed on that. So, in this case, we are going to build a data engineering pipeline which will be driven by some CSV files or the orders files on order-related files that we have provided you guys with, and there is a step-by-step plan to work on this entire assessment.

**Them:** So firstly, the files will be available on Google Drive; the link will be shared with you. And to proceed with the starting step is to get the files downloaded, and the structures of the files are as shown on the screen.

**Them:** So if you look at the actual files, you will be able to see if there are any problems with the files, some integrity issues, some other data issues you need to consider that I need to find and report it. Next is analyze the CSV files to understand how you are going to create the schema design or the RD diagram in short, and then it has to be done entirely manually, no automated process is needed for that.

**Them:** Next is defining a data engineering pipeline or architecture to complete this entire assessment. So in this case, you are required to present a business insight for a particular order orders data orders and orders-related data, and for that you have to create the entire pipeline starting from

**You:** Hi, Holly.

**Them:** ingestion, then transformation, then business insights metrics calculation, and then you have to build a dashboard. Out of it, with some given instructions.

**Them:** So while you are doing this, we are considering SQL servers to be our main database or the source database from which you are going to ingest the data. And

**You:** Hey.

**Them:** the entire thing has to be done in AWS or using AWS resources. We cannot use any Snowflake, DBT, or any other external tools.

**Them:** The transformations, the ETL transformations has to be done using PySpark. You may choose your own resources of your choice, and then you can proceed with that.

**Them:** The entire pipeline has to be processed daily once as a batch process, and it to do this scheduling part of this particular assessment as well. So when you are talking about the approach, you have to first calculate the customer lifetime value, that is the mean.

**Them:** The primary metric. First calculate the customer lifetime value, that is the mean or the primary metric that we need to achieve, and then we are going to calculate the additional business insights metric.

**Them:** Metrics.

**Them:** As we can see, down below.

**Them:** Architectural design has to be as certified by the subject matter expert, and post-approval you are going to create the pipeline. So you have to give us with the pipeline architectural diagram, the explanation, how did you reach to the conclusion of using a certain architecture, you have to create a solution design document, you have to get a written approval from the SME, and then eventually you can use

**Them:** .io and other drawing tools to showcase the designs. Now the primary metric is around customer lifetime value.

**Them:** In this case we have defined a goal and.

**Them:** Why we need that and how to do it proceeding with that. For each metrics that you see on the screen, you are given certain background around why do we need that, and also how to proceed with getting that particular metric calculated.

**Them:** So there are churn indicators, customer segmentation, and behavior, sales trends, monitoring, loyalty program impact, top performing locations, pricing and discount effectiveness, and finally the entire thing has to be produced as a dashboard on Streamlit that we have decided, and you guys need to create dashboards for specific metrics as given below under deliverable, like customer segmentation dashboard, there is a question, and you need to focus on a certain metric and objective in that. So churn risk indicator dashboard, sales trend, loyalty program location, performance dashboard, pricing, discount, and effectiveness dashboard, and finally after all these things are done, you have to submit us with the pipeline documentation, the code files, the ETL scripts, the Spark scripts, SQL queries, that you are going to use, set a configurations if any.

**Them:** Shown on the screen. So if you look at the actual files.

**Them:** Like you have to define a CSV. Loyalty program location, performance dashboard, pricing, discount, and effectiveness dashboard, and finally after all these things are done, you have to submit us with the pipeline documentation, the code files, the ETL scripts, the Spark scripts, SQL queries, that you are going to use, set a configurations if any you have used, the final dashboard with all the listed dashboards that we have segregated, and you have to create this entire architectural performing under CI/CD pipeline architecture as well, like you have to define a CI/CD pipeline for the entire code and the configurations to be stored and to be performing as a real-world project.

**Them:** As it behaves. So in that case you will also learn about how to proceed with CI/CD pipelines, the coding architectures, and how to maintain your code for a production-level deployment.

**Them:** And lastly, you have to clearly mention what document is for what purpose with a clear naming convention, and you have to present explaining the work that you have done, and finally you have to also briefly explain about why did you choose a particular architecture to solve this business insights assessment. So the entire process has been defined clearly on this.

**Them:** Particular document, there are small hyperlinks as well. You will see there is a small hyperlink for the installation video and the SQL data loader video, under.

**Them:** the hyperlink for Windows operating system, there is Azure Data Studio or Azure Studio for the macOS users, for installing a similar client to what Microsoft SSMS SQL Server Management Studio.

**Them:** And there is one more descriptive video link for the Streamlit dashboard under building dashboards using Streamlit. So.

**Them:** Hope you guys have a wonderful assessment and see you soon. Good luck.
