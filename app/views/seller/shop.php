<?php include 'app/views/shares/header.php'; ?>
<div class="container mt-4">
    <h1>Quản lý Thông tin Shop</h1>
    <form action="/mini_ecommerce/seller/updateShop" method="post">
        <div class="mb-3">
            <label for="shopName" class="form-label">Tên Shop</label>
            <input type="text" class="form-control" id="shopName" name="shopName" value="<?php echo isset($shopName) ? $shopName : ''; ?>" required>
        </div>
        <div class="mb-3">
            <label for="shopAddress" class="form-label">Địa chỉ</label>
            <input type="text" class="form-control" id="shopAddress" name="shopAddress" value="<?php echo isset($shopAddress) ? $shopAddress : ''; ?>" required>
        </div>
        <div class="mb-3">
            <label for="shopPhone" class="form-label">Số điện thoại</label>
            <input type="text" class="form-control" id="shopPhone" name="shopPhone" value="<?php echo isset($shopPhone) ? $shopPhone : ''; ?>" required>
        </div>
        <button type="submit" class="btn btn-primary">Cập nhật</button>
    </form>
</div>
<?php include 'app/views/shares/footer.php'; ?>
