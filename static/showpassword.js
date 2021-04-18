//for show pass word in signup
function showpasforsignup()
{
  
  var password=document.getElementById("psw");
  var password2=document.getElementById("psw2");
  var x=document.getElementById("box1").checked;
  if(x==true)
  {
    password.type="text";
    password2.type="text";
    
  }
  else
  {
    password.type="password";
    password2.type="password";
    
  }
}
  //for show password in login
  function showpasforlogin()
{
  var password=document.getElementById("loginpsw2");
  var x=document.getElementById("box2").checked;
  if(x==true)
  {
    password.type="text";
  }
  else
  {
    password.type="password";    
  }
}

