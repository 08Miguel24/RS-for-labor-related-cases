from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def create_friendship(self, person1_name, person2_name):
        with self.driver.session(database="neo4j") as session:
            # Write transactions allow the driver to handle retries and transient errors
            # pass also the static method callback along with the other arguments
            result = session.execute_write(self._create_and_return_friendship, person1_name, person2_name)
            for row in result:
                print("Created friendship between: {p1}, {p2}".format(p1=row['p1'], p2=row['p2']))

    @staticmethod
    def _create_and_return_friendship(tx, person1_name, person2_name):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            "CREATE (p1:Person { name: $person1_name }) "
            "CREATE (p2:Person { name: $person2_name }) "
            "CREATE (p1)-[:KNOWS]->(p2) "
            "RETURN p1, p2"
        )
        result = tx.run(query, person1_name=person1_name, person2_name=person2_name)
        try:
            return [{"p1": row["p1"]["name"], "p2": row["p2"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def find_person(self, person_name):
        with self.driver.session(database="neo4j") as session:
            # pass the static method callback along with the other arguments
            result = session.execute_read(self._find_and_return_person, person_name)
            for row in result:
                print("Found person: {row}".format(row=row))

    @staticmethod
    def _find_and_return_person(tx, person_name):
        query = (
            "MATCH (p:Person) "
            "WHERE p.name = $person_name "
            "RETURN p.name AS name"
        )
        result = tx.run(query, person_name=person_name)
        return [row["name"] for row in result]

    def create_judgement(self, person1, person2):
        with self.driver.session(database="neo4j") as session:
            # Write transactions allow the driver to handle retries and transient errors
            # pass also the static method callback along with the other arguments
            result = session.execute_write(self._create_judgement, person1, person2)
            for row in result:
                print("Created judgement: {j1}, {j2}".format(j1=row['j1'], j2=row['j2']))

    @staticmethod
    def _create_judgement(tx, person1, person2):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/

        query = (
            "CREATE (j1:Judgement { name: $person1, date: $date1 }) "
            "CREATE (j2:Judgement { name: $person2, date: $date2 }) "
            "RETURN j1, j2"
        )
        result = tx.run(query, person1=person1['judgement'], date1=person1['date'], person2=person2['judgement'], date2=person1['date'])
        try:
            return [{"j1": row["j1"]["name"], "j2": row["j2"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_article(self, article):
        pass

    def _create_article(tx, article):
        pass

if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    
    # as long as instance is running on the remote machine
    # and is being managed by the administrator this script will run
    # using the following credentials given by the admin to access the DB

    # credentials:
    # NEO4J_URI=neo4j+s://60318b06.databases.neo4j.io
    # NEO4J_USERNAME=neo4j
    # NEO4J_PASSWORD=Cq-Of1FHfShywvyaq0RpAJaOmIHA6ZVPW9yB6UxxXs8
    # AURA_INSTANCENAME=Instance01

    # "neo4j+s://<number>.databases.neo4j.io"
    uri = "neo4j+s://60318b06.databases.neo4j.io"

    # "<Username for Neo4j Aura instance>"
    user = "neo4j"
    
    # "<Password for Neo4j Aura instance>"
    password = "Cq-Of1FHfShywvyaq0RpAJaOmIHA6ZVPW9yB6UxxXs8"
    app = App(uri, user, password)
    # app.create_friendship("Michael", "Luke")
    # app.find_person("Luke")
    app.create_judgement(
        {"judgement": "judgement 1", "date": "january 1 2022"},
        {"judgement": "judgement 2", "date": "january 2 2022"},
    )
    app.close()