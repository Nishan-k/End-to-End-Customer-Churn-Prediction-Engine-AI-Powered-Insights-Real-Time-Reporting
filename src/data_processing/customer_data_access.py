from src.data_processing.database import execute_query


def get_customer_dist_count():
    """
    Get the current churn count from the database.
    """

    query = "SELECT churn, COUNT(*) FROM customer GROUP BY churn;"
    result = execute_query(query=query, return_df=True)

    return result



def load_all_data():
    """
    Load all the data from the database to train the ML model.
    """
    
    query = "SELECT * FROM customer;"
    result = execute_query(query=query, return_df=True)
    return result




def get_churn_count():
    """
    Get the total number of customers who will churn.
    """
    result = execute_query(
        "SELECT COUNT(*) FROM customer WHERE churn = 'Yes'",
        return_df=True
    )
    return result.iloc[0, 0] if not result.empty else 0
    
