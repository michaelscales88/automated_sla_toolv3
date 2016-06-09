Mike's Streamlined Reporting Tool:

Purpose: 
Takes excel spreadsheets and parses through each row to extract the necessary information to generate the daily SLA report.

Acknowledgements:
Alex Mays

Notes:
Excel spreadsheets must be in xlsx format for the program to work.*
Excel spreadsheets require some formatting. Requirements will be noted below.

*Conversion software that will take the xls format spreadsheets and convert them into xlsx is included in this directory.

__TABLE OF CONTENTS__
	
* Formatting Requirements
** Procedure
*** Adding New Clients

*Formatting requirements:

Call Details needs to be titled: "Call Details.xlsx"
- No changes required

Abandon Group needs to be titled: "Group Abandoned Calls.xlsx"
- All call IDs must be moved to "ECA Gen"
- Delete each tab after the contents have been moved to ECA Gen. Before processing Abandon Group should have ECA Gen + Summary tabs only.
- Remove duplicate Call IDs by selecting column A and removing duplicates by "Call" Field

Cradle to Grave needs to be titled: "Cradle to Grave.xlsx"
- No changes required

Hunt Group Reports titles need to match the format in the client_file_list located in the bin Column B.
- Files need to be converted into xlsx format. (Use OFC Tools located in this directory in Converter)*1

**Procedure:

*1 OFC Tools: Conversion software is included. To convert files:

	1. If required change the directory source/destination for converted files. This can be done by opening 		the ofc ini file located in Converter>Tools

	2. Through the cmd line run cd [current directory]/Daily SLA Parser/converter/tools

	3. Run 'ofc'

	4. Files are set to output into the C:\Users\mscales\Desktop\Development\Daily SLA 	Parser\converted_files_come_here.

2. Put your source files into their respective directories.
	1. Hunt Group Reports (converted into xlsx) into: hunt_group_dir
	2. Call Details/Cradle to Grave/Abandon Group go into: Add_CDetails_AbandonGRP_C2Grave

3. cd into the bin folder and run 'cli.py'

4. Enter the date and follow on-screen prompts.

5. Once report has been written you should check that the ticker totals = the calls answered amount. Written files go to the output folder. 

6. In the Archive locate the current day's Abandon Group report. Check for voicemails and use the report to remove lost calls as required.

*** Adding New Clients:
1. In the bin folder locate the client_file_list
2. Add the client number and hunt group path (Insert the client in the list in the order in which it will appear on the final report)
3. Add the client to the template file located in the bin (Data and Report tabs)
5. Check that the cells on the report tab are pointing to the correct cell on the data tab
6. Ensure that the averages on the report tab are adjusted for the additional client

* Note that the data is printed in order. If the sequence of the client list is different from the excel template your output will not print out correctly.