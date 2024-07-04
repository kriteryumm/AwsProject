# AWS QR based feedback system 
Our objective in this project is to increase tenant satisfaction and operational efficiency
by using Amazon Web Services (AWS) and Quick Response (QR) codes.

Our endeavor revolves around implementing a feedback mechanism accessible by QR
codes that exists in various amenities within a residential building, such as trash bins, elevators,
storage rooms and so on. These QR codes are used as gateways to connect tenants to our
feedback platform.

This feedback process begins with tenants scanning the QR code with the amenity they
wish to give feedback on. After scanning, they are redirected to a web interface, urging them to
register themselves then log in. Registration requires a unique user name and a password which
is stored in MySQL database.

## Homepage and Loginpage

![homepage](https://github.com/kriteryumm/Aws_QR_Based_Feedback_System/assets/61352431/ef52e580-18b7-4d91-bfe4-e3ac45ce3a94)


![loginpage](https://github.com/kriteryumm/Aws_QR_Based_Feedback_System/assets/61352431/d6692430-0d30-4c51-8d44-8de9267d082d)


Once authenticated, tenants can access the feedback submission form. This feedback then
is forwarded to the administrator.
### Feedback Submission Process
1. Scanning the QR Code: Tenants scan the QR code on the specific amenity they wish to give
feedback on.
2. Redirect to Web Interface: The QR code redirects the tenant to a web interface where they are
prompted to register or log in.
3. Feedback Form Access: Upon successful authentication, tenants can access the feedback
submission form tailored to the specific amenity.
4. Form Submission: Tenants fill out the feedback form, which includes fields for rating, comments,
and suggestions.

## User Experience Design

![QrUploadpage](https://github.com/kriteryumm/Aws_QR_Based_Feedback_System/assets/61352431/a4e1667a-71cc-4c12-a2ca-681c7e004356)

![enterFeedback](https://github.com/kriteryumm/Aws_QR_Based_Feedback_System/assets/61352431/19a58c7a-8a79-42f7-a1af-9dc7be99c8e9)

![thankyou page](https://github.com/kriteryumm/Aws_QR_Based_Feedback_System/assets/61352431/f19577ea-8dba-44f4-9881-62c26e8da161)

## Usage Concepts
### 1 - AWS EC2 
We write a flask application and run with Aws EC2 (ubuntu).
### 2 - AWS RDS
For the database we used the Aws RDS postresql.
### 3 - AWS S3 
For creating and keeping qr datas we are using Aws S3

## Staff and Admin pages

![staffpage](https://github.com/kriteryumm/Aws_QR_Based_Feedback_System/assets/61352431/1c6bc596-62ec-4ce4-9b52-1d9a9ed005ca)

![adminpage](https://github.com/kriteryumm/Aws_QR_Based_Feedback_System/assets/61352431/9a938986-9e36-48b4-b76d-fd5e1b7667f7)

## important libraries
### 1 - nginx
For web server software we used nginx library.
### 2 - gunicorn
We used this library to run our Python flask application simultaneously by running multiple Python processes on a single dyno.

