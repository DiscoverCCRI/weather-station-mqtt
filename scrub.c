/**
 * @file
 * This file performs cleanup on the insertions made from the weather
 * station MQTT subscribe code. Detecting outliers/anomalies in data
 *
 * NOTE: this program requires root privledges to your MariaDB/MySQL
 * instance
 */

#include <mysql.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


/**
 * @brief Establishes a MariaDB/MySQL connection and returns a MYSQL pointer
 * @param addr server address
 * @param user user name
 * @param pass user password
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
 * @brief Returns an array of strings containing the names of the columns in mqtt_data
 * @param con A pointer to a MySQL connection object.
 * @return A pointer to an array of strings containing the names of the columns
 *
 */
char **col_names(MYSQL *con) {
    // MYSQL result struct
    MYSQL_RES *result;
    // MYSQL field struct
    MYSQL_FIELD *field;
    int num_fields;
    // result array
    char **result_arr;

    // query mqtt_data table 
    if (mysql_query(con, "SELECT * FROM mqtt_data LIMIT 0")) {
        fprintf(stderr, "%s\n", mysql_error(con));
        exit(1);
    }
    // stores query result in struct
    result = mysql_store_result(con);
    if (result == NULL) {
        fprintf(stderr, "%s\n", mysql_error(con));
        exit(1);
    }

    // allocate memory for result array
    result_arr = (char **) malloc(num_fields * sizeof(char *));
    num_fields = mysql_num_fields(result);

    // iterate through column names (fields) and populate the result array
    for (int i = 0; i < num_fields; i++) {
        // field for current column index
        field = mysql_fetch_field_direct(result, i);

        if (field == NULL) {
            fprintf(stderr, "%s\n", mysql_error(con)); 
            exit(1);
        }
    
        // allocate memory for result array elements
        result_arr[i] = (char *) malloc(strlen(field->name) + 1);
        // copy column name to result array
        strcpy(result_arr[i], field->name);
    }
    
    // free allocated result memory
    mysql_free_result(result);
    return result_arr;
}

/*
outliers(MYSQL *con, column_name, ) {
    // define struct for min/max for ranges

    // for all 20 readings, establish baseline set of ranges, given
    // column names, check if the rows for a given column are in range
    for (i=0; i < num of rows for given col; i++) {
        if (row val is not in range) {
            // print some pretty table of information
        }
    }
    // think of way to return outliers in a easy to use format
}
*/

/*
scrubber(MYSQL *con) {
    // parse column names

    // define outlier ranges for the 20 fields

    // given column name, check the colums rows for outliers

    // check for NULL/empty data?

    // <---->
    // Several optimizations can be made
    // - Merge sort approach, partition data (rows) of each column
    // - Spawn worker threads for equal parts of the rows
    // - ThreadPool, for each column name clean it up, each function call can
    // be a thread

}
*/

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
    char **col_arr = col_names(db_con);

    // print column names
    for (int i = 0; col_arr[i] != NULL; i++) {
        printf("%s\n", col_arr[i]);
        // free the memory allocated for each element
        free(col_arr[i]);
    }
    

    // call scrubber with connection object?

    // free memory allocated for column array
    free(col_arr);
    // close connection
    mysql_close(db_con);

    return 0;
}

