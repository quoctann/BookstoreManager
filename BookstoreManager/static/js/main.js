// Toggle trạng thái hiển thị của menu bên
$(function() {
  // Sidebar toggle behavior
  $('#sidebarCollapse').on('click', function() {
    $('#sidebar, #content').toggleClass('active');
  });
})


// Thêm xóa một phần tử html
function addProduct() {
  var inputID = 0;

  const div = document.createElement('div');

  div.className = 'form-group d-flex';

  div.innerHTML = `
        <input type="text" class="form-control mr-2" name="product_item" placeholder="Nhập gì đó">
        <input type="button" class="btn btn-secondary" value="Xóa" onclick="removeRow(this)" />
  `;

  document.getElementById('sell_form').appendChild(div);
}

// Xóa một phần tử html
function removeRow(input) {
  document.getElementById('sell_form').removeChild(input.parentNode);
}

// Xuất ngày giờ hiện tại,
function printDate() {
    date = Date();
    document.getElementById("invoice-date").innerHTML = date;
    return date;
}