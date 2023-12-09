import graphene
from graphene_django.types import DjangoObjectType
from django.db import connection



def get_top_10_best_scores():
    with connection.cursor() as cursor:
        cursor.execute("SELECT score FROM reviews ORDER BY score DESC LIMIT 10;")
        rows = cursor.fetchall()
        return [ReviewType(score=float(row[0])) for row in rows if row[0] is not None]
def get_top_10_worst_scores():
    with connection.cursor() as cursor:
        cursor.execute("SELECT score FROM reviews ORDER BY score ASC LIMIT 10")
        rows = cursor.fetchall()
        return [ReviewType(score=float(row[0])) for row in rows if row[0] is not None]

def get_first_200_reviews():
    with connection.cursor() as cursor:
        cursor.execute("SELECT score FROM reviews LIMIT 200")
        rows = cursor.fetchall()
        return [ReviewType(score=float(row[0])) for row in rows if row[0] is not None]

class MaxMinScoreType(graphene.ObjectType):
    max_score = graphene.Float()
    min_score = graphene.Float()



class ReviewType(graphene.ObjectType):
    productid = graphene.String()
    review_date = graphene.String()
    average_score = graphene.Float()
    average_helpfulness = graphene.Float()
    productId = graphene.String()  # Corregido
    userid = graphene.String()     # Corregido
    profilename = graphene.String()  # Corregido
    helpfulness = graphene.String()  # Corregido
    score = graphene.Float()        # Corregido
    reviewtime = graphene.Int()     # Corregido
    summary = graphene.String()     # Corregido
    reviewtext = graphene.String()   # Corregido


