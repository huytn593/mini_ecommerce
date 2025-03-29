<?php
// /mini_ecommerce/controllers/SellerController.php

session_start();
require_once __DIR__ . '/../models/ProductModel.php';
require_once __DIR__ . '/../models/OrderModel.php';

class SellerController {
    public function __construct() {
        // Nếu chưa đăng nhập, chuyển hướng đến trang đăng nhập
        if (!isset($_SESSION['user'])) {
            header("Location: /mini_ecommerce/views/account/login.php");
            exit;
        }
        // Chỉ cho phép role seller và admin truy cập
        if ($_SESSION['user']['role'] !== 'seller' && $_SESSION['user']['role'] !== 'admin') {
            header("Location: /mini_ecommerce/views/account/login.php");
            exit;
        }
    }

    // Quản lý đơn hàng của người bán
    public function manageOrders() {
        // Lấy dữ liệu đơn hàng theo seller nếu cần (gọi model OrderModel nếu có)
        include_once __DIR__ . '/../views/seller/orders.php';
    }

    // Quản lý sản phẩm của người bán
    public function manageProducts() {
        // Lấy dữ liệu sản phẩm theo seller nếu cần (gọi model ProductModel nếu có)
        include_once __DIR__ . '/../views/seller/products.php';
    }

    // Quản lý thông tin shop của người bán
    // Quản lý thông tin shop của người bán
    public function manageShop() {
        // Ví dụ: lấy thông tin shop của seller (có thể lấy từ ShopModel nếu có)
        // Nếu chưa có model ShopModel, ta dùng dữ liệu mẫu
        $shopInfo = [
            'shopName'    => 'Tên Shop của bạn',
            'shopAddress' => 'Địa chỉ shop',
            'shopPhone'   => 'Số điện thoại shop'
        ];
        // Truyền dữ liệu sang view, có thể dùng extract() để chuyển mảng thành biến
        extract($shopInfo);
        include_once __DIR__ . '/../views/seller/shop.php';
    }
}

// Phần định tuyến đơn giản cho SellerController
if (isset($_GET['action'])) {
    $action = $_GET['action'];
    $sellerController = new SellerController();
    switch($action) {
        case 'manageOrders':
            $sellerController->manageOrders();
            break;
        case 'manageProducts':
            $sellerController->manageProducts();
            break;
        case 'manageShop':
            $sellerController->manageShop();
            break;
        default:
            echo "Action không tồn tại.";
    }
} else {
    echo "Không có action được chỉ định.";
}
?>
