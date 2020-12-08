
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


