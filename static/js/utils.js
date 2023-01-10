function check_response(result, code){
    if(code === 200) alert("Configure successfully!", "success")
    else if (code === 400) alert(result, "Warning")
    else alert("Something is wrong!", "danger")
}