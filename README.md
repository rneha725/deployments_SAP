# Helper for deployments on neo platform
GUI using Tkinter for running deployment scripts

Prerequisites:
python, Tkinter, properties.json 

Execute:
`python main.py`

### A properties.json file has to be used for configuration
##### Format:

```
{
	"reporting_source":"<global war location for reporting application>/warname.war",
	"framework_source":"<global war location for framework application>/warname.war",
	"host":"<hostname for the SCP location>",
	"neo_command":"<location of neo.sh in local file system>/neo.sh",
	"password":"<global password for the global/local user>",
	"user":"<global user with global/local passwrod>",
	"Customers":{
		"<Customer-Name>":{
			"Reporting":{
				"application":"<application-name>",
				"account":"<account>",
				"source":"<if differnt than global>",
				"host":"<if differnt than global>",
				"user":"<if differnt than global>",
				"password":"<if differnt than global>"
			},
			"Framework":{
				"application":"",
				"account":"",
				"source":"",
				"host":"",
				"user":"",
				"password":""
			}
		},...
	}
}

Such a nice project!! Really loved it!!
```
