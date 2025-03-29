<?php include 'app/views/shares/header.php'; ?>

<h1>Giỏ hàng</h1>

<?php if (!empty($cart)): ?>
    <ul class="list-group">
        <?php 
        $total = 0; // Thêm biến tính tổng tiền
        foreach ($cart as $id => $item): 
            $subtotal = $item['price'] * $item['quantity'];
            $total += $subtotal;
        ?>
            <li class="list-group-item">
                <h2><?php echo htmlspecialchars($item['name'], ENT_QUOTES, 'UTF-8'); ?></h2>
                <?php if ($item['image']): ?>
                    <img src="/mini_ecommerce/<?php echo $item['image']; ?>" alt="Product Image" style="max-width: 100px;">
                <?php endif; ?>
                <p>Đơn giá: <?php echo number_format($item['price'], 0, ',', '.') ?> VND</p>
                
                <!-- Phần điều chỉnh số lượng -->
                <div class="quantity-control d-flex align-items-center gap-2">
                    <form action="/mini_ecommerce/Product/updateQuantity" method="POST">
                        <input type="hidden" name="product_id" value="<?= $id ?>">
                        <input type="hidden" name="quantity" value="<?= $item['quantity'] - 1 ?>">
                        <button type="submit" >-</button>
                    </form>
                    
                    <span><?= $item['quantity'] ?></span>
                    
                    <form action="/mini_ecommerce/Product/updateQuantity" method="POST">
                        <input type="hidden" name="product_id" value="<?= $id ?>">
                        <input type="hidden" name="quantity" value="<?= $item['quantity'] + 1 ?>">
                        <button type="submit" >+</button>
                    </form>
                </div>

                <p>Thành tiền: <?php echo number_format($subtotal, 0, ',', '.') ?> VND</p>
            </li>
        <?php endforeach; ?>
    </ul>

    <!-- Hiển thị tổng tiền -->
    <div class="mt-3 fw-bold">
        Tổng cộng: <?php echo number_format($total, 0, ',', '.') ?> VND
    </div>
<?php else: ?>
    <p>Giỏ hàng của bạn đang trống.</p>
<?php endif; ?>

<a href="/mini_ecommerce/Product" class="btn btn-secondary mt-2">Tiếp tục mua sắm</a>
<a href="/mini_ecommerce/Product/checkout" class="btn btn-secondary mt-2">Thanh Toán</a>
<style>
  .list-group-item {
    background-color: white; 
    padding: 15px 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
    transition: all 0.3s ease-in-out; /* Hiệu ứng mượt */
    cursor: pointer;
    width: 190px;
    border-left: 2px solid black;
   

}

.row{
    display: flex;
    gap: 10px;
    white-space: nowrap;

}

.list-group-item:hover {
    transform: translateY(-10px); 
    box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.15); 
    background-color: #f8f9fa; 
}

    .list-group-item h2{
        font-size: 15px;
        white-space: nowrap;
    }

    .list-group-item img{
        height: 86px;width: 86px;
        
    }

    .list-group{
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

.doanhmuc_p{
    white-space: nowrap;
}

.btn-primary{
    height: 38px;width: 51px;
}

.btn-primary .{
    height: 38px;width: 51px;
}

.row a img{
    height: 45px;width: 45px;
    margin-top: -7px;
    margin-left: -10px;
}


</style>
<?php include 'app/views/shares/footer.php'; ?>
