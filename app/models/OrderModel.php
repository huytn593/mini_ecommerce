<?php
class OrderModel {
    private $conn;
    private $table_name = "orders";

    public function __construct($db) {
        $this->conn = $db;
    }

    /**
     * Lấy danh sách đơn hàng liên quan đến seller.
     * Giả sử rằng:
     * - Bảng orders chứa thông tin đơn hàng.
     * - Bảng order_details chứa chi tiết đơn hàng với cột product_id.
     * - Bảng product chứa cột seller_username để xác định người bán.
     */
    public function getOrdersBySeller($seller_username) {
        $query = "SELECT DISTINCT o.id, o.name, o.phone, o.address, o.created_at
                  FROM orders o
                  JOIN order_details od ON o.id = od.order_id
                  JOIN product p ON od.product_id = p.id
                  WHERE p.seller_username = :seller_username";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(':seller_username', $seller_username, PDO::PARAM_STR);
        $stmt->execute();
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
}
?>
