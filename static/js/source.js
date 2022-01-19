function toggle_Password() {
    var x = document.getElementById("passFunc");
    if (x.type === "password") {
        x.type = "text";
    }else {
        x.type = "password";
    }
}
