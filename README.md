# Business Card Details Extractor

This Streamlit application allows users to extract information from uploaded business card images and store it in a database. It offers various functionalities such as extraction, display, loading to the database, reading from the database, updating, and deleting information.

## Features

1. **Upload Business Card Images**: Users can upload images of business cards through the user interface.

2. **Information Extraction**: Upon uploading an image, the application extracts the following information from the business card:
   - Company Name
   - Card Holder Name
   - Designation
   - Mobile Number
   - Email Address
   - Website URL
   - Area
   - City
   - State
   - Pincode

3. **Display Extracted Information**: The extracted information is displayed back to the user on the graphical user interface (GUI).

4. **Database Interaction**:
   - **Load and Save**: Users have the option to load and save all the extracted information into a database.
   - **Read Data**: The application can read data from the database once it's stored.
   - **Update Data**: Users can update the extracted and stored information in the database.
   - **Delete Data**: Information stored in the database can be deleted via the user interface.

## Technologies Used

1. **Python**: The application is built using the Python programming language.
2. **Streamlit**: Streamlit is used to create the interactive web application interface.
3. **easyOCR**: easyOCR is used for optical character recognition (OCR) to extract text from business card images.
4. **Database**: A database is used to store and manage the extracted information. The choice of database system can vary based on requirements.

## How to Run

To run the application locally:

1. Clone the repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Run the Streamlit application using `streamlit run app.py`.
4. Access the application in your web browser at the provided URL.

## Contributors

- Saravanesh
