# Wave Petplus Backend

Wave Petplus Backend is a Django-based backend application. This repository contains all the code and resources required to run the backend.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#Local-Usage)
- [Docker](#Running-with-Docker-and-Docker-Compose)
- [API Endpoints](#api-endpoints)
- [License](#license)
- [Postman test](#Postman-Tests)

## Overview

Wave Petplus Backend is built using the Django framework, a high-level Python web framework that promotes rapid development and clean, pragmatic design. The backend utilizes various Django features and follows best practices to ensure a robust and scalable application.

## Installation

To get a copy of the backend up and running on your local machine, follow these steps:

1. Clone the repository: `git clone https://github.com/Henriknn01/ShopBackend`
2. Change to the project directory: `cd ShopBackend`
3. Create a virtual environment: `python -m venv myenv`
4. Activate the virtual environment:
   - On Windows: `myenv\Scripts\activate`
   - On macOS/Linux: `source myenv/bin/activate`
5. Install the project dependencies: `pip install -r requirements.txt`

## Local Usage

To use the backend, follow these steps:

1. Make migrations: `python manage.py makemigrations`
2. Apply migrations to set up the database: `python manage.py migrate`
3. Create a super user: `python manage.py createsuperuser` and follow the steps
4. Create the groups: `python manage.py create_groups`
5. Start the development server: `python manage.py runserver`
6. Access the backend API endpoints through `http://localhost:8000`

## Running with Docker and Docker Compose

Wave Petplus Backend can be easily run using Docker and Docker Compose. Docker provides containerization, which ensures consistent and isolated environments for running the application. Docker Compose simplifies the management of multiple containers required for the project.

To run Wave Petplus Backend with Docker and Docker Compose, follow these steps:

1. Open the `docker-compose.yml` file and make any necessary configuration changes.
2. Build the Docker images and start the containers: `docker-compose up -d`
3. The application should now be running. You can access it through the specified port in your browser or use the provided API endpoints.

Remember to stop the containers when you're done: `docker-compose down`

## API Endpoints

The backend provides the following API endpoints:

| Name              | Description                                      |
| ----------------- | ------------------------------------------------ |
| [User](http://api.norheimweb.com/user/)             | API endpoint for managing user data               |
| [Discount](http://api.norheimweb.com/discount/)     | API endpoint for managing discounts               |
| [Tag](http://api.norheimweb.com/tag/)               | API endpoint for managing tags                    |
| [Product Category](http://api.norheimweb.com/productcategory/) | API endpoint for managing product categories |
| [Product](http://api.norheimweb.com/product/)       | API endpoint for managing products                |
| [Image](http://api.norheimweb.com/image/)           | API endpoint for managing images                  |
| [Blog Post](http://api.norheimweb.com/blogpost/)     | API endpoint for managing blog posts              |
| [Product List](http://api.norheimweb.com/productlist/) | API endpoint for managing product lists        |
| [Wishlist](http://api.norheimweb.com/wishlist/)     | API endpoint for managing wishlists               |
| [Product Review](http://api.norheimweb.com/productReview/) | API endpoint for managing product reviews   |
| [Order](http://api.norheimweb.com/order/)           | API endpoint for managing orders                  |
| [Order Item](http://api.norheimweb.com/order-item/) | API endpoint for managing order items             |



## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Postman Tests

As our postman tests were just to powerful, we have to run the collections one by one because of licensing issues.

