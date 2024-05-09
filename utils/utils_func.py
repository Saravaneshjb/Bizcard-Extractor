import easyocr
import pandas as pd
from utils.preprocessing import is_noun,states,cities,db_load
from utils.db_to_df import execute_query
from utils.data_load_sql_connector import Dataload


# Function to extract details
def extract_details(image):
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])

    # Read bytes from the uploaded image file
    image_bytes = image.read()

    # Read text from image
    result = reader.readtext(image_bytes)

    #Gathering the state and the city details 
    state_lst=states()
    city_lst=cities()

    # Extracted details dictionary
    lst_of_items=list()
    noun_lst=list()
    not_noun_lst=list()
    processed_data=list()
    details_dict={"Name": [],
            "Designation": [],
            "Organization_Name": [],
            "State": [],
            "City": [],
            "Pincode": [],
            "Area": [],
            "Phone_number": [],
            "Email_ID": [],
            "Website": []}

    ##Preprocessing the data to remove extra commas and semi-colons
    for detection in result:
        text=detection[1]
        processed_text = text.replace(';', '').replace(',', '')  # Replace both ; and ,
        processed_data.append(processed_text)
        
    #Main Data Processing Starts from the below loop 
    for index,detection in enumerate(processed_data):
        text=detection
        lst_of_items.append(text)
        print(text)
        if (('+' in text) or ('-' in text)) and any(items.isdigit() for items in text):
            details_dict['Phone_number'].append(text)
            not_noun_lst.append(text)
        elif ("@" not in text.lower()) and ("www" in text.lower() or ".com" in text.lower()):
            details_dict['Website'].append(text)
            not_noun_lst.append(text)
        elif "@" in text.lower():
            details_dict['Email_ID'].append(text)
            not_noun_lst.append(text)
        elif text.isdigit() and (len(text)==6 or len(text)==7):
            details_dict['Pincode'].append(text)
            not_noun_lst.append(text)
        elif text.lower() in [items.lower() for items in state_lst]:
            details_dict['State'].append(text)
        elif text.lower() in [items.lower() for items in city_lst]:
            details_dict['City'].append(text)
            details_dict['Area'].append(text)
        elif index==0:
            details_dict['Name'].append(text)
        elif index==1:
            details_dict['Designation'].append(text)
        elif is_noun(text.lower()):
            noun_lst.append(text)
        else:
            not_noun_lst.append(text)

    ## Iterating over the Noun list 
    print("\n")
    print("The noun list items begins from here")
    for noun_items in noun_lst:
        if len(noun_items.split())>1:
            for items in noun_items.split():
                print(items)
                if items.lower() in [items.lower() for items in state_lst]:
                    # print(f"The {items} is a state")
                    details_dict['State'].append(items)
                elif items.lower() in [items.lower() for items in city_lst]:
                    details_dict['City'].append(items)
                    details_dict['Area'].append(items)
                elif items.isdigit() and (len(items)==6 or len(items)==7):
                    # print(f"{items} is a pincode")
                    details_dict['Pincode'].append(items)

    # Code to set the Organization Name 
    final_items=list()
    for items in details_dict.values():
        for vals in items:
            final_items.append(vals)

    # Convert final_items to a set for faster lookup
    final_items_set = set(final_items)
    # print(final_items_set)

    # Create a new list to store items not present in final_items
    updated_lst_of_items = []

    # Iterate through lst_of_items
    for item in lst_of_items:
        # Check if any part of the item is present in final_items
        if not any(part in final_items_set for part in item.split()):
            # If not present, add the item to updated_lst_of_items
            updated_lst_of_items.append(item)

    # Update lst_of_items with updated_lst_of_items
    lst_of_items = updated_lst_of_items
    # print("Lst of items before last check")
    print(lst_of_items)
    print(final_items)

    #One final check 
    for items in lst_of_items:
        # print(f'{items} being processed')
        if (items not in final_items) and (not any(char.isdigit() for char in items)) and ('st ' not in items.lower() or 'st' not in items.lower() or len(items)>3):
            details_dict['Organization_Name'].append(items)
            # continue
        # elif items not in final_items:
        #     details_dict['Organization Name'].append(items)
    
    print(details_dict)
    ## Logic to unpack all the elements in the list and store them as a string in the Dictionary
    for item in details_dict:
        if item=='Organization_Name':
            if len(details_dict[item])>1:
                # print(item, my_dict[item][0]+' '+my_dict[item][1])
                details_dict[item]=details_dict[item][0]+' '+details_dict[item][1]
            elif len(details_dict[item])==1:
                details_dict[item] = details_dict[item][0]
        elif item=='Website':
            if len(details_dict[item])>1:
                # print(item, my_dict[item][0]+' '+my_dict[item][1])
                details_dict[item]=details_dict[item][0]+'.'+details_dict[item][1]
            else:
                if details_dict[item][0][3]=='.':
                    details_dict[item] = details_dict[item][0]
                else:
                    details_dict[item]=details_dict[item][0][0:3]+'.'+details_dict[item][0][4:]
        else:
            if item!="Phone_number":
                if isinstance(details_dict[item], list):
                    details_dict[item] = ' '.join(details_dict[item])
                else:
                    details_dict[item] = details_dict[item]
            elif item=="Phone_number" and len(details_dict[item])==1:
                if isinstance(details_dict[item], list):
                    details_dict[item] = ' '.join(details_dict[item])
                else:
                    details_dict[item] = details_dict[item]

    print(details_dict)

    #Logic to convert the dictionary to a dataframe 
    details_dict['Phone_number'] = str(details_dict['Phone_number'])
    df=pd.DataFrame(details_dict,index=[0])
    df2=df.T

    # return details_dict
    return df,df2,details_dict

