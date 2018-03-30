# Import modules for CGI handling 
import cgi, cgitb 
 
 # Create instance of FieldStorage 
form = cgi.FieldStorage() 
 
 # Get data from field 'name' 
name = form.getvalue('name') 
 
 # Get data from field 'address' 
address = form.getvalue('address') 
 
 # Get data from field 'phone' 
phone = form.getvalue('phone') 
 
 # Get data from field 'email' 
email = form.getvalue('email')

print form, name, address, phone, email
