import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_value(conn, data):
    sql = """ INSERT INTO `values`(title, description)
              VALUES(?,?) """
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    return cur.lastrowid


def create_principle(conn, data):
    sql = """ INSERT INTO `principles`(title, description)
              VALUES(?,?) """
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    return cur.lastrowid


def main():
    database = r"agile-project.db"

    sql_create_values_table = """ CREATE TABLE IF NOT EXISTS `values` (
                                    id integer PRIMARY KEY,
                                    title string NOT NULL,
                                    description text
                                ); """

    sql_create_principles_table = """ CREATE TABLE IF NOT EXISTS principles (
                                    id integer PRIMARY KEY,
                                    title string NOT NULL,
                                    description text
                                ); """

    # create a database connection
    conn = create_connection(database)
    with conn:

        create_table(conn, sql_create_values_table)
        create_table(conn, sql_create_principles_table)

        # insert 4 agile values
        value1 = (
            "Individuals and Interactions Over Processes and Tools",
            "Valuing people more highly than processes or tools is easy to understand because it is the people who respond to business needs and drive the development process.",
        )
        value2 = (
            "Working Software Over Comprehensive Documentation",
            "Historically, enormous amounts of time were spent on documenting the product for development and ultimate delivery.",
        )
        value3 = (
            "Customer Collaboration Over Contract Negotiation",
            "Negotiation is the period when the customer and the product manager work out the details of a delivery, with points along the way where the details may be renegotiated.",
        )
        value4 = (
            "Responding to Change Over Following a Plan",
            "Traditional software development regarded change as an expense, so it was to be avoided.",
        )
        create_value(conn, value1)
        create_value(conn, value2)
        create_value(conn, value3)
        create_value(conn, value4)

        # insert 12 agile principles
        principle1 = (
            "Customer satisfaction through early and continuous software delivery",
            "Customers are happier when they receive working software at regular intervals, rather than waiting extended periods of time between releases.",
        )
        principle2 = (
            "Accommodate changing requirements throughout the development process",
            "The ability to avoid delays when a requirement or feature request changes.",
        )
        principle3 = (
            "Frequent delivery of working software",
            "Scrum accommodates this principle since the team operates in software sprints or iterations that ensure regular delivery of working software.",
        )
        principle4 = (
            "Collaboration between the business stakeholders and developers throughout the project",
            "Better decisions are made when the business and technical team are aligned.",
        )
        principle5 = (
            "Support, trust, and motivate the people involved",
            "Motivated teams are more likely to deliver their best work than unhappy teams.",
        )
        principle6 = (
            "Enable face-to-face interactions",
            "Communication is more successful when development teams are co-located.",
        )
        principle7 = (
            "Working software is the primary measure of progress",
            "Delivering functional software to the customer is the ultimate factor that measures progress.",
        )
        principle8 = (
            "Agile processes to support a consistent development pace",
            "Teams establish a repeatable and maintainable speed at which they can deliver working software, and they repeat it with each release.",
        )
        principle9 = (
            "Attention to technical detail and design enhances agility",
            "The right skills and good design ensures the team can maintain the pace, constantly improve the product, and sustain change.",
        )
        principle10 = (
            "Simplicity",
            "Develop just enough to get the job done for right now.",
        )
        principle11 = (
            "Self-organizing teams encourage great architectures, requirements, and designs",
            "Skilled and motivated team members who have decision-making power, take ownership, communicate regularly with other team members, and share ideas that deliver quality products.",
        )
        principle12 = (
            "Regular reflections on how to become more effective",
            "Self-improvement, process improvement, advancing skills, and techniques help team members work more efficiently.",
        )
        create_principle(conn, principle1)
        create_principle(conn, principle2)
        create_principle(conn, principle3)
        create_principle(conn, principle4)
        create_principle(conn, principle5)
        create_principle(conn, principle6)
        create_principle(conn, principle7)
        create_principle(conn, principle8)
        create_principle(conn, principle9)
        create_principle(conn, principle10)
        create_principle(conn, principle11)
        create_principle(conn, principle12)


if __name__ == "__main__":
    main()
