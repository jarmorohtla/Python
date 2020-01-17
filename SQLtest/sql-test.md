# SQL test

The task is to create a simple schema with mock values and then perform some queries on the data.

The language for the parts of the solution that cannot be implemented in SQL should be either Python or Nodejs.

For the database I recommend you use something simple, such as sqlite or similar, that is easy to set up, 
is self contained and can be presented with the solution. Alternatively a PostgreSQL dump is fine too.

The solution should contain the SQL for schema creation, the algorithms for mock data generation
and the code/queries for finding related products in the last step.

Please do try to keep the dependencies to external libraries and tools to a minimum and provide
instructions for installing any that may be required.


## Step 1 - the schema

Create the following tables:

* Products:
	- id - the product identifier
	- name - the product name

* Orders:
	- id - the order id

* Order lines:
	- id - id of the order line
	- order_id - reference to Orders model
	- product_id - reference to Products model
	- quantity - Quantity of the ordered product


## Step 2 - test data generation

Generate mock products (name generation can be as simple or as interesting as you desire) and 
a significant amount of orders containing random selection of random quantities of products. 

The methods of generation are up to you as long as the resulting orders are diverse in character.


## Step 3 - related products

Given a product (by it's id), find out which other items have been purchased in the same order
with the given product.

Order the results by popularity, where polularity is defined by the number of times a product
has been purchased (not the quantity of the product in any given order).

The solution should present a reasonably easy way for the reviewer to see all products and to query
related products for any given product.
