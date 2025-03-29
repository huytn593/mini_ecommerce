<?php include 'app/views/shares/header.php'; ?>

<style>
    .container-center {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        text-align: center;
        position: relative;
    }

    .moving-button {
        position: absolute;
    }

    btn-primary,
    .btn-danger{
    white-space: nowrap;
    }

    .moving-button {
    position: relative; /* Không còn absolute để căn chỉnh dễ dàng */
}

</style>

<div class="container-center">
    <div style="position: relative; width: 300px; height: 200px;">
        <h1 style="white-space: nowrap; margin-left: -20px;" class="title">Xác nhận đơn hàng</h1>
        <p>Cảm ơn bạn đã đặt hàng. Đơn hàng của bạn đã được xử lý thành công.</p>
        <div style="display: flex; justify-content: center; gap: 10px;">
            <a style="white-space: nowrap" href="/mini_ecommerce/Product" class="btn btn-primary mt-2">Tiếp tục mua sắm</a>
            <button id="moveButton" class="btn btn-danger mt-2 moving-button" onclick="moveRandom()">Không mua nữa</button>
        </div>
    </div>
</div>


<script>
function showToast(message) {
    var toast = document.createElement("div");
    toast.style.position = "fixed";
    toast.style.bottom = "20px";
    toast.style.right = "20px";
    toast.style.backgroundColor = "black";
    toast.style.color = "white";
    toast.style.padding = "10px";
    toast.style.borderRadius = "5px";
    toast.style.zIndex = "1000";
    toast.textContent = message;

    document.body.appendChild(toast);

    // Tự động ẩn thông báo sau 3 giây
    setTimeout(function() {
        toast.remove();
    }, 1000);
}

function moveRandom() {
    var button = document.getElementById("moveButton");
    var container = button.parentElement;

    var containerWidth = container.clientWidth;
    var containerHeight = container.clientHeight;

    // Hệ số nhân để tăng khoảng cách di chuyển (tùy chỉnh theo nhu cầu)
    var scaleFactor = 1000;

    // Tính toán vị trí mới
    var randomX = Math.floor(Math.random() * (containerWidth - button.clientWidth) * scaleFactor) % (containerWidth - button.clientWidth);
    var randomY = Math.floor(Math.random() * (containerHeight - button.clientHeight) * scaleFactor) % (containerHeight - button.clientHeight);

    // Di chuyển nút đến vị trí mới
    button.style.left = randomX + 50 + "px";
    button.style.top = randomY + 50 + "px";

    // Hiển thị thông báo toast
    showToast("Không mua nữa ăn Lon à!!!!!!!");
    
}

</script>
