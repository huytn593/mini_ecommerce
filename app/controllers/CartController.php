
// Trong file app/controllers/CartController.php

public function updateQuantity() {
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $product_id = $_POST['product_id'];
        $action = $_POST['action'];

        if ($action === 'increase') {
            // Tăng số lượng sản phẩm
            $_SESSION['cart'][$product_id]['quantity'] += 1;
        } elseif ($action === 'decrease') {
            // Giảm số lượng sản phẩm, nhưng không nhỏ hơn 1
            if ($_SESSION['cart'][$product_id]['quantity'] > 1) {
                $_SESSION['cart'][$product_id]['quantity'] -= 1;
            }
        }

        // Redirect về trang giỏ hàng
        header('Location: /mini_ecommerce/Cart');
        exit();
    }
}
