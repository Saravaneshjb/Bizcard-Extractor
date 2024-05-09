import india
import nltk
from utils.data_load_sql_connector import Dataload
from mysql.connector import IntegrityError
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Function to detect if a word is a noun
def is_noun(word):
    # Tokenize the word
    tokens = nltk.word_tokenize(word)
    
    # Perform POS tagging
    tagged = nltk.pos_tag(tokens)
    
    # Check if the word is tagged as a noun (NN)
    for _, tag in tagged:
        if tag == 'NN':
            return True
    return False

# Function to return all the states present in Indian sub-continent 
def states():
    state_lst=[
        'Andaman & Nicobar',
        'AndhraPradesh',
        'ArunachalPradesh',
        'Assam',
        'Bihar',
        'Chandigarh',
        'Chhattisgarh',
        'Dadra and Nagar Haveli and Daman and Diu',
        'Delhi',
        'Goa',
        'Gujarat',
        'Haryana',
        'HimachalPradesh',
        'Jammu & Kashmir',
        'Jharkhand',
        'Karnataka',
        'Kerala',
        'Ladakh',
        'Lakshadweep',
        'MadhyaPradesh',
        'Maharashtra',
        'Manipur',
        'Meghalaya',
        'Mizoram',
        'Nagaland',
        'Odisha',
        'Puducherry',
        'Punjab',
        'Rajasthan',
        'Sikkim',
        'TamilNadu',
        'Telangana',
        'Tripura',
        'UttarPradesh',
        'Uttarakhand',
        'WestBengal']
    
    return state_lst


# Function to return all the cities in India
def cities():    
    city_lst=list()

    for items in india.CITIES:
        city_lst.append(str(items))
    return city_lst


# Load the details in the dataframe into the database 
def db_load(dataframe,dataframe_name):
    try:
        if dataframe is not None:
            # Display the DataFrame returned by the function
            # st.write(dataframe)
            try:
                dl_ob=Dataload()
                dl_ob.load_df(dataframe,dataframe_name)
                # logging.info(f"{dataframe} Data Extracted, processed & loaded successfully")
            except IntegrityError as e:
                print(f'Unique Key Violation while inserting the to the {dataframe} table. Provide another id')
            except Exception as e:
                print(f"Error loading {dataframe} data to database {e}")
        else:
            print('Failed to retrieve channel details. Please check the Channel ID')
    except Exception as e:
        print(f"An exception has occured : {e}")
