<?php include 'app/views/shares/header.php'; ?>
<div class="container mt-4">
    <h1>Thêm sản phẩm mới</h1>
    <form action="/mini_ecommerce/seller/addProduct?action=addProduct" method="post">
        <div class="mb-3">
            <label for="name" class="form-label">Tên sản phẩm</label>
            <input type="text" class="form-control" id="name" name="name" required>
        </div>
        <div class="mb-3">
            <label for="description" class="form-label">Mô tả</label>
            <textarea class="form-control" id="description" name="description" rows="3"></textarea>
        </div>
        <div class="mb-3">
            <label for="price" class="form-label">Giá</label>
            <input type="number" step="0.01" class="form-control" id="price" name="price" required>
        </div>
        <div class="mb-3">
            <label for="category_id" class="form-label">Danh mục</label>
            <input type="number" class="form-control" id="category_id" name="category_id">
            <!-- Bạn có thể thay input bằng select nếu có danh sách danh mục -->
        </div>
        <div class="mb-3">
            <label for="image" class="form-label">Ảnh (URL)</label>
            <input type="text" class="form-control" id="image" name="image">
        </div>
        <button type="submit" class="btn btn-primary">Thêm sản phẩm</button>
    </form>
</div>
<?php include 'app/views/shares/footer.php'; ?>
