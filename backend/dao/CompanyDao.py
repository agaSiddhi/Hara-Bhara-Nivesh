import mysql.connector

class CompanyDao:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
    def execute_query(self, query, params=None):
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
            
    def get_industry_descriptions(self):
        query = "SELECT industryID, description FROM Industry;"
        results = self.execute_query(query)
        descriptions = {}
        for row in results:
            descriptions[row[0]] = row[1]
        return descriptions
    
    def get_company_name_and_description(self):
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
        
        query = f'SELECT companyID FROM Company WHERE name = "{company_name}";'
        result = self.execute_query(query)
        
        return result

    def get_company_details_from_companyID(self, companyID):
        query = f'''SELECT c.companyID, c.name AS companyName, c.createdAt, c.updatedAt, c.totalAssets, c.revenue, c.employeeCount, c.currentScore, c.foundedYear, w.url 
                FROM Company c 
                LEFT JOIN CompanyWebsite w ON c.companyID = w.companyID WHERE c.companyID = {f"'{companyID}'"};'''
        try:
            result = self.execute_query(query)
        except Exception as e:
            print(e)
        
        print(result)
        return result
    
    def get_industry_description_from_companyID(self,companyID=None):
        query = f''' SELECT i.description
                FROM Company c
                JOIN Industry i ON c.industryID = i.industryID
                WHERE c.companyID = "{companyID}"; '''
        result = self.execute_query(query)
        
        return result
    
    def get_price_history_from_companyID(self, companyID=None):
        query = f'''SELECT price, updatedAt
                FROM PriceHistory
                WHERE companyID = "{companyID}";'''
        result = self.execute_query(query)
        return result

    def get_score_history_from_companyID(self, companyID=None):
        query = f'''SELECT score, updatedAt
                FROM ScoreHistory
                WHERE companyID = "{companyID}";'''
        result = self.execute_query(query)
        return result
    
    def get_price_and_date(self):
        query = f'''SELECT companyID, price, updatedAt
                FROM PriceHistory;'''
        result = self.execute_query(query)
        print(result)
        return result
    
    def get_score_and_date(self):
        query = f'''SELECT companyID, score, updatedAt
                FROM ScoreHistory;'''
        result = self.execute_query(query)
        print(result)
        return result
    