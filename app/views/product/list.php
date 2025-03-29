<?php include 'app/views/shares/header.php'; ?>

<h1>Danh sách sản phẩm</h1>
<a href="/mini_ecommerce/Product/add" class="btn btn-success mb-2">Thêm sản phẩm mới</a>
<ul class="list-group">
    <?php foreach ($products as $product): ?>
        <li class="list-group-item">
            <h2>
                <a href="/mini_ecommerce/Product/show/<?php echo $product->id; ?>">
                    <?php echo htmlspecialchars($product->name ?? '', ENT_QUOTES, 'UTF-8'); ?>
                </a>
            </h2>

            <?php if (!empty($product->image)): ?>
                <img src="/mini_ecommerce/<?php echo htmlspecialchars($product->image, ENT_QUOTES, 'UTF-8'); ?>" 
                     alt="Product Image" style="max-width: 100px;">
            <?php else: ?>
                <img src="/mini_ecommerce/public/img/default.jpg" alt="No Image" style="max-width: 100px;">
            <?php endif; ?>

            <p><?php echo htmlspecialchars($product->description ?? '', ENT_QUOTES, 'UTF-8'); ?></p>
            <p>Giá: <?php echo htmlspecialchars($product->price ?? '0', ENT_QUOTES, 'UTF-8'); ?> VND</p>
            <p class="doanhmuc_p">Danh mục: <?php echo htmlspecialchars($product->category_name ?? 'Không xác định', ENT_QUOTES, 'UTF-8'); ?></p>

            <div class="row">
                <a href="/mini_ecommerce/Product/edit/<?php echo $product->id; ?>" class="btn btn-warning">Sửa</a>
                <a href="/mini_ecommerce/Product/delete/<?php echo $product->id; ?>" class="btn btn-danger" onclick="return confirm('Bạn có chắc chắn muốn xóa sản phẩm này?');">Xóa</a>
                <a href="/mini_ecommerce/Product/addToCart/<?php echo $product->id; ?>" class="btn btn-primary">
                    <img src="/mini_ecommerce/public/img/add-removebg-preview.png" alt="Thêm sản phẩm">
                </a>
            </div>
        </li>
    <?php endforeach; ?>
</ul>

<style>
  .list-group-item {
    background-color: white; 
    padding: 15px 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
    transition: all 0.3s ease-in-out;
    cursor: pointer;
    width: 190px;
    border-left: 2px solid black;
}

.row {
    display: flex;
    gap: 10px;
    white-space: nowrap;
}

.list-group-item:hover {
    transform: translateY(-10px);
    box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.15);
    background-color: #f8f9fa;
}

.list-group-item h2 {
    font-size: 15px;
    white-space: nowrap;
}

.list-group-item img {
    height: 86px;
    width: 86px;
}

.list-group {
    flex-direction: row;
    border: 2px solid black;
}

.btn-success {
    background-color: #28a745;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
    margin-left: 10px;
    transition: all 0.3s ease-in-out;
}

.btn-success:hover {
    background-color: #218838;
    transform: translateY(-3px);
    box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.2);
}

.doanhmuc_p {
    white-space: nowrap;
}

.btn-primary {
    height: 38px;
    width: 51px;
}

.row a img {
    height: 45px;
    width: 45px;
    margin-top: -7px;
    margin-left: -10px;
}
</style>

<?php include 'app/views/shares/footer.php'; ?>