# def display_data(uploaded_file):

#     # Display details if image is uploaded
#     if uploaded_file is not None:
#         # Display uploaded image
#         # st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
        
#         # Extract details from image
#         # if df is None or details is None:
#         df,df_T,details = extract_details(uploaded_file)
#         # print('The details :\n',details)

#         # Display details
#         if not df.empty:
#             print("Details extracted from the business card:")
#             # st.write("Name:", details.get("Name", ""))
#             # st.write("Designation:", details.get("Designation", ""))
#             # st.write("Organization_Name:", details.get("Organization_Name", ""))
#             # st.write("State:", details.get("State", ""))
#             # st.write("City:", details.get("City", ""))
#             # st.write("Pincode:", details.get("Pincode", ""))
#             # st.write("Area:", details.get("Area", ""))
#             # st.write("Phone_number:", details.get("Phone_number", ""))
#             # st.write("Email_ID:", details.get("Email_ID", ""))
#             # st.write("Website:", details.get("Website", ""))
#             with st.expander("View Details"):
#                 st.write(df_T)
#         else:
#             st.error("Failed to extract details from the image. Please try again with a different image.")

# Load the information in the dataframe to the database table
def load_df_to_db(df):
    # if df is None:
    #     st.error("Please extract details before attempting to load to DB ")
    #     return 
    # Extract details from image
    # if df is None or details is None:
    # df,df_T,details = extract_details(uploaded_file)
    df_name="card_details"
    db_load(df,df_name)
    # st.success("Data loaded successfully into the DB")

def read_data():
    read_query="""select * from card_details;"""
    query_result=execute_query(read_query)

    return query_result

