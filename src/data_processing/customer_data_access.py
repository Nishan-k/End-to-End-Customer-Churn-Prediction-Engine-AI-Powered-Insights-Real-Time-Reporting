from src.data_processing.database import execute_query


def get_churn_count():
    """
    Get the current churn count from the database.
    """

    query = "SELECT churn, COUNT(*) FROM customer GROUP BY churn;"
    result = execute_query(query=query, return_df=True)

    return result