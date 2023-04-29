/**
 * @file
 * This file performs cleanup on the insertions made from the weather
 * station MQTT subscribe code. Detecting outliers/anomalies in data
 *
 * NOTE: this program requires root privledges to your MariaDB/MySQL
 * instance
 */

// MYSQL header
#include <mysql.h>
#include <stdio.h>
#include <stdlib.h>


/**
 * @brief Establishes a MySQL connection and returns a MYSQL pointer.
 *
 * @param addr The MySQL server address.
 * @param user The MySQL user name.
 * @param pass The MySQL user password.
 * @return A MYSQL pointer if the connection is successful, NULL otherwise.
 */
MYSQL *db_connect(char *addr, char *user, char *pass, char *db) {
    // mysql connection object 
    MYSQL *con = mysql_init(NULL);
    
    // verify object is initialized
    if (!con) {
        fprintf(stderr, "%s\n", mysql_error(con));
        exit(1);
    }

    // establish connection, close & exit if not successful
    if (!mysql_real_connect(con, addr, user, pass, db, 0, NULL, 0 )) {
        fprintf(stderr, "%s\n", mysql_error(con));
        mysql_close(con);
        exit(1);
    }
    else {
        printf("\n[+] Connection SUCCESS\n");
    }
    // return connection object
    return con;
}

/**
 * @brief Retrieve the column names from a SQL table
 * @param con A MySQL struct pointer representing the database connection
 * @return MYSQL_RES struct pointer coontaining query
 */
MYSQL_RES *cols(MYSQL *con) {
    MYSQL_RES *result;
    MYSQL_FIELD *field;
    int num_fields;
    int i;

    if (mysql_query(con, "SELECT * FROM mqtt_data LIMIT 0")) {
        fprintf(stderr, "%s\n", mysql_error(con));
        return NULL;
    }

    result = mysql_store_result(con);
    if (result == NULL) {
        fprintf(stderr, "%s\n", mysql_error(con));
        return NULL;
    }

    num_fields = mysql_num_fields(result);
    for (i = 0; i < num_fields; i++) {
        field = mysql_fetch_field_direct(result, i);
        if (field == NULL) {
            fprintf(stderr, "%s\n", mysql_error(con));
            return NULL;
        }
        printf("%s \n", field->name);
    }

    mysql_free_result(result);
    return result;
}

MYSQL_RES* col_name(MYSQL* con) {
    MYSQL_RES* result;
    MYSQL_FIELD* field;
    int num_fields;
    int i;

    if (mysql_query(con, "SELECT * FROM mqtt_data LIMIT 0")) {
        fprintf(stderr, "%s\n", mysql_error(con));
        return NULL;
    }

    result = mysql_store_result(con);
    if (result == NULL) {
        fprintf(stderr, "%s\n", mysql_error(con));
        return NULL;
    }

    num_fields = mysql_num_fields(result);

    for (i = 0; i < num_fields; i++) {
        field = mysql_fetch_field_direct(result, i);
        if (field == NULL) {
            fprintf(stderr, "%s\n", mysql_error(con));
            return NULL;
        }
    }

    return result;
}

/**
 * @brief main()
 */
int main(int argc, char **argv) {
    char addr[] = "localhost";
    char user[] = "aba275";
    char pass[] = "";
    char db[] = "SEEED_WEATHER";
    char table[] = "mqtt_data";
    // establish connection
    MYSQL *db_con = db_connect(addr, user, pass, db);
    // query column names
    //MYSQL_RES *col_res = cols(db_con);
    

    MYSQL_RES *columns;
    MYSQL_ROW row;
    columns = col_name(db_con);
    int num_fields = mysql_num_fields(columns);

    while ((row = mysql_fetch_row(columns))) {
        for (int i = 0; i < num_fields; i++) {
            printf("%s ", row[i] ? row[i] : "NULL");
        }
        printf("\n");
    }

    free(columns);

    // scrubber(db_con)

    // close connection
    mysql_close(db_con);

    return 0;
}

