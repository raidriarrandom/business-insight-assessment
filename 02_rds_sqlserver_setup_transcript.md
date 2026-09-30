# RDS SQL Server Setup — Walkthrough (Raw Transcript)

> Raw, unedited transcript of the video tutorial on creating a SQL Server RDS instance and loading the provided CSV files into it. Source of truth — do not treat the summary file as more accurate than this.

**Speaker 1:** Hello all, and welcome to this video tutorial on how to load data into SQL Server, which you will host on RDS in Amazon. So what we're looking at is: we're going to create the RDS database for installing SQL Server. So once you're on the database console, you go ahead and click on "RDS" after searching there, and once that is done, you'll land onto this page.

As you can see, it says 1 out of 20 because I have created an instance previously. So I'll show you how to create an instance as a new one.

So click on "DB Instances," or from here you can click on "Databases." It will take you onto this page where you can see all the databases that you have created previously, and later you can go ahead and click on "Create a database."

Once you do that, we'll go with standard create, and then we will select Microsoft SQL Server because that is what we're going to host. We'll leave it to Amazon RDS, we'll leave it to SQL Server Express Edition.

Now, SQL Server Engine we'll leave by default, the one that it comes with, and then we'll go down and give a name to our database. We can give it any name that you like.

I'm keeping the name as it is. We'll give "Self-managed" one because we want to create the password for our own, so we'll give any password.

Now, once you're there, you need to give a password, and here we'll reset. Scroll down, leave these all settings like as it is; we won't touch it.

We also don't want an EC2 instance right now. Obviously, check for public access because you're going to connect from your local machine to upload the data, the raw data, into the SQL Server table, and then you're going to process the next step for ingestion into S3 using YAML and.

Because you're going to connect to your local machine and upload the data into your SQL Server table. You'll choose the existing VPC that comes with your AWS account by default.

We'll leave it like this. We'll select one of the availability zones.

We don't need any proxy. We don't want SQL Server Windows Authentication.

Scroll down. It's standard one, 7 days of retention, and then scroll down, "Enable enhanced monitoring."

If you want, you can remove this as well. We don't want this.

So your DB installation storage cost is around $34.27 monthly cost, it is showing you. We'll see.

We'll remove these as well. And this is the default one, and VPC can't be changed.

We have storage. We'll keep minimum storage because we are not storing as great data as right now.

We may need on an enterprise level later. I'll go down and check, and your cost is like this.

Click on "Create a database." It'll take some time to create the database.

While I'll show with the one that I have already created, which is already operational. So once this database is created, right, it will take a lot of time, like 10 to 15 minutes.

You go inside this, and you'll be able to see all the details here, like the endpoint and the port. This is what you're going to look at for your new.

And one more thing, you're seeing this VPC security group, right? For the new one that is created, you click on this, you will take it to the security groups page, and from there you're going to click for the security group and check for inbound and outbound notes.

You see how account rules are all traffic, like to the CD SEIDR 0.0.0.0. I have black space, zero.

And then you have the inbound rules also set to all. This might not be set to all because you have allowed public access, so it may point to another security group in here.

So you have to go into editor inbound rules and add a rule like this: all traffic, all, all, custom, zero, zero, and then you must delete the other one and click on "Save rules." I'm not doing anything because the changes are there.

So I'll cancel and go out, and I'll go to the RDS page. By this time, you should be searching for Microsoft SSMS, which is your SQL Server Studio management studio.

And then I'll leave this to be created, but I'll just click on this and delete because I don't need anymore. I just wanted to show you.

And once you search for SSMS on the Google or any other search engine, it will take you to this page. Click on this.

It will show you "Download SSMS," and it will take you in here and click on this particular link. Once you click on this link, you will be taken to your download page, and from there you're able to see this particular setup file.

Once you click on the prompt thing, click on this. This on the Google.

Once you click on the setup file, it will be asked to install. Because I have already installed, so it will not give me "Fresh install," but it will show you installation here and follow the steps to complete it.

Once that is completed, you just search for SSMS, and it will come up.

Once you're here on the SSMS, we'll go and check how we can add the host names, the endpoints, and the ports. So how it is, it will be something like this of this sort.

This won't be filled up, and it will be selected for Windows Authentication. So you have to change it to SQL Server Authentication.

You have to put the exact endpoint name here. Copy it.

Come and then paste here. Like this.

You have to change it to SQL Server Authentication. You have to give your password, master password, and you can also remember password and click on "Trust Server Certificate," encryption optional, and click on "Connect."

Once you click on what happens when you actually get outside of Wispr and try to get in from our local databases.

I'm going to turn the thing in. That might cause problems.

So once that is done, you will be seeing this screen, which is your RDS SQL Server hosted on that. So under databases, you'll see multiple databases, but there is no database for you to create your tables or load the data.

For this time, you'll go and click on "New Query," and then you'll write down "Create database like global," like this, something like this, and select and click on "Execute." It will execute and tell you that the database is created.

All right. How can you view it?

Just refresh this. Click on this, and you'll see "Global Partners" is here.

Under this, you won't have any database right now because you haven't created it. So the easiest way to work on this: we don't need to create tables explicitly.

What we are going to do is we'll right-click on this, we'll click on "Task," and we'll go down and import flat file. Because we are providing you the flat file, the CSV file, you can directly upload the data with the tables getting created and the data is getting added.

Click on "Next" for import flat file. Specify input flat file.

For that, you can click on "Browse," and you can choose one by one. I'll choose one by one.

It says "Date in the table name" and the schema is GPO. That is how SQL Server names it, the schema.

And then you can preview the data. Just verify before you upload if it is correct or not.

And keep it selected. Don't change it.

You have to make sure you're allowing nulls. So for this regular table, "Olyday_name" is going forward.

Click on "Next." It'll show you how it is done, the details.

Click on "Finish." It will start inserting data.

Now click on "Close." So if you see under tables, under tables, you got this table.

So if you want to check, you want to check this particular table, what data it has, so just do global partners.dbo... So if you do this, you'll be able to see all the data in that particular table. Okay, so that is how you load all the other files, and good luck on creating the data pipeline.

Thank you.
