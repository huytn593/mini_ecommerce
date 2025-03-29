<?php include 'app/views/shares/header.php'; ?>
<div class="container mt-4">
    <h1>Quản lý Sản phẩm</h1>
    <table class="table table-striped">
        <thead>
            <tr>
                <th>ID</th>
                <th>Tên sản phẩm</th>
                <th>Giá</th>
                <th>Danh mục</th>
                <th>Hành động</th>
            </tr>
        </thead>
        <tbody>
            <?php if(isset($products) && is_array($products) && count($products) > 0): ?>
                <?php foreach($products as $product): ?>
                    <tr>
                        <td><?php echo $product['id']; ?></td>
                        <td><?php echo $product['name']; ?></td>
                        <td><?php echo $product['price']; ?></td>
                        <td><?php echo $product['category_name'] ?? 'N/A'; ?></td>
                        <td>
                            <a href="/mini_ecommerce/seller/editProduct/<?php echo $product['id']; ?>" class="btn btn-warning btn-sm">Edit</a>
                            <a href="/mini_ecommerce/seller/deleteProduct/<?php echo $product['id']; ?>" class="btn btn-danger btn-sm" onclick="return confirm('Bạn có chắc chắn muốn xóa?');">Delete</a>
                        </td>
                    </tr>
                <?php endforeach; ?>
            <?php else: ?>
                <tr>
                    <td colspan="5">Không có sản phẩm nào</td>
                </tr>
            <?php endif; ?>
        </tbody>
    </table>
    <a href="/mini_ecommerce/seller/addProduct" class="btn btn-success">Thêm sản phẩm mới</a>
</div>
<?php include 'app/views/shares/footer.php'; ?>
