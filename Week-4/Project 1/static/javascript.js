let value = [];
function check() {
    const request = new XMLHttpRequest();
    request.open('POST', '/api/search')
    request.setRequestHeader("Content-Type", "application/json");
    let search = document.querySelector('#Search').value;
    if (document.querySelector('#drop').value == "ISBN") {
        request.send(JSON.stringify({"searchby" : "ISBN", "search" : search}));
    } else if (document.querySelector('#drop').value == "Title") {
        request.send(JSON.stringify({"searchby" : "Title", "search" : search}));
    } else {
        request.send(JSON.stringify({"searchby" : "Author", "search" : search}));
    }
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        let isbns = data.isbns;
        let titles = data.titles;
        let authors = data.authors;
        let string = "";
        value = [];
        for (let i = 0; i < isbns.length; i++) {
            // console.log(typeof isbns[i]);
            value.push(isbns[i]);
            string += "<tr>";
            string += "<th scope=\"row\">"+(i+1)+"</th>";
            string += "<td><a href=\"javascript:method("+i+")\">"+isbns[i]+"</a></td>";
            string += "<td>"+titles[i]+"</td>";
            string += "<td>"+authors[i]+"</td>";
            string += "</tr>";
        }
        document.getElementById("panel-heading").innerHTML = "Showing "+isbns.length+" results for \""+search+"\"";
        document.querySelector('#tbody').innerHTML = string;
    }
    document.getElementById("tableSection").style.display = "block";
    document.getElementById("secondpart").style.display = "none";
    event.preventDefault();
    // location.href='#tableSection';
    return true;
}

function method(index) {
    // console.log(typeof index);
    // console.log(index);
    let search = "";
    if (typeof index === 'number') {
        search = String(value[index]);
    }
    else {
        search = index;
    }
    let rates = document.getElementsByName('rate');
    rates.forEach((rate) => {
        if(rate.checked){
            rate.checked = false;
        }
    })
    document.getElementById('reviewfield').value = "";
    const request = new XMLHttpRequest();
    request.open('POST', '/api/search')
    request.setRequestHeader("Content-Type", "application/json");
    request.send(JSON.stringify({"searchby" : "ISBN", "search" : search}));
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        let string = "";
        string += "<h3 id=form-isbn class=\"form-control\">ISBN &ensp;&emsp;&emsp;- &emsp;"+data.isbns[0]+"</h3>";
        string += "<h3 class=\"form-control\">Title &ensp;&emsp;&emsp;&nbsp;- &emsp;"+data.titles[0]+"</h3>";
        string += "<h3 class=\"form-control\">Author &ensp;&emsp;- &emsp;"+data.authors[0]+"</h3>";
        string += "<h3 class=\"form-control\">Year &ensp;&emsp;&emsp;&nbsp;- &emsp;"+data.years[0]+"</h3>";
        document.querySelector('#block').innerHTML = string;
    }
    const xml = new XMLHttpRequest();
    xml.open('POST', '/api/book')
    xml.setRequestHeader("Content-Type", "application/json");
    xml.send(JSON.stringify({"isbn" : search}));
    xml.onload = () => {
        const data = JSON.parse(xml.responseText);
        // console.log(data); 
        let users = data.users;
        // log.console(users);
        let ratings = data.ratings;
        let reviews = data.reviews;
        let string = "";
        let user = document.querySelector('h5').innerText;
        user = user.substring(6);
        let boolean = false;
        for (let i = 0; i < users.length; i++) {
            if (user === users[i]) {
                boolean = true;
            }
            string += "<tr>";
            string += "<th scope=\"row\">"+(i+1)+"</th>";
            string += "<td>"+users[i]+"</td>";
            string += "<td>";
            for (let j = 0; j < ratings[i]; j++) {
                string += "<span class=\"fa fa-star checked\" style=\"color: #fff176;\"></span>"
            }
            for (let j = 0; j < (5-ratings[i]); j++) {
                string += "<span class=\"fa fa-star\"></span>"
            }
            string += "</td>";
            string += "<td>"+reviews[i]+"</td>";
            string += "</tr>";
            // console.log(string);
        }
        document.querySelector('#reviewtbody').innerHTML = string;
        if (boolean === false) {
            document.getElementById("reviewedText").style.display = "none";
            document.getElementById("secondtable").style.top = "150px";
            document.getElementById("hide").style.display = "block";
        } else {
            document.getElementById("hide").style.display = "none";
            document.getElementById("secondtable").style.top = "475px";
            document.getElementById("reviewedText").style.display = "block";
        }
        document.getElementById("secondpart").style.display = "block";
        event.preventDefault();
        return true;
    }
}

function func() {
    // console.log("Come on");
    let user = document.querySelector('h5').innerText;
    user = user.substring(6);
    let isbn = document.querySelector('#form-isbn').innerText;
    isbn = isbn.substring(11);
    let rating = 1;
    let rates = document.getElementsByName('rate');
    rates.forEach((rate) => {
        if(rate.checked){
            rating = rate.value;
        }
    })
    let review = document.getElementById('reviewfield').value;
    // console.log(user);
    // console.log(rating);
    // console.log(review); 
    // console.log(isbn);
    const request = new XMLHttpRequest();
    request.open('POST', '/api/submit_review');
    request.setRequestHeader("Content-Type", "application/json");
    request.send(JSON.stringify({"user" : user, "isbn" : isbn, "rating" : rating, "review" : review}));
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        let message = data.Message;
        if (message === "Successfully Reviewed") {
            document.getElementById("hide").style.display = "none";
            document.getElementById("secondtable").style.top = "475px";
            // document.getElementById("reviewedText").style.display = "block";
        }
    }
    setTimeout(() => {method(isbn)}, 1000);
    // rates.forEach((rate) => {
    //     if(rate.checked){
    //         rate.checked = false;
    //     }
    // })
    // document.getElementById('reviewfield').value = "";
    // method(isbn);
    // method(isbn);
    event.preventDefault();
    return true;
}