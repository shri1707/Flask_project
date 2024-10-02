# Influencer Engagement and Sponsorship Coordination Platform

# Made By Shrijan Kumar 23f2003824

## Modern Application Development-I May, 2024

### Author 

**Name**: Shrijan Kumar<br>
**Roll No**: 23f2003824<br>
**Email**: 23f2003824@ds.study.iitm.ac.in<br>
**About**: I joined this course in May,2023 and since then I've developed a keen interest in coding. In school I learned Python which ignited my interest in programming. SQL has been a strong point in my whole journey. I also learned HTML, CSS, JS in foundation level through other resources which also helped me in this project.

### Description

<p>We’re making a project using Flask, Jinja2, SQLite and JQuery. It is a coordination platform between influencers and sponsors. The aim is to help both Influencers and sponsors to make their collaborations a bit easy and seamless. So that an influencer can find a right sponsor and a sponsor can find a right influencer for their campaigns.</p>

### Technologies used

- **Jinja2**: Render dynamic HTML templates with data in Flask.<br>
- **Flask**: To Develop the Business logic.<br>
- **SQLAlchemy**: Manage database operations with an ORM(Object Relational Mapping).<br>
- **SQLite**:  Store and retrieve data in a lightweight, file-based database.<br>
- **RESTful**:  Design and implement web services using REST architecture principles.<br>
- **HTML/CSS/JS**: Design and style the web application's frontend and add interactivity.<br>
- **JQuery**: Simplify JavaScript programming for dynamic web pages.<br>
- **Datetime Module**: Handle and manipulate date and time data.<br>
- **Matplotlib**: Create visualizations and plots for data analysis.<br>

### DB Schema Design 

![db image](/static/images/Database%20ER%20diagram%20(crow's%20foot).png)

### API Design 

<p>This API provides endpoints for managing campaigns, influencers, and sponsors within a Flask application. It supports CRUD operations (Create, Read, Update, Delete) for each entity using RESTful principles.</p>

| API endpoints | APIs For      |                |               |
|---------------|---------------|----------------|---------------|
|               | **Campaign**  | **Sponsor**    | **Influencer**|
| **GET**       | /api/campaign/<int:spon_id>  | /api/sponsor/<int:spon_id> | /api/influencer/<int:influ_id> |
| **POST**      | /api/campaign/<int:spon_id>  | /api/sponsor   | /api/influencer |
| **PUT**       | /api/campaign/update/<int:spon_id> | /api/sponsor/update/<int:spon_id> | /api/influencer/update/<int:influ_id> |
| **DELETE**    | /api/campaign/delete/<int:spon_id> | /api/sponsor/delete/<int:spon_id> | /api/influencer/delete/<int:influ_id> |

### Architecture and Features 

<p>I’ve organized all my files in a folder named after my roll number, inside of that i’ve a CODES folder that is having my  template folder where i’ve all my HTMLs, another folder named static in which i’ve all my css files and images, and a backend folder with controller, APIs and models and a app.py separately. In the root folder i also have this PDF saved.</p>

### Video 

</p>Link to your online video of not more than 3 minutes length</p>



