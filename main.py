from Tkinter import *;
import os;
import json;

FILE="properties.json"

APPLICATION_TYPE=["Reporting", "Framework"];
DEPLOY="Deploy";DEPLOY_RESTART="Deploy and Restart";RESTART="Restart";START="Start";STOP="Stop";
PROCESS_TYPE=[DEPLOY_RESTART, DEPLOY, RESTART, STOP, START];
data={}

def getCustomerList(file):
	with open(file) as data_file:
		global data
		data = json.load(data_file)

	customer_list=[];
	for i in data["Customers"]:
		customer_list.append(str(i));

	return customer_list

def getCommand(neo, process_type, account, application, user, password, host, source):
	neo_command = neo+" ";
	neo_command = neo_command + process_type + " ";
	neo_command = neo_command + "--account " + account + " ";
	neo_command = neo_command + "--application " + application + " ";
	if(user):
		neo_command = neo_command + "--user " + user + " ";
	if(password):
		neo_command = neo_command + "--password " + password + " ";
	neo_command = neo_command + "--host " + host + " ";
	neo_command = neo_command + "--source " + source;
	print neo_command
	return neo_command;

def execute(customer, application_type, process_type):
	os.system("notify-send 'Process started...'");
	global data;
	customer_data=data["Customers"];
	print customer_data;
	neo=data["neo_command"];
	host=data["host"];

	customer_app_data=customer_data[customer][application_type];
	account=customer_app_data['account'];
	application=customer_app_data['application'];

	user = (customer_app_data['user'] if customer_app_data['user']!="" else data['user']);
	password=(customer_app_data['password'] if customer_app_data['password']!="" else data['password']);

	source=data["reporting_source"] if application_type=="Reporting" else data["framework_source"]

	flag=0;
	if(process_type==DEPLOY_RESTART):
		flag=1;
		process_type=DEPLOY;

	neo_command = getCommand(neo, process_type.lower(), account, application, user, password, host, source);
	
	if(flag):
		neo_command = getCommand(neo, 'restart', account, application, user, password, host, source);

master = Tk();

customer_list = getCustomerList(FILE);

customer = StringVar(master)
customer.set(customer_list[0])

w = OptionMenu(master, customer, *customer_list)
w.pack()

# for second drop down
application_type = StringVar(master)
application_type.set(APPLICATION_TYPE[0])

w = OptionMenu(master, application_type, *APPLICATION_TYPE)
w.pack()

#for third drop down
process_type = StringVar(master)
process_type.set(PROCESS_TYPE[0])

w = OptionMenu(master, process_type, *PROCESS_TYPE)
w.pack();

b = Button(master, text="Execute", command=lambda: execute(customer.get(), application_type.get(), process_type.get()));
b.pack();

mainloop();