class Query(graphene.ObjectType):
    reviews_filter = graphene.List(ReviewType, product_id=graphene.String(), user_id=graphene.String(), start_date=graphene.Int(), end_date=graphene.Int())

    def resolve_reviews_filter(self, info, product_id=None, user_id=None, start_date=None, end_date=None):
        with connection.cursor() as cursor:
            query = """
            SELECT 
                TO_CHAR(TO_TIMESTAMP(reviewtime), 'YYYY-MM-DD') AS review_date,
                AVG(score) AS average_score, 
                AVG(CAST(SPLIT_PART(helpfulness, '/', 1) AS FLOAT) / NULLIF(CAST(SPLIT_PART(helpfulness, '/', 2) AS FLOAT), 0)) AS average_helpfulness
            FROM 
                reviews
            WHERE
            """
            conditions = []
            params = []
            
            if product_id:
                conditions.append("productid = %s")
                params.append(product_id)
            if user_id:
                conditions.append("userid = %s")
                params.append(user_id)
            if start_date and end_date:
                conditions.append("reviewtime >= %s AND reviewtime <= %s")
                params.extend([start_date, end_date])

            if conditions:
                query += " AND ".join(conditions)
            else:
                query += "1=1"  # Para evitar errores SQL si no hay condiciones

            query += " GROUP BY review_date"

            cursor.execute(query, tuple(params))
            result = cursor.fetchall()

        return [ReviewType(
            review_date=row[0],
            average_score=row[1],
            average_helpfulness=row[2]
        ) for row in result]

    
    user_count = graphene.Int(product_id=graphene.String(), user_id=graphene.String(), start_date=graphene.Int(), end_date=graphene.Int())

    def resolve_user_count(self, info, product_id=None, user_id=None, start_date=None, end_date=None):
        with connection.cursor() as cursor:
            query = "SELECT COUNT(DISTINCT userid) FROM reviews WHERE "
            conditions = []
            params = []
            
            if product_id:
                conditions.append("productid = %s")
                params.append(product_id)
            if user_id:
                conditions.append("userid = %s")
                params.append(user_id)
            if start_date and end_date:
                conditions.append("reviewtime >= %s AND reviewtime <= %s")
                params.extend([start_date, end_date])

            if conditions:
                query += " AND ".join(conditions)
            else:
                query += "1=1"  # Para evitar errores SQL si no hay condiciones

            cursor.execute(query, tuple(params))
            result = cursor.fetchone()
        return result[0]

    max_min_score = graphene.Field(MaxMinScoreType, product_id=graphene.String(), user_id=graphene.String(), start_date=graphene.Int(), end_date=graphene.Int())

    def resolve_max_min_score(self, info, product_id=None, user_id=None, start_date=None, end_date=None):
        with connection.cursor() as cursor:
            query = "SELECT MAX(score), MIN(score) FROM reviews WHERE "
            conditions = []
            params = []
            
            if product_id:
                conditions.append("productid = %s")
                params.append(product_id)
            if user_id:
                conditions.append("userid = %s")
                params.append(user_id)
            if start_date and end_date:
                conditions.append("reviewtime >= %s AND reviewtime <= %s")
                params.extend([start_date, end_date])

            if conditions:
                query += " AND ".join(conditions)
            else:
                query += "1=1"

            cursor.execute(query, tuple(params))
            result = cursor.fetchone()
        return MaxMinScoreType(max_score=result[0], min_score=result[1])

    
    
    average_score = graphene.Float(product_id=graphene.String(), user_id=graphene.String(), start_date=graphene.Int(), end_date=graphene.Int())

    def resolve_average_score(self, info, product_id=None, user_id=None, start_date=None, end_date=None):
        with connection.cursor() as cursor:
            query = "SELECT AVG(score) FROM reviews WHERE "
            conditions = []
            params = []
            
            if product_id:
                conditions.append("productid = %s")
                params.append(product_id)
            if user_id:
                conditions.append("userid = %s")
                params.append(user_id)
            if start_date and end_date:
                conditions.append("reviewtime >= %s AND reviewtime <= %s")
                params.extend([start_date, end_date])

            if conditions:
                query += " AND ".join(conditions)
            else:
                query += "1=1"

            cursor.execute(query, tuple(params))
            result = cursor.fetchone()
        return result[0] if result[0] is not None else 0
    
    
    
    top_10_best_scores = graphene.List(ReviewType, product_id=graphene.String(), user_id=graphene.String(), start_date=graphene.Int(), end_date=graphene.Int())

    def resolve_top_10_best_scores(self, info, product_id=None, user_id=None, start_date=None, end_date=None):
        with connection.cursor() as cursor:
            query = "SELECT * FROM reviews WHERE score IS NOT NULL "
            conditions = []
            params = []
            
            if product_id:
                conditions.append("productid = %s")
                params.append(product_id)
            if user_id:
                conditions.append("userid = %s")
                params.append(user_id)
            if start_date and end_date:
                conditions.append("reviewtime >= %s AND reviewtime <= %s")
                params.extend([start_date, end_date])

            if conditions:
                query += " AND " + " AND ".join(conditions)
            query += " ORDER BY score DESC LIMIT 10"

            cursor.execute(query, tuple(params))
            result = cursor.fetchall()

        return [ReviewType(
                    productid=row[0],
                    userid=row[1],
                    profilename=row[2],
                    helpfulness=row[3],
                    score=row[4],
                    reviewtime=row[5],
                    summary=row[6],
                    reviewtext=row[7]
                ) for row in result]

    top_10_worst_scores = graphene.List(ReviewType, product_id=graphene.String(), user_id=graphene.String(), start_date=graphene.Int(), end_date=graphene.Int())

    def resolve_top_10_worst_scores(self, info, product_id=None, user_id=None, start_date=None, end_date=None):
        with connection.cursor() as cursor:
            query = "SELECT * FROM reviews WHERE score IS NOT NULL "
            conditions = []
            params = []
            
            if product_id:
                conditions.append("productid = %s")
                params.append(product_id)
            if user_id:
                conditions.append("userid = %s")
                params.append(user_id)
            if start_date and end_date:
                conditions.append("reviewtime >= %s AND reviewtime <= %s")
                params.extend([start_date, end_date])

            if conditions:
                query += " AND " + " AND ".join(conditions)
            query += " ORDER BY score ASC LIMIT 10"

            cursor.execute(query, tuple(params))
            result = cursor.fetchall()

        return [ReviewType(
                    productid=row[0],
                    userid=row[1],
                    profilename=row[2],
                    helpfulness=row[3],
                    score=row[4],
                    reviewtime=row[5],
                    summary=row[6],
                    reviewtext=row[7]
                ) for row in result]




    first_200_reviews = graphene.List(ReviewType, product_id=graphene.String(), user_id=graphene.String(), start_date=graphene.Int(), end_date=graphene.Int())

    def resolve_first_200_reviews(self, info, product_id=None, user_id=None, start_date=None, end_date=None):
        with connection.cursor() as cursor:
            query = "SELECT * FROM reviews "
            conditions = []
            params = []
            
            if product_id:
                conditions.append("productid = %s")
                params.append(product_id)
            if user_id:
                conditions.append("userid = %s")
                params.append(user_id)
            if start_date and end_date:
                conditions.append("reviewtime >= %s AND reviewtime <= %s")
                params.extend([start_date, end_date])

            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            query += " LIMIT 200"

            cursor.execute(query, tuple(params))
            result = cursor.fetchall()

        return [ReviewType(
                    productid=row[0],
                    userid=row[1],
                    profilename=row[2],
                    helpfulness=row[3],
                    score=row[4],
                    reviewtime=row[5],
                    summary=row[6],
                    reviewtext=row[7]
                ) for row in result]

    
schema = graphene.Schema(query=Query)
