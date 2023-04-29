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
MYSQL *db_connect(char *addr, char *user, char *pass) {
    // mysql connection object 
    MYSQL *con = mysql_init(NULL);
    
    // verify object is initialized
    if (!con) {
        fprintf(stderr, "%s\n", mysql_error(con));
        exit(1);
    }

    // establish connection, close & exit if not successful
    if (!mysql_real_connect(con, addr, user, pass, NULL, 0, NULL, 0 )) {
        fprintf(stderr, "%s\n", mysql_error(con));
        mysql_close(con);
        exit(1);
    }
    else {
        printf("\n[+] Connection SUCCESS\n");
    }
    return con;
}




int main(int argc, char **argv) {
    printf("VERSION: %s \n", mysql_get_client_info());

    char addr[] = "localhost";
    char user[] = "aba275";
    char pass[] = "";

    // establish connection
    MYSQL *db_con = db_connect(addr, user, pass);

    // scrubber(db_con)

    // close connection
    mysql_close(db_con);

    return 0;
}

