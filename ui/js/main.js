//
// Main javascript file
//

function removeChildren(parentId) {
    var myNode = document.getElementById(parentId);
    while (myNode.firstChild) {
        myNode.removeChild(myNode.firstChild);
    }
}


function getUsers() {
    //
    // GET full list of users and show them on the table
    //
    // fetch("http://app:60010/api/v1/users",
    fetch("http://127.0.0.1:60010/api/v1/users",
        {
            mode: "cors",
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {
            // console.log("GET response:", JSON.stringify(myJson));

            // Clean table before inserting users into the table
            removeChildren("tableBody");

            // Populate table with the users returned by the API
            var tbody = document.getElementById("tableBody");
            for (var i = 0; i < myJson.length; i++) {
                // console.log(myJson[i]);

                tbody.innerHTML += `<tr>
                            <td>${myJson[i]["id"]}</td>
                            <td>${myJson[i]["username"]}</td>
                            <td>${myJson[i]["email"]}</td>
                            <td>${myJson[i]["dob"]}</td>
                            <td>${myJson[i]["address"]}</td>
                            </tr>`;
            }
        });
}

function addUser() {
    //
    // POST new user
    //
    // var urlUser = "http://app:60010/api/v1/users";
    var urlUser = "http://127.0.0.1:60010/api/v1/users";
    var payload = {
        username: $("#inputUsername").val(),
        email: $("#inputEmail").val(),
        dob: $("#inputBirthdate").val(),
        address: $("#inputAddress").val()
    };

    // console.log("payload:", payload);
    var data = new FormData();
    data.append("json", JSON.stringify(payload));

    fetch(urlUser,
        {
            method: "POST",
            headers: { "Accept": "application/json", "Content-Type": "application/json" },
            body: JSON.stringify(payload),
            mode: "cors"
        })
        .then(function (res) {
            // console.log("res:", res)
            return res.json();
        })
        .then(function (data) {
            var color = "";
            console.log("DATA from response: ", data)
            if (data.code == 200) {
                color = "success";
            }
            else {
                color = "danger";
            }
            addNotification(data.code, data.message, color)

            getUsers();

        });
}

function removeAlert() {
    $("#alert").remove()
}

function addNotification(code, msg, color) {
    $("#notification").html(`<span style="float: right; text-align: left;" class="label label-${color}">Code: ${code}<br>Msg: ${msg}</span>
    `
    )
}

$(document).ready(function () {

    console.log("Running ui!");
    getUsers();

    $("#addButton").on("click", function () {
        removeAlert();
        addUser();
    });

    $(".input-group.date").datepicker({ format: "dd.mm.yyyy" });

});
