function loginAlert()
{
var username=document.getElementById('username').value;
var password=document.getElementById('password').value;

if(!username || !password)
{
alert('Please enter valid credentials!')
}
else
{
alert('Login successfull!');
}

}
