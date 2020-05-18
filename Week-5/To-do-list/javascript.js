function method() {
    let variable = document.getElementById("list").innerHTML;
    let input = document.getElementById("box").value;
    variable += "<li onclick=\"this.classList.toggle(\'checked\')\">"+input+"<button id=\'close\' onclick=\"this.parentElement.style.display=\'none\'\" style=\'font-size:15px; float: right;\'><i class=\'fas fa-trash-alt\'></i></button></li>";
    document.getElementById("list").innerHTML = variable;
    var list = document.querySelector('ul');
    console.log(list);
    list.addEventListener('click', function(event) {
        if (event.target.tagName === 'li') {
            event.target.classList.toggle('checked');
        } else {
            console.log("Come on");
        }
    });
    document.getElementById("box").value = "";
    event.preventDefault();
    return false;
}