def update_data():
    selected_update_columns = st.multiselect("Select columns to perform update operation:", 
                                      ["Name", "Designation", "Organization_Name", "State", 
                                       "City", "Pincode", "Area", "Phone_number", "Email_ID", "Website"])
    selected_where_columns = st.multiselect("Select columns for the WHERE clause:", 
                                      ["Name", "Designation", "Organization_Name", "State", 
                                       "City", "Pincode", "Area", "Phone_number", "Email_ID", "Website"])
    if selected_update_columns:
        with st.form("Update_table"):
            input_update_data = {}
            input_where_data = {}
            for upd_column in selected_update_columns:
                input_update_data[upd_column] = st.text_input(f"Enter new value for {upd_column}:", key=f"{upd_column}_update")
            for whr_column in selected_where_columns:
                input_where_data[whr_column] = st.text_input(f"Enter value for {whr_column}:", key=f"{whr_column}_where")
            if st.form_submit_button("Update"):
                print("============The Update button is clicked==================")
                print("The update data dictionary : ",input_update_data)
                print("The where data dictionary :", input_where_data)
                if input_update_data:
                    print("Inside the if condition of the if input_update_data")
                    # Generate the Update Query 
                    update_query = "UPDATE card_details SET "
                    for column, value in input_update_data.items():
                        if column == "Pincode":
                            update_query += f"{column} = {value}, "
                        else:
                            update_query += f"{column} = '{value}', "
                    update_query = update_query.rstrip(", ")
                    print("Update query generated by providing just the update fields : ", update_query)
                if input_where_data:
                    # Include the where condition in the update query
                    print("Inside if condition for where clause")
                    for column, value in input_where_data.items():
                        if column == "Pincode":
                            update_query += f" WHERE {column} = {value} AND "
                        else:
                            update_query += f" WHERE {column} = '{value}' AND "
                    update_query = update_query.rstrip(" AND ")
                print("The Update query generated is:", update_query)
                dl_ob = Dataload()
                dl_ob.execute_update_query(update_query)
                # To display the Updated record from database 
                select_query = "SELECT * FROM card_details WHERE "
                conditions = []
                for column, value in input_update_data.items():
                    if column == "Pincode":
                        conditions.append(f"{column}={value}")
                    else:
                        conditions.append(f"{column}='{value}'")
                select_query += " AND ".join(conditions) + " "
                print("The select query generated is : ",select_query)
                query_result = dl_ob.execute_query(select_query)
                # Display the updated record
                st.write(query_result)

def delete_data():
    selected_delete_columns = st.multiselect("Select columns to perform Delete Operation:", 
                                      ["Name", "Designation", "Organization_Name", "State", 
                                       "City", "Pincode", "Area", "Phone_number", "Email_ID", "Website"])
    
    if selected_delete_columns:
        with st.form("Update_table"):
            input_del_data = {}
            for del_column in selected_delete_columns:
                input_del_data[del_column] = st.text_input(f"Enter new value for {del_column}:", key=f"{del_column}_delete")
            if st.form_submit_button("Delete"):
                # print("============The Update button is clicked==================")
                # print("The update data dictionary : ",input_update_data)
                # print("The where data dictionary :", input_where_data)
                if input_del_data:
                    print("Inside the if condition of the if input_del_data")
                    # Generate the Update Query 
                    delete_query = "DELETE FROM card_details where "
                    for column, value in input_del_data.items():
                        if column == "Pincode":
                            delete_query += f"{column} = {value} AND "
                        else:
                            delete_query += f"{column} = '{value}' AND "
                    delete_query = delete_query.rstrip(" AND ")
                    print("Delete query generated by providing delete : ", delete_query)
                print("The Update query generated is:", delete_query)
                dl_ob = Dataload()
                dl_ob.execute_update_query(delete_query)
                # To display the records in database after deletion
                select_query = "SELECT * FROM card_details"
                # conditions = []
                # for column, value in input_del_data.items():
                #     if column == "Pincode":
                #         conditions.append(f"{column}={value}")
                #     else:
                #         conditions.append(f"{column}='{value}'")
                # select_query += " AND ".join(conditions) + " "
                print("The select query generated is : ",select_query)
                query_result = dl_ob.execute_query(select_query)
                # Display the updated record
                st.write("Data in the card details table after deletion")
                st.write(query_result)







