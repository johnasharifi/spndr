''' This module acts as a wrapper for the psycopg2 module that allows us to work with our PostgreSQL database.


    FUNCTIONS IN THIS MODULE

    1. getTransactionState() - Retrieves the transaction state of the sender of the message currently being processed.
                               If the sender doesn't have an ongoing transaction, it will return None.

    2. createNewTransaction() - If the sender has sent 'new' when their transaction state is none. A new transaction
                                will be initiated for them, and their transaction state will be increased to 0.

    3. updateTransaction() - Increments the transaction state and commits the newly provided date from the user to the 
                             current_transaction database.
                             It also calls commitTransaction() when a transaction has been completed. That is, when
                             the transaction state equals 4.

    4. commitTransaction() - Once a transaction has been completed. The transaction information is taken from the 
                             current_transaction database and committed to the transactions database.

    5. abortTransaction() - Aborts an ongoing transaction when the user gives the !abort command.

    6. checkCreds() - This function checks whether a particular sender is registered with the service or not.

    7. createAccount() - This function registers a sender if they agree to join spndr.

    8. deleteNewSender() - This function removes an unregistered sender if they don't want to sign up for spndr.

    9. lastTenTransactions() - This function retrieves upto 10 of the latest transactions made my a specific user.

    10. deleteUser() - This function removes a user from the database, essentially deleting the user's account.
'''

import psycopg2 as pg2 
import os

def getTransactionState(sender_id):
    get_transaction_state_script = open(os.getcwd()+'//sql_scripts//get_transaction_state.sql').read()
    con = pg2.connect(database='spndr', user='postgres', password='password')
    curs = con.cursor()
    curs.execute(get_transaction_state_script, {"sender_id":sender_id})
    query_result = curs.fetchone()
    if query_result is None:
        con.commit(); curs.close(); con.close()
        return None
    transaction_state = query_result[0]
    con.commit(); curs.close(); con.close()
    return transaction_state


def createNewTransaction(sender_id):
    create_new_transaction_script = open(os.getcwd()+'//sql_scripts//create_new_transaction.sql').read()
    con = pg2.connect(database='spndr', user='postgres', password='password')
    curs = con.cursor()
    curs.execute(create_new_transaction_script, {"sender_id":sender_id})
    con.commit(); curs.close(), con.close()

def updateTransaction(sender_id, message, previous_transaction_state):
    con = pg2.connect(database='spndr', user='postgres', password='password')
    curs = con.cursor()

    if previous_transaction_state == 0:
        add_product_service_script = open(os.getcwd()+'//sql_scripts//add_product_service.sql').read()
        curs.execute(add_product_service_script, {"prod_serv":message, "sender_id":sender_id})
        
    if previous_transaction_state == 1:
        add_price_script = open(os.getcwd()+'//sql_scripts//add_price.sql').read()
        curs.execute(add_price_script, {"price":float(message), "sender_id":sender_id})

    if previous_transaction_state == 2:
        add_vendor_script = open(os.getcwd()+'//sql_scripts//add_vendor.sql').read()
        curs.execute(add_vendor_script, {"vendor":message, "sender_id":sender_id})

    if previous_transaction_state == 3:
        add_category_script = open(os.getcwd()+'//sql_scripts//add_category.sql').read()
        curs.execute(add_category_script, {"category":message, "sender_id":sender_id})

    
    con.commit(); curs.close(); con.close()

    transaction_state = getTransactionState(sender_id)
    if transaction_state == 4:
        commitTransaction(sender_id)

def commitTransaction(sender_id):
    con = pg2.connect(database='spndr', user='postgres', password='password')
    cur = con.cursor()

    commit_transaction_script = open(os.getcwd()+'//sql_scripts//commit_transaction.sql').read()
    delete_completed_transaction_script = open(os.getcwd()+'//sql_scripts//delete_completed_transaction.sql').read()
    cur.execute(commit_transaction_script, {"sender_id":sender_id})
    cur.execute(delete_completed_transaction_script, {"sender_id":sender_id})

    con.commit(); cur.close(); con.close()

def abortTransaction(message, sender_id, transaction_state):
    con = pg2.connect(database='spndr', user='postgres', password='password')
    cur = con.cursor()

    if message.lower() == '!abort':
        init_abort_transaction_script = open(os.getcwd()+'//sql_scripts//init_abort_transaction.sql').read()
        cur.execute(init_abort_transaction_script, 
                    {"previous_transaction_state":transaction_state, "sender_id":sender_id})
    
    if transaction_state == 5:
        if message == 'y':
            confirm_abort_transaction_script = open(os.getcwd()+'//sql_scripts//confirm_abort_transaction.sql').read()
            cur.execute(confirm_abort_transaction_script, {"sender_id":sender_id})

        elif message == 'n':
            stop_abort_transaction_script = open(os.getcwd()+'//sql_scripts//stop_abort_transaction.sql').read()
            cur.execute(stop_abort_transaction_script, {"sender_id":sender_id})
    
    con.commit(); cur.close(); con.close()

def checkCreds(sender_id):
    con = pg2.connect(database='spndr', user='postgres', password='password')
    cur = con.cursor()
    check_creds_script = open(os.getcwd()+'//sql_scripts//check_creds.sql').read()
    cur.execute(check_creds_script, {"sender_id":sender_id})
    creds_exist = cur.fetchone()[0]
    con.commit(); cur.close(); con.close()
    if creds_exist:
        return True
    return False

def createAccount(sender_id):
    con = pg2.connect(database='spndr', user='postgres', password='password')
    cur = con.cursor()
    create_account_script = open(os.getcwd()+'//sql_scripts//create_account.sql').read()
    cur.execute(create_account_script, {"sender_id":sender_id})
    con.commit(); cur.close(); con.close()
    
def deleteNewSender(sender_id):
    con = pg2.connect(database='spndr', user='postgres', password='password')
    cur = con.cursor()
    delete_new_sender_script = open(os.getcwd()+'//sql_scripts//delete_new_sender.sql').read()
    cur.execute(delete_new_sender_script, {"sender_id":sender_id})
    con.commit(); cur.close(); con.close()

def lastTenTransactions(sender_id):
    con = pg2.connect(database='spndr', user='postgres', password='password')
    cur = con.cursor()
    get_last_ten_transactions_script = open(os.getcwd()+'//sql_scripts//get_last_ten_transactions.sql').read()
    cur.execute(get_last_ten_transactions_script, {"sender_id":sender_id})
    spending_data = cur.fetchmany(10)
    return spending_data
    con.commit(); cur.close(); con.close()

def deleteUser(sender_id, state):
    con = pg2.connect(database='spndr', user='postgres', password='password')
    cur = con.cursor()
    if state == 1:
        init_user_deletion_script = open(os.getcwd()+'//sql_scripts//init_user_deletion.sql').read()
        cur.execute(init_user_deletion_script, {"sender_id":sender_id})
    elif state == 2:
        delete_user_script = open(os.getcwd()+'//sql_scripts//delete_user.sql').read()
        cur.execute(delete_user_script, {"sender_id":sender_id})
    else:
        abort_user_deletion_script = open(os.getcwd()+'//sql_scripts//abort_user_deletion.sql').read()
        cur.execute(abort_user_deletion_script, {"sender_id":sender_id})


    con.commit(); cur.close(); con.close()


    










    


