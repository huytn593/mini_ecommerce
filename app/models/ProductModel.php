<?php
class ProductModel
{
    private $conn;
    private $table_name = "product";

    public function __construct($db)
    {
        $this->conn = $db;
    }
    public function getProductsBySeller($seller_username) {
        $query = "SELECT p.id, p.name, p.description, p.price, p.image, c.name as category_name
                  FROM " . $this->table_name . " p
                  LEFT JOIN category c ON p.category_id = c.id
                  WHERE p.seller_username = :seller_username";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(':seller_username', $seller_username, PDO::PARAM_STR);
        $stmt->execute();
        return $stmt->fetchAll(PDO::FETCH_OBJ);
    }
    
    public function getProducts()
    {
        $query = "SELECT p.id, p.name, p.description, p.price, p.image, c.name as category_name
                  FROM " . $this->table_name . " p
                  LEFT JOIN category c ON p.category_id = c.id";
        $stmt = $this->conn->prepare($query);
        $stmt->execute();
        return $stmt->fetchAll(PDO::FETCH_OBJ);
    }

    // Lấy sản phẩm theo id (dùng cho edit)
    public function getProductById($id)
    {
        $query = "SELECT * FROM " . $this->table_name . " WHERE id = :id";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(':id', $id, PDO::PARAM_INT);
        $stmt->execute();
        return $stmt->fetch(PDO::FETCH_OBJ);
    }

    // Thêm sản phẩm mới (bao gồm seller_username)
    public function addProduct($name, $description, $price, $category_id, $image, $seller_username)
    {
        // Xử lý dữ liệu đầu vào
        $name = htmlspecialchars(strip_tags($name));
        $description = htmlspecialchars(strip_tags($description));
        $price = (float)$price;
        $category_id = !empty($category_id) ? (int)$category_id : null;
        $image = htmlspecialchars(strip_tags($image));
        $seller_username = htmlspecialchars(strip_tags($seller_username));

        $query = "INSERT INTO " . $this->table_name . " (name, description, price, category_id, image, seller_username) 
                  VALUES (:name, :description, :price, :category_id, :image, :seller_username)";
        $stmt = $this->conn->prepare($query);

        $stmt->bindParam(':name', $name);
        $stmt->bindParam(':description', $description);
        $stmt->bindParam(':price', $price, PDO::PARAM_STR);
        $stmt->bindParam(':category_id', $category_id, $category_id !== null ? PDO::PARAM_INT : PDO::PARAM_NULL);
        $stmt->bindParam(':image', $image);
        $stmt->bindParam(':seller_username', $seller_username);

        return $stmt->execute();
    }

    // Cập nhật sản phẩm (chỉ cho seller của sản phẩm được cập nhật)
    public function updateProduct($id, $name, $description, $price, $category_id, $image, $seller_username)
    {
        $query = "UPDATE " . $this->table_name . " 
                  SET name = :name, description = :description, price = :price, category_id = :category_id, image = :image 
                  WHERE id = :id AND seller_username = :seller_username";
        $stmt = $this->conn->prepare($query);

        $name = htmlspecialchars(strip_tags($name));
        $description = htmlspecialchars(strip_tags($description));
        $price = (float)$price;
        $category_id = !empty($category_id) ? (int)$category_id : null;
        $image = htmlspecialchars(strip_tags($image));
        $seller_username = htmlspecialchars(strip_tags($seller_username));

        $stmt->bindParam(':id', $id, PDO::PARAM_INT);
        $stmt->bindParam(':name', $name);
        $stmt->bindParam(':description', $description);
        $stmt->bindParam(':price', $price, PDO::PARAM_STR);
        $stmt->bindParam(':category_id', $category_id, $category_id !== null ? PDO::PARAM_INT : PDO::PARAM_NULL);
        $stmt->bindParam(':image', $image);
        $stmt->bindParam(':seller_username', $seller_username);

        return $stmt->execute();
    }

    // Xóa sản phẩm (chỉ cho seller của sản phẩm được xóa)
    public function deleteProduct($id, $seller_username)
    {
        $query = "DELETE FROM " . $this->table_name . " WHERE id = :id AND seller_username = :seller_username";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(':id', $id, PDO::PARAM_INT);
        $stmt->bindParam(':seller_username', $seller_username);
        return $stmt->execute();
    }
}
?>
