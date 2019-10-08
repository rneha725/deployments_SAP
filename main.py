from tkinter import *;
import os
import json
from tkinter import messagebox

FILE = "properties.json"

APPLICATION_TYPE = ["Reporting", "Framework"]
PROCESS_TYPE = {"DEPLOY": ["Deploy"], "DEPLOY_RESTART": ["Deploy and Restart"], "RESTART": ["Restart"],
                "START": ["Start"], "STOP": ["Stop"]}

data = {}


def write_to_file(account, application, source, host, user,password):
    if account== "" or application== "":
        messagebox.showinfo("Title", "Please fill mandatory fields")
        return


def add_customer():
    details = Toplevel();
    details.wm_title("Add Customer")
    account = Label(details, text="Account*").pack()
    account_entry = Entry(details)
    account_entry.pack()
    application = Label(details, text="Application*").pack()
    application_entry = Entry(details)
    application_entry.pack()
    source = Label(details, text="Source").pack()
    source_entry = Entry(details)
    source_entry.pack()
    host = Label(details, text="Host").pack()
    host_entry = Entry(details)
    host_entry.pack()
    user = Label(details, text="User").pack()
    user_entry = Entry(details)
    user_entry.pack()
    password = Label(details, text="Password").pack()
    password_entry = Entry(details)
    password_entry.pack()
    add_button = Button(details, text="Add", command=write_to_file(
        account_entry.get(), application_entry.get(), source_entry.get(), host_entry.get(), user_entry.get(),
        password_entry.get())).pack()

    return


def get_customer_list(file):
    with open(file) as data_file:
        global data
        data = json.load(data_file)
    customer_list = []
    for i in data["Customers"]:
        customer_list.append(str(i))
    return customer_list


def get_command(neo, process_type, account, application, user, password, host,
                source):
    neo_command = neo + " "
    neo_command = neo_command + process_type + " "
    neo_command = neo_command + "--account " + account + " "
    neo_command = neo_command + "--application " + application + " "
    if user:
        neo_command = neo_command + "--user " + user + " "
    elif password:
        neo_command = neo_command + "--password " + password + " "
    neo_command = neo_command + "--host " + host + " "
    if process_type == PROCESS_TYPE["DEPLOY"][0].lower():
        neo_command = neo_command + "--source " + source
    print(neo_command)
    os.system(neo_command);
    os.system("notify-send " + process_type + " done.")
    return neo_command


def execute(customer, application_type, process_type):
    os.system("notify-send 'Process started...'")
    global data
    customer_data = data["Customers"]
    neo = data["neo_command"]
    host = data["host"]
    customer_app_data = customer_data[customer][application_type];
    account = customer_app_data['account']
    application = customer_app_data['application'];

    user = (customer_app_data['user'] if customer_app_data['user'] != "" else data['user']);
    password = (customer_app_data['password'] if customer_app_data['password'] != "" else data['password']);

    source = data["reporting_source"] if application_type == "Reporting" else data["framework_source"]

    flag = 0;
    if process_type == PROCESS_TYPE["DEPLOY_RESTART"][0]:
        flag = 1;
        process_type = PROCESS_TYPE["DEPLOY"][0];

    neo_command = get_command(neo, process_type.lower(), account, application, user, password, host, source);

    if flag:
        neo_command = get_command(neo, 'restart', account, application, user, password, host, source);


master = Tk();

customer_list = get_customer_list(FILE);

customer = StringVar(master)
customer.set(customer_list[0])

w = OptionMenu(master, customer, *customer_list).pack()

# for second drop down
application_type = StringVar(master)
application_type.set(APPLICATION_TYPE[0])

w = OptionMenu(master, application_type, *APPLICATION_TYPE).pack()

# for third drop down
process_type = StringVar(master)
process_type.set(PROCESS_TYPE["DEPLOY"][0])
process_list = [];
for f in PROCESS_TYPE.values():
    process_list.append(f[0]);

w = OptionMenu(master, process_type, *process_list).pack();

b = Button(master, text="Execute",
           command=lambda: execute(customer.get(), application_type.get(), process_type.get())).pack();

menu = Menu(master)
menu.add_command(label="Add Customer", command=add_customer)
menu.add_command(label="Create properties.json")
add_customer_button = Button(master, text="Add Customer", command=add_customer).pack();
exit = Button(master, text="Exit", command=master.destroy).pack();

mainloop();
