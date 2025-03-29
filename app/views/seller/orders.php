<?php include 'app/views/shares/header.php'; ?>
<div class="container mt-4">
    <h1>Quản lý Đơn hàng</h1>
    <table class="table table-striped">
        <thead>
            <tr>
                <th>ID</th>
                <th>Khách hàng</th>
                <th>Số điện thoại</th>
                <th>Địa chỉ</th>
                <th>Ngày đặt</th>
                <th>Hành động</th>
            </tr>
        </thead>
        <tbody>
            <?php if(isset($orders) && is_array($orders) && count($orders) > 0): ?>
                <?php foreach($orders as $order): ?>
                    <tr>
                        <td><?php echo $order['id']; ?></td>
                        <td><?php echo $order['name']; ?></td>
                        <td><?php echo $order['phone']; ?></td>
                        <td><?php echo $order['address']; ?></td>
                        <td><?php echo $order['created_at']; ?></td>
                        <td>
                            <a href="/mini_ecommerce/seller/orderDetails/<?php echo $order['id']; ?>" class="btn btn-info btn-sm">Chi tiết</a>
                        </td>
                    </tr>
                <?php endforeach; ?>
            <?php else: ?>
                <tr>
                    <td colspan="6">Không có đơn hàng nào</td>
                </tr>
            <?php endif; ?>
        </tbody>
    </table>
</div>
<?php include 'app/views/shares/footer.php'; ?>
