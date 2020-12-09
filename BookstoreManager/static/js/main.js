// Global variable that any function can be accessible
var inputID = 0;
var totalItem = 0;
var dt = new Date();
document.getElementById("invoice-date").innerHTML = (("0"+dt.getDate()).slice(-2)) +"."+ (("0"+(dt.getMonth()+1)).slice(-2)) +"."+ (dt.getFullYear()) +" "+ (("0"+dt.getHours()).slice(-2)) +":"+ (("0"+dt.getMinutes()).slice(-2));


// Ẩn hiện menu bên
$(function() {
  // Sidebar toggle behavior
  $('#sidebarCollapse').on('click', function() {
    $('#sidebar, #content').toggleClass('active');
  });
})


// Reset everything to default value
function init() {
    inputID = 0;
    totalItem = 0;
}

// Add a HTML element
function addProduct() {
  const div = document.createElement('div');
  div.className = 'form-group d-flex';
  div.innerHTML = `
        <input type="text" class="form-control mr-2" name=` +
        inputID +
        ` placeholder="Mã sản phẩm">
        <input type="button" class="btn btn-secondary" value="Xóa" onclick="removeRow(this)" />
  `;
  inputID++;
  totalItem++;
  document.getElementById('sell_form').appendChild(div);
}

// Remove a HTML element
function removeRow(input) {
  totalItem--;
  document.getElementById('sell_form').removeChild(input.parentNode);
}

// Print current date time
function printDate() {
    date = Date();
    document.getElementById("invoice-date").innerHTML = date;
    return date;
}


// Promises, have a catch()
function myFunction(id) {
    fetch('/api/get_value', {
        method: "post",
        body: JSON.stringify({
            "id": id,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data);
        var sometime = document.getElementById("something");
        sometime.innerText = `${data.message}`;
    }).catch(err => {
        console.log(err);
    })

    // promise --> await/async
}
