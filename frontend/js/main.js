const url = new URL('http://127.0.0.1:5000/definitions')
var params = []


let input = document.getElementById('input_string');
input.addEventListener('input', onChange, true);

function onChange() {
    console.info(this.value);

    params = [['word', this.value]]
    url.search = new URLSearchParams(params)

    send_request(url)
        .then(data => {
            remove_table()
            if (data["success"] == true) {
                console.log(data["definitions"])
                create_table(data["definitions"])
            }
            else {
                console.log(data["error_message"])
                create_table([data["error_message"]])

            }
        })
}

function send_request(backend_url) {
    return fetch(backend_url)
        .then(response => {
            return response.json()
        })
}


function remove_table() {
    let answer_table_list = document.getElementById("answer_table").querySelectorAll("li");
    answer_table_list.forEach((item) => {
        item.parentNode.removeChild(item);
    });
}


function create_table(list) {

    let ul = document.getElementById("answer_table");

    list.forEach((item) => {
        let li = document.createElement("li");
        li.appendChild(document.createTextNode(item));
        li.classList.add("list-group-item")
        ul.appendChild(li);
    })
}

