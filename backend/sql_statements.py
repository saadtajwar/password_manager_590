def add_user_query(user_id, master_pass):
    return f"INSERT INTO users VALUES ({user_id}, {master_pass}); CREATE TABLE {user_id} (website text, alias text, password text, shared_with_me boolean, shared_with_others boolean, shared_list text[]);"

def add_password_query(user_id, website, alias, password):
    pass

def delete_password_query(user_id, website, alias):
    pass

def update_password_query(user_id, website, alias, password):
    pass
