// Ẩn hiện menu bên
$(function() {
  // Sidebar toggle behavior
  $('#sidebarCollapse').on('click', function() {
    $('#sidebar, #content').toggleClass('active');
  });
})

// BIẾN TOÀN CỤC
// Khi ở trang sellview, giá trị inputID lưu thuộc tính name của ô input sản phẩm cuối cùng
// có thể sử dụng trong vòng lặp để duyệt lấy request phía backend
var inputID = 0;
// totalItem lưu tổng số ô input sản phẩm ở sellview
var totalItem = 0;
var dt = new Date();
// Gắn giá trị ngày tháng hiện tại vào document, DD/MM/YYY HH:MM
document.getElementById("invoice-date").innerHTML = (("0"+dt.getDate()).slice(-2)) +"."+ (("0"+(dt.getMonth()+1)).slice(-2)) +"."+ (dt.getFullYear()) +" "+ (("0"+dt.getHours()).slice(-2)) +":"+ (("0"+dt.getMinutes()).slice(-2));

// Khởi tạo các giá trị toàn cục về mặc định
function init() {
    inputID = 0;
    totalItem = 0;
}

// Thêm một trường mới để nhập mã sản phẩm, số lượng ở sellview
function addProduct() {
  const div = document.createElement('div');
  div.className = 'form-group d-flex';
  div.innerHTML = `
        <label for=
        ` + inputID + `
        >Mã sản phẩm: </label>
        <input type="text" class="form-control mx-2" name=
        ` + inputID + `
        placeholder="Ví dụ: 1234">
        <label for=
        ` + ('quantity-' + inputID) + `
        >Mã sản phẩm: </label>
        <input type="number" class="form-control mx-2" name=
        ` + ('quantity-' + inputID) + `
        min=1 max=5 value=1 placeholder="Tối đa 5">
        <input type="text" class="form-control mr-2" name=` +
        inputID +
        ` placeholder="Mã sản phẩm">
        <input type="button" class="btn btn-secondary" value="Xóa" onclick="removeRow(this)" />
  `;
  inputID++;
  totalItem++;
  document.getElementById('sell_form').appendChild(div);
}

// Xóa phần tử input được tạo bên trên
function removeRow(input) {
  totalItem--;
  document.getElementById('sell_form').removeChild(input.parentNode);
}

// UNSTABLE/DEVELOPING CODE BELOW

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

// |====================|
// | PHÂN HỆ KHÁCH HÀNG |
// |====================|




//  ------------------------------------------------------------------------ Customer   -----------------------------------
var globalCounter = 0;
function inc() {
    globalCounter++;
    return globalCounter;
}

 function increment(id) {
    document.getElementById("id").innerHTML = globalCounter++;
    console.log('get success');
}
// ------------------ xử lý thêm sách vào giỏ ---------------------------

function addToCart(id, name, price, path) {
    fetch('/api/cart', {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "selling_price": price,              // từ khóa "selling_price" chỉ qua main.py
            "path": path                        // có thêm bớt biến thì tắt bật trang lại cho chắc, sure kèo :))
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data);
        alert(data.message);
        location.reload();
    }).catch(err => {
        console.log(err);
    })

    // promise --> await/async
}


// Tăng số lượng trong giỏ
function addPlus(id, name, price, path) {
    fetch('/api/cart', {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "selling_price": price,              // từ khóa "selling_price" chỉ qua main.py
            "path": path                        // có thêm bớt biến thì tắt bật trang lại cho chắc, sure kèo :))
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data);
        location.reload();
    }).catch(err => {
        console.log(err);
    })

    // promise --> await/async
}


// giảm số lượng trong giỏ
function subtractCart(id) {
    fetch('/api/subtractcart', {
        method: "post",
        body: JSON.stringify({
            "id": id
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data);
        location.reload();
    }).catch(err => {
        console.log(err);
    })
}


// xóa khỏi giỏ hàng
function deleteCart(id) {
    fetch('/api/deletecart', {
        method: "post",
        body: JSON.stringify({
            "id": id
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data);
        location.reload();
    }).catch(err => {
        console.log(err);
    })
}

// Thực hiện mua ngay
function buyNow(id, name, price, path) {
    fetch('/api/buy', {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "selling_price": price,
            "path": path
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data);
//        alert(data.message);
    }).catch(err => {
        console.log(err);
    })
}


// --------------------------- Xử lý thanh toán -----------------------------

//function pay() {
//    fetch('/api/pay', {
//        method: 'post',
//        headers: {
//            "Content-Type": 'application/json'
//        }
//    }).then(res => res.json()).then(data => {
//        alert(data.message);
//        location.reload();
//        location.href = '/login?next=/checkout';
//    }).catch(res => {
//        console.log(res);
//    })
//}





// --------------------- xử lý thêm sách vào danh mục yêu thích ----------------------

function addToWishlist(id, name, price, path) {
    fetch('/api/wish', {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "selling_price": price,
            "path": path
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        alert(data.message);
        console.info(data);
    }).catch(err => {
        console.log(err);
    })
}


// Xóa khỏi danh sách yêu thích
function deleteWish(id) {
    fetch('/api/deletewish', {
        method: "post",
        body: JSON.stringify({
            "id": id
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data);
//        alert(data.message);
        location.reload();
    }).catch(err => {
        console.log(err);
    })
}


// ---------------------    back to top     ---------------------------
var btnTop = document.getElementById("btnTop");
window.onscroll = function() {scrollFunction()};


function scrollFunction() {
    var btnTop = document.getElementById("btnTop");
    if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 500) {
        btnTop.style.display = "block";
    } else {
        btnTop.style.display = "none";
    }
}


function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}



// ------------------------
