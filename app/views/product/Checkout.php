<?php include 'app/views/shares/header.php'; ?>


<form method="POST" action="/mini_ecommerce/Product/processCheckout">
<h1>Thanh toán</h1>

    <div class="form-group">
        <label for="name">Họ tên:</label>
        <input type="text" id="name" name="name" class="form-control" required>
    </div>
    <div class="form-group">
        <label for="phone">Số điện thoại:</label>
        <input type="text" id="phone" name="phone" class="form-control" required>
    </div>
    <div class="form-group">
        <label for="address">Địa chỉ:</label>
        <textarea id="address" name="address" class="form-control" required></textarea>
    </div>
    <button type="submit" class="btn btn-primary">Thanh toán</button>
<a href="/mini_ecommerce/Product/cart" class="btn btn-secondary mt-2">Quay lại giỏ hàng</a>

</form>

<style>
    form{
        width: 300px;
        margin-left: 550px;
        margin-top: 20px;
    }

    .btn-primary{
        width: 300px;
    }
</style>
<?php include 'app/views/shares/footer.php'; ?>
