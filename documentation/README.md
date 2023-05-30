### Guide: How to Run Postman Tests

This guide provides step-by-step instructions on how to run Postman tests.

---

#### Step 1: Install Postman

1. Download and install Postman from the official website: [postman.com](https://www.postman.com/downloads/).
2. Follow the installation instructions specific to your operating system.

---

#### Step 2: Import a Postman Collection

1. Launch Postman.
2. Click on the **Import** button on the top left corner of the Postman application.
3. Select the option to **Import File**.
4. Browse and select the Postman collection file (.json or .postman_collection) from your local machine. [Make sure to import the 2 .json files separately ]
5. Click **Open** to import the collection into Postman.

---

#### Step 3: Select Collection and Environment

1. In the left sidebar of the Postman application, click on **Collections**.
2. Find and click on the "Wave shop tests" collection.
3. In the right upper corner of the screen, select **Wave Environment** as the environment for the collection.
4. go to the Variables tab on the collection, and change baseUrl to the correct url you want to test

---

#### Step 4: Modify Environment Variables

1. Click on the **Environments** tab in the Postman application.
2. Locate and open the **Wave Environment** from the list.
3. Change the current value of the variable **admin_password** to the superuser password.
4. Change the current value of the variable **admin_username** to the superuser email address.
5. Click **Save changes** to update the environment variables.

---

#### Step 5: Run Postman Tests

1. Go back to the **Collections** tab and select the "Wave shop tests" collection.
2. Click on the **Run** button located on the top right corner of the Postman application.
3. In the **Collection Run** window, select the collection you want to run (if not already selected).
4. Choose the **Wave Environment** from the **Environment** dropdown.
5. Click on the **Run wave Shop Tests** button to begin executing the tests in the collection.
6. Wait for the tests to complete. You can view the test results in the **Run** window.