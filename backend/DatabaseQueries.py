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
    
    def get_company_name_and_description(self):
        """
        Retrieves the company name, currentScore, and description from the database. 
        Returns a dictionary containing the company names as keys and their corresponding details as values.
        """
        query = "SELECT name,currentScore, (SELECT description FROM Industry WHERE Company.industryID = Industry.industryID)  FROM Company ORDER BY currentScore DESC;"
        results = self.execute_query(query)
        descriptions = {}
        rank = 1
        for row in results:
            # print(list(row[1:]))
            temp = list(row[1:])
            temp.append(rank)
            descriptions[row[0]] = temp
            rank += 1
            # print(descriptions)
        return descriptions
    
    def get_companyID_from_company_name(self,company_name=None):
        """
        Get company ID from company name.

        Args:
            company_name (str): The name of the company.

        Returns:
            The company ID.
        """
        
        query = f'SELECT companyID FROM Company WHERE name = "{company_name}";'
        result = self.execute_query(query)
        
        return result

    def get_company_details_from_companyID(self, companyID):
        """
        Retrieves company details based on the provided companyID.

        Parameters:
            companyID (int): The unique identifier of the company.

        Returns:
            result: The retrieved company details.
        """
        query = f'''SELECT c.companyID, c.name AS companyName, c.createdAt, c.updatedAt, c.totalAssets, c.revenue, c.employeeCount, c.currentScore, c.foundedYear, w.url 
                FROM Company c 
                LEFT JOIN CompanyWebsite w ON c.companyID = w.companyID WHERE c.companyID = "{companyID}";'''
        result = self.execute_query(query)
        print(result)
        return result
    
    def get_industry_description_from_companyID(self,companyID=None):
        """
        Retrieves the industry description associated with the given company ID.

        Args:
            companyID (int): The ID of the company for which the industry description is to be retrieved. Defaults to None.

        Returns:
            str: The industry description associated with the specified company ID.
        """
        
        query = f'''SELECT i.description
                FROM Company c
                JOIN Industry i ON c.industryID = i.industryID
                WHERE c.companyID = "{companyID}";'''
        result = self.execute_query(query)
        
        return result
    
    def get_price_history_from_companyID(self, companyID=None):
        """
        Retrieve price history for a specific company based on the companyID.

        Args:
            companyID (int): The ID of the company for which to retrieve price history.
        Returns:
            list: A list of tuples containing price and updatedAt information.
        """
        query = f'''SELECT price, updatedAt
                FROM PriceHistory
                WHERE companyID = "{companyID}";'''
        result = self.execute_query(query)
        return result

    def get_score_history_from_companyID(self, companyID=None):
        """
        Get the score history for a specific company ID.

        Args:
            companyID (int): The ID of the company to retrieve the score history for.

        Returns: 
            list: A list of tuples containing the score and the timestamp when it was updated.
        """
        query = f'''SELECT score, updatedAt
                FROM ScoreHistory
                WHERE companyID = "{companyID}";'''
        result = self.execute_query(query)
        return result