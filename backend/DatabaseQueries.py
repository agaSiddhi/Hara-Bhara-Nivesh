import mysql.connector

class QueryRunner:
    def __init__(self, connection):
        self.connection= connection

    def execute_query(self, query, params=None):
        """
        Executes a provided SQL query using a cursor.

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): A tuple of parameters to bind to the query.

        Returns:
            list: A list of rows returned by the query, each row represented as a tuple.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params=params)
                return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error executing query: {query}. Error: {err}")
            raise
        finally:
            if not self.connection.autocommit:
                self.connection.commit()

    # def get_companies_by_score(self):
    #     """
    #     Fetches companies from the database ordered by current score descending.

    #     Returns:
    #         list: A list of Company objects.
    #     """
    #     query = "SELECT name, currentScore FROM Company ORDER BY currentScore DESC;"
    #     results = self.execute_query(query)
    #     companies = []
    #     for row in results:
    #         company = Company(row[0], row[1])  # Replace with your Company class initialization
    #         companies.append(company)
    #     return companies

    def get_industry_descriptions(self):
        """
        Fetches a dictionary mapping industry IDs to their descriptions.

        Returns:
            dict: A dictionary where keys are industry IDs and values are descriptions.
        """
        query = "SELECT industryID, description FROM Industry;"
        results = self.execute_query(query)
        descriptions = {}
        for row in results:
            descriptions[row[0]] = row[1]
        return descriptions


# class Company:
#     # Define your Company class attributes and methods here
# # Usage example
#     runner = QueryRunner("localhost", "root", "your_password", "Securities")
#     companies = runner.get_companies_by_score()
#     descriptions = runner.get_industry_descriptions()

#     for company in companies:
#         print(f"{company.name} ({descriptions[company.industryID]})")

#     runner.disconnect()
