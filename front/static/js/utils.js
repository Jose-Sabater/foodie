function get_token(){
    let token = localStorage.getItem('token');
    return token
}

function submit_form(category,token){
    // token=get_token();
    console.log(category+"-token"+ token);
    document.getElementById(str(category)+"-token").value = token;
    document.getElementById(category+"-form").submit();
  }
let token = localStorage.getItem('token');
let username = localStorage.getItem('uname');
console.log("Hello");

function showmessage(id,message){
  document.getElementById(id).textContent = message;
}



